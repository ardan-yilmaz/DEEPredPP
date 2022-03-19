# DEEPRED++, A TOOL FOR PROTEIN FUNCTION PREDICION
## Gene Ontology-Based protein function prediction on primary structures with a stack of feed-forward deep neural networks.
## This repository includes the source codes to generate datasets from amino acid sequences, and to train the models under the train directory. 

## FILES

### 1. filter.py: Applies similarity-based filtering on amino acid sequences usin the readily availably similarity clusters can be downloaded from UniProt KB.
### 2. generate_datasets_POSSUM.py: Generates datasets for each term in the ontology.