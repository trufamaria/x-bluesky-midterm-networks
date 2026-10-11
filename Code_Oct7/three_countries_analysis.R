install.packages(c("readr", "dplyr", "ggplot2", "igraph"))

# ---------------------------------------------------------------
# Community-structure treemap, one chart per country
#
# Reads the folders made by build_network.py:
#   network_Brazil/  network_United_States/  network_Netherlands/
# each with nodes.csv, edges.csv, groups.csv
#
# Saves: treemap_Brazil.png, treemap_United_States.png, treemap_Netherlands.png
#
# Packages (install once):
#   install.packages(c("readr", "dplyr", "ggplot2", "igraph"))
# ---------------------------------------------------------------
library(readr)
library(dplyr)
library(ggplot2)
library(igraph)

 setwd("/Users/marinapetric/PycharmProjects/pythonProject12")

COUNTRIES  <- c("Brazil", "United_States", "Netherlands")
PLATFORM   <- "Bluesky"
MAX_GROUPS <- 60   # show the largest groups only; the rest are counted in the subtitle
EDGE_MIN   <- 5    # groups smaller than this are drawn without edges
SEED       <- 42   # same layout every run


# ---------------------------------------------------------------
# 1. Read one country
# ---------------------------------------------------------------
read_network <- function(country) {
  folder <- paste0("network_", country)
  list(
    nodes  = read_csv(file.path(folder, "nodes.csv"),  show_col_types = FALSE),
    edges  = read_csv(file.path(folder, "edges.csv"),  show_col_types = FALSE),
    groups = read_csv(file.path(folder, "groups.csv"), show_col_types = FALSE)
  )
}


# ---------------------------------------------------------------
# 2. Squarified treemap layout (box area = sqrt of group size)
# ---------------------------------------------------------------
squarify <- function(areas, W = 100, H = 100) {
  areas <- areas / sum(areas) * W * H
  x0 <- 0; y0 <- 0; w <- W; h <- H
  out <- matrix(NA, length(areas), 4)
  i <- 1; n <- length(areas)
  worst <- function(r, side) {
    s <- sum(r)
    max(side^2 * max(r) / s^2, s^2 / (side^2 * min(r)))
  }
  while (i <= n) {
    side <- min(w, h)
    j <- i
    while (j < n && worst(areas[i:(j + 1)], side) <= worst(areas[i:j], side)) j <- j + 1
    row <- areas[i:j]; s <- sum(row)
    if (w >= h) {                       # fill a column on the left
      cw <- s / h; yy <- y0
      for (k in seq_along(row)) {
        hh <- row[k] / cw
        out[i + k - 1, ] <- c(x0, x0 + cw, yy, yy + hh); yy <- yy + hh
      }
      x0 <- x0 + cw; w <- w - cw
    } else {                            # fill a row along the top
      rh <- s / w; xx <- x0
      for (k in seq_along(row)) {
        ww <- row[k] / rh
        out[i + k - 1, ] <- c(xx, xx + ww, y0, y0 + rh); xx <- xx + ww
      }
      y0 <- y0 + rh; h <- h - rh
    }
    i <- j + 1
  }
  # flip so the first (largest) box sits at the top
  data.frame(xmin = out[, 1], xmax = out[, 2],
             ymin = H - out[, 4], ymax = H - out[, 3])
}


# ---------------------------------------------------------------
# 3. Positions of the accounts inside each box
# ---------------------------------------------------------------
sunflower <- function(n) {               # even fill of a disk
  k <- seq_len(n); r <- sqrt(k - 0.5) / sqrt(n); a <- k * pi * (3 - sqrt(5))
  cbind(r * cos(a), r * sin(a))
}

grid_layout <- function(n) {             # small groups: simple grid
  nc <- ceiling(sqrt(n * 1.5)); nr <- ceiling(n / nc)
  cbind(((seq_len(n) - 1) %% nc), -((seq_len(n) - 1) %/% nc)) -> m
  if (nc == 1) m[, 1] <- 0
  if (nr == 1) m[, 2] <- 0
  m
}

rescale_into <- function(m, xmin, xmax, ymin, ymax) {
  sc <- function(v, lo, hi) {
    if (diff(range(v)) == 0) return(rep((lo + hi) / 2, length(v)))
    lo + (v - min(v)) / diff(range(v)) * (hi - lo)
  }
  cbind(sc(m[, 1], xmin, xmax), sc(m[, 2], ymin, ymax))
}


