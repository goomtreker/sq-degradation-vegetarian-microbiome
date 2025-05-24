library(ape)
install.packages('ggtree')
library(ggtree)
if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("ggtree")
library(readr)

library(ggplot2)
library(tidyr)
library(ggnewscale)
library(dplyr)
library(purrr)
library(tibble)
library(stringr)
library(ggnewscale) 

# import tree from UHGP
uhgp_tree <- read.tree('bac120_iqtree.nwk')

# save the data about taxons and SQ metadata
data <- read.csv('locus_result.csv', sep = ',')
data[c("Domen","Phylum","Class","Order","Family","Genus","Species")] <- str_split_fixed(data$Lineage, ";",7)
data <- filter(data, Species != 's__')
data <- data %>% 
  filter(!grepl("[0-9]", Genus))

selected_ids <- data$Species_rep

heatmap_data <- data[,c("Species_rep","EMP","TK", "TAL", "ED")]
heatmap_data[,2:5] <- lapply(heatmap_data[,2:5], function(x) as.numeric(as.logical(x)))
heatmap_data <- heatmap_data[heatmap_data$Species_rep %in% selected_ids, ]
heatmap_data <- heatmap_data[!duplicated(heatmap_data$Species_rep),]
rownames(heatmap_data) <- heatmap_data$Species_rep
heatmap_data <- heatmap_data[, -1]

# tree filtration
filtered_tree <- keep.tip(uhgp_tree, selected_ids)
common_ids <- intersect(selected_ids,uhgp_tree$tip.label)
write.csv(common_ids, 'common_ids.tsv')

# taxonomy label
taxonomy <- data[,c("Species_rep","Species","Lineage")]

taxonomy_split <- taxonomy %>%
  separate(col = Lineage,
           sep = ';',
           into = c('Domain', 'Phylum', 'Class', 'Order', 'Family', 'Genus','Species'),
           remove = FALSE,
           extra = 'drop',
           fill = 'right')


taxonomy_split$Phylum[taxonomy_split$Phylum == "p__Firmicutes_C"] <- "p__Firmicutes"
taxonomy_split$Phylum[taxonomy_split$Phylum == "p__Firmicutes_A"] <- "p__Firmicutes"
taxonomy_split$Phylum[taxonomy_split$Phylum == "p__Proteobacteria"] <- "p__Pseudomonadota"

taxonomy_valid <- taxonomy_split %>%
  filter(Species_rep %in% filtered_tree$tip.label) %>%
  distinct(Phylum, Species_rep)

taxonomy_valid$node = nodeid(filtered_tree, taxonomy_valid$Species_rep)



# tree making
p <- ggtree(filtered_tree, branch.length = "none", mrsd = "2013-01-01") %<+% taxonomy_split +
  layout_circular() +
  geom_treescale(x = 1980, y = 0.005, offset = 3) +
  geom_hilight(
    data = taxonomy_valid,
    aes(node = node, fill = Phylum),
    alpha = 0.7,
    extend = 9.7
  ) +
  geom_tiplab(
    aes(label = paste(Species)),
    size = 2.5,
    align = FALSE,
    offset = 0.9,
    show.legend = FALSE
  ) +
  scale_fill_manual(
    values = c(
      "p__Bacteroidota" = 'pink',
      "p__Pseudomonadota" = 'blue',
      "p__Firmicutes" = 'forestgreen',
      "p__Verrucomicrobiota" = 'khaki'  ,
      "p__Fusobacteriota" = 'salmon',
      "p__Actinobacteriota" = 'orange',
      "p__Spirochaetota" = 'purple',
      "p__Desulfobacterota" = 'aquamarine'
    ),
    name = "Phylum"
  )

# Add new scale for heatmap
p <- p + new_scale_fill() 

# final tree
p_heatmap <- gheatmap(
  p = p,
  data = heatmap_data,
  offset = 9,
  width = 0.5,
  colnames = TRUE
) +
  scale_fill_gradientn(
    colors = c("red","green"),
    name = "Value",
    na.value = "grey"
  )

ggsave("plot2.png",  p_heatmap, width = 30, height = 30, dpi = 300)


