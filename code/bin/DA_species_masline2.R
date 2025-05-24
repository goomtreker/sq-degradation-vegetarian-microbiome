# install packages
if(!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("Maaslin2")
library(Maaslin2)
install.packages('plotly')
library(plotly)
install.packages("scales")
library(scales)

# import data

LastDataset <- read_excel("LastDataset.xlsx")
input_data2 <- LastDataset
input_data2 <- as.data.frame(input_data2)
rownames(input_data2) <- input_data2$X
input_data2 <- input_data2[,-1]


# import metadata
input_metadata <- read.csv('metadata_rpkm.csv',sep = ';')
rownames(input_metadata) <- input_metadata$sample_name
input_metadata <- input_metadata[,-1]
input_metadata$diet_type <- input_metadata$diet_type %>%
  replace(grepl("omnivore", ., ignore.case = TRUE), "Omnivore")
input_metadata2 <- input_metadata[rownames(input_metadata) %in% rownames(input_data2),]

# outliers 
hist(input_data2$`s__Bacteroides acidifaciens`) 
hist(input_data2$`s__Phocaeicola sartorii`)
hist(input_data2$`s__Escherichia coli_D`)
mean(input_data2$`s__Escherichia coli_D`)
input_data2$`s__Bacteroides acidifaciens`[input_data2$`s__Bacteroides acidifaciens` >= 580] <- 100.1763
input_data2$`s__Phocaeicola sartorii`[input_data2$`s__Phocaeicola sartorii` >= 1000] <- 150.6923
input_data2$`s__Escherichia coli_D`[input_data2$`s__Escherichia coli_D` >= 3000] <- 789.9056

# Maaslin2 run
fit_data <- Maaslin2(
  input_data = input_data2, 
  input_metadata = input_metadata2, 
  output = 'sq_output_path_lm',
  analysis_method = 'LM',
  fixed_effects = c('diet_type','age_cat','sex'),
  reference = c(
    "diet_type:Vegetarian",
    "age_cat:30s",
    "sex:Male"
  ),
  transform = 'LOG',
  normalization = 'NONE',
  standardize = TRUE, 
  cores = 1
)