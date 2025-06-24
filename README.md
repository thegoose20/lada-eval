# Evaluating AI-Generated Linked Data

This repository contains Jupyter Notebooks that evaluate the syntax, completeness, and conformance of AI-generated linked data.  This evaluation work was completed from May through June 2025 for the project *[Linking Anthropology's Data and Archives]()*.

***
### Table of Contents

[Setup and Usage](#setup-and-usage)

[Data and Files](#data-and-files)

[Related Resources](#related-resources)

***

## Setup and Usage

### Option 1
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgithub.com%2Fthegoose20%2Flada-eval/main)

The Jupyter Notebooks can be run in a web browser with [Binder](https://mybinder.org/v2/git/https%3A%2F%2Fgithub.com%2Fthegoose20%2Flada-eval/main).  The advantage of using Binder is that you do not need to install any software to run the Notebooks.  Please note that when using Binder, any changes you make to the code will not be saved after you close the Binder webpage, but you can download data files that the code generates in Binder to save them to your own computer.  You can also upload your own data files to Binder to have the Jupyter Notebooks analyze those.

### Option 2
Alternatively, you can follow the steps below to clone the GitHub repository (repo), which creates a copy of all the code to your computer so you can run it from your computer rather than through Binder.  This way, you can save any changes you make to the code, and any data files and error reports you create will automatically be saved to your computer.

**Step 1:** Using your command line, navigate to the folder in which you'd like to save a copy of the repo's code and then clone the repo.

*If you're not familiar with command line tools, check out [this Bash tutorial](https://programminghistorian.org/en/lessons/intro-to-bash) (for Mac and Linux) or [this PowerShell tutorial](https://programminghistorian.org/en/lessons/intro-to-powershell) (for Windows) from the Programming Historian.*

```
git clone https://github.com/thegoose20/lada-eval.git
```

**Step 2:** Navigate into the repo.

```
cd lada-eval
```

**Step 3:** Create a virtual environment from the environment file:

*Note: We recommend using **conda** rather than pip.  You can install Miniconda or the Anaconda Distribution, but if you don't already have [Jupyter](https://jupyter.org/) installed, we recommend installing the **Anaconda Distribution**, because this includes Jupyter, which you'll need to run the code in this repo (the files with the extension `.ipynb` are Jupyter Notebooks).  Otherwise, you'll need to [install Jupyter](https://anaconda.org/anaconda/jupyter) after installing Miniconda.  If you don't already have conda installed, follow the [instructions here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).  You may also want to check out the "[Getting started with conda](https://docs.conda.io/projects/conda/en/stable/user-guide/getting-started.html)" guide.*

```
conda env create -f environment.yml
```

**Step 4:** Activate your newly created virtual environment (you can find the name of the environment, `ldeval`, at the top of the environment file).
```
conda activate ldeval
```

**Step 5:** Initialize the git repository.  

*If you're not familiar with git or GitHub, checkout GitHub's [Quick Start](https://docs.github.com/en/get-started/start-your-journey) and [Using Git](https://docs.github.com/en/get-started/using-git) documentation.*
```
git init
```

Now you're ready to begin running the Jupyter Notebooks in this repo!  You can run the Notebooks using Project Jupyter's Jupyter Lab or Jupyter Notebook platforms, or using an IDE such as [Visual Studio](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).  If you installed the Anaconda Distribution, open the Anaconda application (the logo is a green circle) and then click on Jupyter (the logo is an orange circle).  

When you're done working, shut down the virtual environment by entering the following in the command line:
```
conda deactivate
```

When you want to return to working with this code, re-activate the virtual environment by running the command in step 4.


## Data and Files
* `data-prep.ipynb`: a Jupyter Notebook that uses data in a CSV file to creates two individual data files per metadata record found in that CSV file: a TXT (Plain Text) file and either an XML (Extensible Markup Language) or JSON (JavaScript Object Notation) file.
* `evaluation-syntax.ipynb`: a Jupyter Notebook that evaluates whether the Dublin Core metadata records have correct XML syntax and whether Schema.org and CIDOC-CRM metadata records have correct JSON-LD syntax.
* `evaluation-completeness.ipynb`: a Jupyter Notebook that evaluates whether the metadata records have empty or unknown values in the data fields (depending on the metadata standard, a.k.a. 'types,' 'entities,' 'properties') and whether any URLs provided as values in data fields are valid and relevant URLs.
* `evaluation-conformance.ipynb`: a Jupyter Notebook that evaluates whethow well the Dublin Core metadata records adhere to the Dublin Core metadata standard, the Schema.org metadata records adhere to the Schema.org metadata standard, and the CIDOC-CRM metadata records adhere to the CIDOC-CRM metadata standard.
* `correction-dc-xml.ipynb`: a Jupyter Notebook that attempts to automatically correct errors found in the Dublin Core (DC) XML files during evaluation, and exports a report about which errors were corrected, which remain, and any new errors found.
* `correction-sdo-cidoc-json.ipynb`: a Jupyter Notebook that attempts to automatically correct errors found in the Schema.org and CIDOC-CRM records found during evaluation, and exports a report about which errors were corrected, which remain, and any new errors found.
* `wikidata-integration.ipynb`: a Jupyter Notebook that attempts to reconcile the metadata records with existing (and relevant!) Wikidata records.
* `data/`: this folder contains the source data file from which additional files are made (two per metadata record: a TXT file and either a JSON or XML file), as well as the data files generated by the code in the repo's Jupyter Notebooks
* `data/error_reports`: this folder contains CSV files of evaluation reports generated by the repo's Jupyter Notebooks, specifically by the `evaluation-syntax.ipynb`, `evaluation-completeness.ipynb`, and `evaluation-conformance.ipynb` files

## Related Resources
* [ADD: previous project publications]
* [Anything else???]