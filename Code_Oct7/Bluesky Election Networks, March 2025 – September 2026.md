# Bluesky Election Networks, March 2025 – September 2026

Oct 7, 2026 · @Marina

## Overview

The Dutch election conversation on Bluesky is the most connected of the three, and the U.S. midterm conversation is the most scattered. Brazil sits in between, with a large connected core built mostly on replies and quote-posts.

The U.S. network (English, "midterm") is the largest, with 26,856 accounts and 70,231 posts. Brazil follows with 10,183 accounts and 58,963 posts, and the Netherlands has 7,860 accounts and 33,858 posts. In the Netherlands, 51.4% of all edges are interactions between different accounts, against 26.5% in Brazil and 22.7% in the United States.

Only 23.7% of Dutch accounts are isolated, compared with 33.8% in Brazil and 52.3% in the United States. More than half of the U.S. accounts posted about the midterms without replying to, quoting or mentioning anyone, and without being addressed by others. The largest connected component holds 71.1% of Dutch accounts, 58.1% of Brazilian accounts and 32.8% of U.S. accounts.

The three samples do not cover the same months (see Data and limitations). Restricted to the common period of April to September 2026, the order between the countries stays the same.

## Volume over time

Posting follows the election calendar in each country. The Dutch sample peaks before the general election of 29 October 2025: October 2025 alone holds 10,078 posts, 29.8% of the Dutch sample. A smaller Dutch peak comes before the municipal elections of 18 March 2026.

&#91;image: Weekly election posts on Bluesky per country, March 2025 to September 2026\]

*Figure 1: Election posts on Bluesky per week, March 2025 – September 2026*

In Brazil and the United States, volume rises steadily toward the 2026 elections. September 2026 alone holds 60.3% of the U.S. posts and 36.3% of the Brazilian posts. Both elections fall after the period: Brazil's first round on 4 October and the U.S. midterms on 3 November.

## Network metrics

The U.S. network has the clearest community structure (modularity 0.792) and almost no returned ties (reciprocity 0.5%). The Dutch network has the weakest community structure (0.424), because many accounts join one large conversation.

*Table 1: Network structure of election discussion on Bluesky, March 2025 – September 2026*

| Metric | Brazil (Portuguese) | United States (English) | Netherlands (Dutch) |
| --- | --- | --- | --- |
| Posts collected | 58,963 | 70,231 | 33,858 |
| Users/vertices | 10,183 | 26,856 | 7,860 |
| Total edges | 59,380 | 72,090 | 35,558 |
| Self-loops | 43,665 (73.5%) | 55,724 (77.3%) | 17,296 (48.6%) |
| Non-self interactions | 15,715 (26.5%) | 16,366 (22.7%) | 18,262 (51.4%) |
| Isolated vertices | 3,438 (33.8%) | 14,058 (52.3%) | 1,863 (23.7%) |
| Largest connected component | 5,913 users (58.1%) | 8,812 users (32.8%) | 5,592 users (71.1%) |
| Community groups (2+ accounts) | 406 | 1,816 | 214 |
| Graph density | 0.000130 | 0.000020 | 0.000254 |
| Modularity | 0.565 | 0.792 | 0.424 |
| Edge reciprocity | 5.8% | 0.5% | 5.4% |

Metrics follow NodeXL's definitions, so they can be read next to the X and Bluesky table in the midterm brief. A self-loop is a post that does not reply to, quote or mention another account. Density falls as networks grow, so the low U.S. value partly reflects size.

**Same period check.** The samples cover different months, so the metrics were also computed for April to September 2026 only, the period all three samples share. The order between the countries holds.

| April – September 2026 | Brazil | United States | Netherlands |
| --- | --- | --- | --- |
| Posts | 54,590 | 70,188 | 8,437 |
| Isolated vertices | 34.8% | 52.4% | 19.3% |
| Largest connected component | 56.6% | 32.8% | 71.0% |
| Modularity | 0.576 | 0.793 | 0.599 |
| Edge reciprocity | 5.6% | 0.5% | 4.8% |

Dutch modularity rises from 0.424 to 0.599 without the 2025 general election. During that campaign, many accounts joined one shared conversation, which blurs the boundaries between groups.

## Interaction types

Replies dominate in all three countries, but each country has its own second channel. Brazil relies on quote-posts (32.2% of interactions), the United States on mentions (25.0%), and the Netherlands on replies almost alone (71.3%).

*Table 2: Non-self interactions by type*

| Type | Brazil | United States | Netherlands |
| --- | --- | --- | --- |
| Replies | 9,682 (61.6%) | 9,339 (57.1%) | 13,028 (71.3%) |
| Quotes | 5,065 (32.2%) | 2,937 (17.9%) | 2,090 (11.4%) |
| Mentions | 968 (6.2%) | 4,090 (25.0%) | 3,144 (17.2%) |