# ---------------------------------------------------------------
# 4. Draw one country
# ---------------------------------------------------------------
plot_network <- function(net, country) {
  set.seed(SEED)
  nodes <- net$nodes; edges <- net$edges
  
  groups <- nodes %>% count(group, name = "size") %>%
    arrange(desc(size), as.integer(sub("G", "", group)))
  n_groups_all <- nrow(groups)
  groups <- head(groups, MAX_GROUPS)
  groups$rank <- seq_len(nrow(groups))
  
  # colors: hue moves around the wheel from the largest to the smallest group
  hues <- seq(0, 300, length.out = nrow(groups))
  groups$col  <- hcl(h = hues, c = 70, l = 52)
  groups$fill <- hcl(h = hues, c = 12, l = 95)
  groups$shape <- c(16, 17, 15, 18, 8)[(groups$rank - 1) %% 5 + 1]
  
  boxes <- cbind(groups, squarify(sqrt(groups$size)))
  
  # within-group edges (accounts in the same group)
  grp_of <- setNames(nodes$group, nodes$id)
  e_in <- edges %>%
    mutate(g1 = grp_of[source], g2 = grp_of[target]) %>%
    filter(!is.na(g1), g1 == g2, g1 %in% groups$group) %>%
    distinct(source, target, g1)
  
  pos <- list()
  for (r in seq_len(nrow(boxes))) {
    b <- boxes[r, ]
    ids <- nodes$id[nodes$group == b$group]
    n <- length(ids)
    w <- b$xmax - b$xmin; h <- b$ymax - b$ymin
    pad_x <- w * 0.12; pad_bot <- h * 0.12; pad_top <- h * 0.22   # room for the label
    
    ge <- e_in[e_in$g1 == b$group, ]
    if (n >= EDGE_MIN && nrow(ge) > 0) {
      g <- graph_from_data_frame(ge[, c("source", "target")], directed = FALSE,
                                 vertices = data.frame(name = ids))
      m <- layout_with_fr(g)
    } else if (n > 12) {
      m <- sunflower(n)
    } else {
      m <- grid_layout(n)
    }
    xy <- rescale_into(m, b$xmin + pad_x, b$xmax - pad_x,
                       b$ymin + pad_bot, b$ymax - pad_top)
    pos[[r]] <- data.frame(id = ids, x = xy[, 1], y = xy[, 2], group = b$group)
  }
  pos <- bind_rows(pos) %>%
    left_join(nodes %>% select(id, degree), by = "id") %>%
    left_join(groups %>% select(group, col, shape, size), by = "group")
  
  # edges are drawn only in groups with at least EDGE_MIN accounts
  big <- groups$group[groups$size >= EDGE_MIN]
  seg <- e_in %>% filter(g1 %in% big) %>%
    left_join(pos %>% select(id, x, y), by = c("source" = "id")) %>%
    left_join(pos %>% select(id, xend = x, yend = y), by = c("target" = "id")) %>%
    left_join(groups %>% select(group, col), by = c("g1" = "group"))
  
  # point size shrinks a little in crowded boxes
  pos$pt <- (1.2 + 2.2 * sqrt(pos$degree / max(pos$degree))) * ifelse(pos$size > 100, 0.7, 1)
  
  shown <- if (n_groups_all > MAX_GROUPS)
    paste0("largest ", MAX_GROUPS, " of ", n_groups_all, " groups shown") else
      paste0(n_groups_all, " groups")
  
  ggplot() +
    geom_rect(data = boxes, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax),
              fill = boxes$fill, color = "grey70", linewidth = 0.3) +
    geom_segment(data = seg, aes(x = x, y = y, xend = xend, yend = yend),
                 color = seg$col, alpha = 0.25, linewidth = 0.25) +
    geom_point(data = pos, aes(x = x, y = y), color = pos$col, shape = pos$shape,
               size = pos$pt, alpha = 0.9) +
    geom_text(data = boxes, aes(x = xmin + 0.6, y = ymax - 0.6,
                                label = paste0(group, " · ", size)),
              hjust = 0, vjust = 1, size = ifelse(boxes$size >= 5, 2.6, 2.1),
              fontface = "bold", color = "grey15") +
    coord_fixed(expand = FALSE) +
    labs(
      title = paste0(PLATFORM, " Interaction Network — Community Structure: ",
                     gsub("_", " ", country)),
      subtitle = paste0(shown, "  ·  ", nrow(nodes), " nodes  ·  ",
                        nrow(edges), " edges  ·  box area reflects relative group size (sqrt-scaled)\n",
                        "groups under ", EDGE_MIN, " accounts shown without edge detail  ·  ",
                        "color represents the cluster a node belongs to")
    ) +
    theme_void(base_size = 11) +
    theme(
      plot.background = element_rect(fill = "#F8F7F3", color = NA),
      plot.title = element_text(face = "bold", size = 16, margin = margin(b = 6)),
      plot.subtitle = element_text(color = "grey35", size = 9.5, lineheight = 1.3,
                                   margin = margin(b = 14)),
      plot.margin = margin(20, 24, 20, 24)
    )
}


# ---------------------------------------------------------------
# 5. Run for every country
# ---------------------------------------------------------------
for (country in COUNTRIES) {
  net <- read_network(country)
  p <- plot_network(net, country)
  ggsave(paste0("treemap_", country, ".png"), p, width = 9, height = 10, dpi = 300)
  cat("Saved treemap_", country, ".png\n", sep = "")
}
