# NLP_project

## Setup
### Dependencies
Create the environment using `conda env create -f environment.yml`
Make sure you are in the nlp conda environment. Additionally, run `pip install spacy` and `python -m spacy download en_core_web_sm`

### File tree
You should have your file tree like this. The data folders are too big so they have to be added manually.

    ├─python files...
    ├─data
        ├───combatfootage
        └───geopolitics

## Preprocessing

**Note:** Some of the data files are very big so you need a lot of memory
Run the following commands from the root directory:
`
conda activate NLP
`
`
python Initial_clean_parent_child_exclude.py
`
`
python group_by_user.py
`

The data will be written to `data/geo_by_user.ndjson` and `data/cf_by_user.ndjson`.

Then run `NER_filter.py` in order to obtain only the posts relevatn to the Russia-Ukraine conflict, which will be written to `data/filtered_combatfootage.csv`

## Sentiment analysis
Then run `sentiment.py` to classify the sentiment of the filtered data. The variable `infile` ("combatfootage" or "geopolitics") controls which subreddit is processed. Set examples to True to generate a small table of examples. Set it to False to generate all the labels. The output is written to `results_geopolitics.csv` and `results_combatfootage.csv`. Note that cuda needs to be available. Without a GPU it theoretically possible to run this but it will take forever. If this is desired change the `device` argument of the pipeline to -1.

## Generating graphs
Run one of `Graph Positive Sentiment Comparison.py`, `Graph Sentiment Split Bars.py`, `Graph Sentiment-Upvote Matrix.py` or `Graph Upvote Distributions.py` to generate the corresponding graph. It will show up in a matplotlib interactive window.