Brazilian users comment on others' posts by quoting them more than by tagging accounts. U.S. users tag other accounts four times as often as Brazilian users, in relative terms.

Replies by an account to its own post (threads) are left out. Reposts are not part of the data, because Bluesky's search returns original posts only.

## Central accounts

The most addressed accounts are different kinds of actors in each country. In the United States, journalists, commentators and opinion media lead. In Brazil, political commentary accounts and digital news sites lead. In the Netherlands, the public broadcaster, a private user and party accounts lead.

*Table 3: Five accounts with the highest in-degree*

| Rank | Brazil | United States | Netherlands |
| --- | --- | --- | --- |
| 1 | Camarote da República (492) | Aaron Rupar (475) | NOS, probable (361) |
| 2 | Revista Fórum (284) | The New Republic (234) | @Marcel / elsschot (352) |
| 3 | Jeff Nascimento (275) | Marc Elias (207) | Progressief Nederland (260) |
| 4 | Brasil 247 (268) | Ron Filipkowski (175) | Rob Jetten (226) |
| 5 | Eixo Político (260) | MeidasTouch (143) | NRC, probable (221) |

In-degree counts every reply, quote and mention an account received. Lula ranks seventh in Brazil (213), and Folha de S.Paulo sixth (257). In the Netherlands, the parties VVD (214) and D66 (204) follow in seventh and eighth place.

Betweenness shows which accounts link otherwise separate parts of the network. Camarote da República ranks first in Brazil and Aaron Rupar first in the United States, so the most addressed accounts also hold those networks together. In the Netherlands, NOS (probable) ranks first and @Marcel second.

In the United States, the next accounts by betweenness are ordinary users (joesm, waiting74patiently, John Doffing). Those users connect separate conversations without being prominent themselves.

Accounts marked "probable" never posted in the sample, so their names are not in the data. They were identified from the @handles in posts that mention them: 101 of 102 posts mentioning the first Dutch account tag @nieuws.nos.nl, and 85 of 86 posts mentioning the fifth tag @nrc.nl. One U.S. account (rank 6, 140) could not be identified. Running network\_metrics.R with LOOKUP\_HANDLES <- TRUE fills in all names.

## Community structure

The U.S. network splits into many small communities, while the Brazilian and Dutch networks each have a few large ones. The ten largest groups hold 31.5% of connected U.S. accounts, against 58.9% in both Brazil and the Netherlands. Each figure shows the 60 largest groups; box area reflects group size (square-root scaled).

&#91;image: Community structure of the Brazilian election network on Bluesky\]

*Figure 2: Community structure of election discussion on Bluesky, Portuguese (Brazil)*

&#91;image: Community structure of the U.S. midterm network on Bluesky\]

*Figure 3: Community structure of midterm discussion on Bluesky, English (United States)*

&#91;image: Community structure of the Dutch election network on Bluesky\]

*Figure 4: Community structure of election discussion on Bluesky, Dutch (Netherlands)*

A group often forms around one popular account or post, for example the replies to Aaron Rupar or to NOS. High modularity therefore does not mean the groups are political camps. Showing that would require coding who is in each group and what they post.

## Data and limitations

Only the Dutch sample covers the full period. The English and Portuguese searches reached the limit of 20,000 posts per search term, and Bluesky returns the newest posts first, so those samples start later.

| Sample | Search terms | Period covered | Posts | Limit reached |
| --- | --- | --- | --- | --- |
| Portuguese | eleição, eleições | 16 Feb – 29 Sep 2026 | 58,963 | Yes |
| English | midterm, midterm election(s) | 31 Mar – 29 Sep 2026 | 70,231 | Yes |
| Dutch | verkiezing, verkiezingen | 1 Mar 2025 – 29 Sep 2026 | 33,858 | No |

- **Different periods.** The Dutch sample includes the 2025 general election; the other two end before their elections. The check on April–September 2026 (Table 1) shows the same order between countries.
- **Different search terms.** The English search uses "midterm", which targets the U.S. election. The Portuguese and Dutch searches use the general word for election. About 9% of English posts refer to the UK or Canada, 9% of Dutch posts discuss U.S. politics, and about 1% of Portuguese posts refer to Portugal.
- **Language, not country.** Searches were filtered by post language, so the samples include some posts from other countries that share the language.
- **Communities.** Groups come from the Louvain method with a fixed seed. NodeXL usually uses Clauset-Newman-Moore, so modularity may differ slightly from NodeXL's value on the same data.
- **Reposts and deleted posts.** Reposts are not included. Posts deleted before collection are missing.

Posts were collected from Bluesky's public search API with Python. Networks and metrics were computed in Python (networkx) and R (igraph).
