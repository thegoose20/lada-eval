# Evaluating AI-Generated Linked Data

[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626.svg?style=flat&logo=Jupyter)](https://docs.jupyter.org/en/latest/) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgithub.com%2Fthegoose20%2Flada-eval/main) [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This repository contains Jupyter Notebooks that evaluate the syntax, completeness, and conformance of AI-generated linked data.  This evaluation work was completed from May through June 2025 for the project *[Building a sustainable future for anthropology's archives: Researching primary source data lifecycles, infrastructures, and reuse](https://ischool.umd.edu/projects/building-a-sustainable-future-for-anthropologys-archives-researching-primary-source-data-lifecycles-infrastructures-and-reuse/)*.

*This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].*

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

***
### Table of Contents

[Setup and Usage](#setup-and-usage)

[Files](#files)

[Related Resources](#related-resources)

***

## Setup and Usage

### Option 1

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


## Files
* `data-prep.ipynb`: a Jupyter Notebook that uses data in a CSV file to creates two individual data files per metadata record found in that CSV file: a TXT (Plain Text) file and either an XML (Extensible Markup Language) or JSON (JavaScript Object Notation) file.
* `evaluation-syntax.ipynb`: a Jupyter Notebook that evaluates whether the Dublin Core metadata records have correct XML syntax and whether Schema.org and CIDOC-CRM metadata records have correct JSON-LD syntax.
* `evaluation-completeness.ipynb`: a Jupyter Notebook that evaluates whether the metadata records have empty or unknown values in the data fields (depending on the metadata standard, a.k.a. 'types,' 'entities,' 'properties') and whether any URLs provided as values in data fields are valid and relevant URLs.
* `evaluation-conformance.ipynb`: a Jupyter Notebook that evaluates whethow well the Dublin Core metadata records adhere to the Dublin Core metadata standard, the Schema.org metadata records adhere to the Schema.org metadata standard, and the CIDOC-CRM metadata records adhere to the CIDOC-CRM metadata standard.
* `config.py`: variables for referencing data file locations used in this repo's Jupyter Notebooks
* `utils.py`: custom functions used in this repo's Jupyter Notebooks

## Related Resources
* D. Marsh, K. Fenlon. “Linking Analog Archival Data Across Scientific Disciplines: What’s Next?” Collections and Collecting Series, Consortium for the History of Science, Technology, and Medicine (CHSTM), online, December 1, 2023.
* D. Marsh. “Indigenizing Archival Discovery: Centering Communities in Research on Reparative Networks, Platforms, and Linked Data.” University of Michigan School of Information Series, “Data, Archives, Information, & Society” Series, Ann Arbor, MI, November 10, 2023.
* C. Emmelhainz, D. Marsh, M. Kamph. “[Structuring Visibility: Using Digitization and Linked Data to Amplify the Stories of Women in Science](https://www.youtube.com/watch?v=v7EeV0Tsc7Q).” American Philosophical Society “Women in Science: Opportunities,” Philadelphia, PA, October 6, 2023: https://www.youtube.com/watch?v=v7EeV0Tsc7Q (4:47).
* A. Sorensen, S. Lee, D.E. Marsh, K. Fenlon, R. Punzalan. 2023. “[Reviving anthropology's past: Digital archival access and ethical collaboration with Indigenous communities](https://rai.onlinelibrary.wiley.com/doi/10.1111/1467-8322.12847).” Anthropology Today 39(6): 11­–13.
* K. Fenlon, N. Wise, D. Marsh [“Linked Data and Anthropological Archives: Learning from Motives Across Disciplines](https://2024ld4.sched.com/event/1lCID/linked-data-and-anthropological-archives-learning-from-motives-across-disciplines).” LD4 Conference: Building Community for Linked Open Data, Online, October 8, 2024.
* D. Marsh, K. Fenlon, A. Sorensen, N. Wise. “[Primary Sources as Linked Data: Exploring Motives across the Sciences and Social Sciences](https://doi.org/10.1002/pra2.1023).” Proceedings of the Association for Information Science and Technology. Association for the Study of Information and Technology Studies, Calgary, AB, October 29, 2024.
* A. Sorensen, K. Fenlon, S. Buchanan, B. Anderson, C. Emmelhainz, D. Marsh, moderated by Lisa Cliggett, “Anthropology’s Archives: Linked Data and Crowdsourcing Technologies for Greater Access and Ethical Data Reuse.” Invited Session, American Anthropological Association Annual Meeting, Tampa, FL, November 21, 2024.
* D. Marsh “Indigenizing Archival Access: Centering Communities in Research on Reparative Location Systems, Platforms, & Linked Data Environments.” Public Lecture Series, Charles Sturt University, online, January 28, 2025.
* L. Havens, K. Fenlon, D. Marsh, N. Wise, U. Smoke, C. Navarrete, J. Sioui, D. Mantle, A. Sorensen. "Evaluating AI-Generated Linked Data."  LD4 2025 Conference: Linked Data in the Real World, Online, July 30, 2025.
* K. Fenlon, L. Havens, D. Marsh, N. Wise, U. Smoke, C. Navarrete, J. Sioui, D. Mantle, A. Sorensen. “Linked Data Workflows for Community Collections: Experiments with Open Access AI.” Proceedings of the Annual Meeting of the Association for Information Science and Technology, Washington, DC, November 14-18, 2025.