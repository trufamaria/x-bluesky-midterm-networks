# ---------------------------------------------------------------
# Network metrics per country, in the same form as the NodeXL brief
# (Table 1: users, edges, self-loops, isolates, largest component,
#  density, modularity, reciprocity) plus edge types and top accounts.
#
# Needs, in the working directory:
#   bluesky_elections_pt_en_nl.csv          (from the collection script)
#   network_Brazil/, network_United_States/, network_Netherlands/
#                                            (from build_network.py)
#
# Saves:
#   metrics_comparison.csv       Table 1, one column per country
#   edge_types.csv               replies / mentions / quotes per country
#   top_accounts_<country>.csv   top 10 by in-degree and by betweenness
#
# Packages: install.packages(c("readr", "dplyr", "igraph", "jsonlite"))
# ---------------------------------------------------------------
library(readr)
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(igraph))

# setwd("path/to/folder")

COUNTRIES <- c(pt = "Brazil", en = "United_States", nl = "Netherlands")
POSTS_CSV <- "bluesky_elections_pt_en_nl.csv"
TOP_N     <- 10
LOOKUP_HANDLES <- TRUE   # fill in handles of top accounts that never posted
                         # (uses Bluesky's public API; set FALSE if offline)

posts_all <- read_csv(POSTS_CSV, show_col_types = FALSE)

fmt_n   <- function(x) format(x, big.mark = ",")
fmt_pct <- function(x, total) sprintf("%s (%.1f%%)", fmt_n(x), 100 * x / total)

lookup_profiles <- function(dids) {
  dids <- unique(dids[!is.na(dids)])
  if (!LOOKUP_HANDLES || length(dids) == 0) return(NULL)
  out <- list()
  for (chunk in split(dids, ceiling(seq_along(dids) / 25))) {
    url <- paste0("https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles?",
                  paste0("actors=", chunk, collapse = "&"))
    res <- suppressWarnings(try(jsonlite::fromJSON(url), silent = TRUE))
    if (!inherits(res, "try-error") && length(res$profiles) > 0) {
      p <- res$profiles
      out[[length(out) + 1]] <- data.frame(
        id = p$did, handle_api = p$handle,
        name_api = if (is.null(p$displayName)) NA else p$displayName)
    }
  }
  bind_rows(out)
}


metrics <- list(); types <- list()

for (lang in names(COUNTRIES)) {
  country <- COUNTRIES[[lang]]
  folder  <- paste0("network_", country)
  posts   <- posts_all %>% filter(search_lang == lang)
  edges   <- read_csv(file.path(folder, "edges.csv"), show_col_types = FALSE)
  nodes   <- read_csv(file.path(folder, "nodes.csv"), show_col_types = FALSE)

  # --- Self-loops, as NodeXL counts them: one per post that does not
  #     reply to, quote, or mention another account
  posts_with_tie <- unique(edges$post_uri)
  n_selfloops <- sum(!posts$post_uri %in% posts_with_tie)
  n_ties      <- nrow(edges)                       # non-self interactions
  n_edges     <- n_selfloops + n_ties

  # --- All accounts: everyone who posted plus everyone they addressed
  all_ids <- base::union(posts$author_did, base::union(edges$source, edges$target))
  n_users <- length(all_ids)

  g <- graph_from_data_frame(edges[, c("source", "target")], directed = TRUE,
                             vertices = data.frame(name = all_ids))
  g_simple <- simplify(g, remove.multiple = TRUE, remove.loops = TRUE)

  n_isolated <- sum(degree(g_simple, mode = "all") == 0)
  comp       <- components(g_simple, mode = "weak")
  largest    <- max(comp$csize)
  density    <- ecount(g_simple) / (n_users * (n_users - 1))
  recip      <- reciprocity(g_simple)               # share of edges returned

  # modularity of the community groups from build_network.py
  to_und <- if (exists("as_undirected")) as_undirected else as.undirected  # igraph 2.x / 1.x
  g_und <- to_und(g_simple, mode = "collapse")
  memb  <- setNames(nodes$group, nodes$id)
  connected <- V(g_und)$name[degree(g_und) > 0]
  g_conn <- induced_subgraph(g_und, connected)
  modul <- modularity(g_conn, as.integer(factor(memb[V(g_conn)$name])))

  metrics[[country]] <- c(
    "Users/vertices"             = fmt_n(n_users),
    "Total edges"                = fmt_n(n_edges),
    "Self-loops"                 = fmt_pct(n_selfloops, n_edges),
    "Non-self interactions"      = fmt_pct(n_ties, n_edges),
    "Isolated vertices"          = fmt_pct(n_isolated, n_users),
    "Largest connected component"= sprintf("%s users (%.1f%%)", fmt_n(largest),
                                           100 * largest / n_users),
    "Graph density"              = sprintf("%.6f", density),
    "Modularity"                 = sprintf("%.3f", modul),
    "Edge reciprocity"           = sprintf("%.1f%%", 100 * recip)
  )

  # --- Edge types (share of non-self interactions)
  types[[country]] <- edges %>% count(type) %>%
    mutate(share = sprintf("%.1f%%", 100 * n / sum(n)), country = country)

  # --- Top accounts
  indeg <- degree(g, mode = "in")                  # counts every reply/mention/quote
  betw  <- betweenness(g_und, directed = FALSE)
  info  <- posts %>% distinct(author_did, .keep_all = TRUE) %>%
    select(id = author_did, handle = author_handle, name = author_name)

  top <- bind_rows(
    data.frame(measure = "in-degree", id = names(sort(indeg, decreasing = TRUE))[1:TOP_N],
               value = sort(indeg, decreasing = TRUE)[1:TOP_N]),
    data.frame(measure = "betweenness", id = names(sort(betw, decreasing = TRUE))[1:TOP_N],
               value = round(sort(betw, decreasing = TRUE)[1:TOP_N], 1))
  ) %>%
    left_join(info, by = "id") %>%
    left_join(nodes %>% select(id, group), by = "id")

  api <- lookup_profiles(top$id[is.na(top$handle)])
  if (!is.null(api) && nrow(api) > 0) {
    top <- top %>% left_join(api, by = "id") %>%
      mutate(handle = coalesce(handle, handle_api), name = coalesce(name, name_api)) %>%
      select(-handle_api, -name_api)
  }
  top <- top %>% select(measure, rank = value, handle, name, group, id) %>%
    group_by(measure) %>% mutate(position = row_number()) %>% ungroup() %>%
    rename(value = rank) %>% select(measure, position, value, handle, name, group, id)

  write_csv(top, paste0("top_accounts_", country, ".csv"))
  cat("\n=====", gsub("_", " ", country), "=====\n")
  print(as.data.frame(top %>% select(measure, position, value, handle, name)), row.names = FALSE)
}

table1 <- data.frame(Metric = names(metrics[[1]]), metrics, check.names = FALSE)
names(table1) <- gsub("_", " ", names(table1))
write_csv(table1, "metrics_comparison.csv")

edge_types <- bind_rows(types) %>% select(country, type, n, share)
write_csv(edge_types, "edge_types.csv")

cat("\n===== Table 1 =====\n");      print(table1, row.names = FALSE)
cat("\n===== Edge types =====\n");   print(as.data.frame(edge_types), row.names = FALSE)
