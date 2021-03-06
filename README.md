# Chemical Source Reduction (ChemSoR) Project

<hr/>

## 1. Overview

This a personal practical project which is under development. Its results would be published in a blogpost and not in a peer-review journal paper.

### 1.1. Project tree

Below you can see the current project tree.

```
├───data
│   ├───raw
│   |   └───.gitkeep
│   └───transformed
|       └───ChemSoR_database.db
|
├───models
|   └───__init__.py
|
├───notebooks
│   ├───1-jodhernandezbe-EDA.ipynb
|   ├───2-jodhernandezbe-data-enrichment.ipynb
|   ├───3-jodhernandezbe-modeling-without-prices-and-gdpbyindustry.ipynb
|   └───4-jodhernandezbe-modeling-with-prices-and-gdpbyindustry.ipynb
|
└───scripts
    ├───data_acquisition
    |   ├───__init__.py
    |   |───main.py
    |   |───extract.py
    |   |───srs_scraper.py
    |   |───nlm_scraper.py
    |   |───pubchem_scraper.py
    |   |───transform.py
    |   |───load.py
    |   |───base.py
    |   |───model.py
    |   |───common.py
    |   |───config.yaml
    |   |───chem_prices.csv
    |   |───database_schema.yaml
    |   |───TRI_File_2a_columns.txt
    |   └───columns_to_use.csv
    |
    └───model_deployment
        └───__init__.py
```

<hr/>

## 2. Requirements

In order to install the Python packages needed to run the tasks contained in the project, you must execute the following command in the Anaconda prompt.

```
conda env create -n ChemSoR -f environment.yml
```

<hr/>

## 3. Extract, Transform, and Load (ETL) pipeline (data engineering)

To obtain the file ChemSoR_database.db (SQLite database), you must navigate to the folder named data_acquisition and execute the following command:

```
python main.py
```
