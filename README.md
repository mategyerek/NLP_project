# NLP_project
## Conda env
### Create:
conda env create -f environment.yml
### Update
conda env update --file environment.yml --prune

## You should have your file tree like this
python files...
data
    ├───combatfootage
    └───geopolitics

## Preprocessing
**Note:** Some of the data files are very big so you need a lot of memory
Run the following commands from the root directory:
`
conda activate NLP
python Initial_clean_parent_child_exclude.py
python group_by_user.py
`

The data will be written to `data/geo_by_user.ndjson` and `data/cf_by_user.ndjson`

Then run `NER_filter.py` in order to obtain only the posts relevatn to the Russia-Ukraine conflict, which will be written to `data/filtered_combatfootage.csv`

