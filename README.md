X vs. Bluesky: Network Structure of 2026 U.S. Midterm Election Discussion

A comparative network analysis of how people talk about the 2026 U.S. midterm elections on X and on Bluesky.

Status: work in progress.

Research question

Do election conversations on X and Bluesky form different community structures? Specifically, how large are the communities on each platform, and how are users distributed across them?

Data
Period: September 1, 2025 to September 1, 2026
Source: Interaction networks exported from NodeXL, one file per platform
X: 525 users, 712 edges
Bluesky: 1,934 users, 2,751 edges

Raw user-level data is not included in this repository. Platform terms of service and user privacy limit what can be shared. The data/ folder explains the file format so the analysis can be repeated with your own NodeXL export.

Method
Export each platform's interaction network from NodeXL.
Read the group (community) assignments for each user.
Draw a treemap for each platform in R with ggplot2. Each box represents one community, and box area is proportional to the number of users in the community.
Compare the two treemaps side by side.

NodeXL's built-in charts do not support this layout, so the treemaps are built in R.

Repository contents
code/      R script that builds the treemaps
data/      Description of the expected input files (no raw data)
figures/   Output images
How to run
Install R and the packages ggplot2, treemapify, and readxl.
Put your NodeXL export files in data/, following the format described in data/README.md.
Run the script in code/.

Author

Marina Petric, Ph.D., Media and Communication, Texas Tech University marinapetric.com
