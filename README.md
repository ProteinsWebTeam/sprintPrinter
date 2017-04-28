# sprintPrinter
A short script to create a PDF file to print the user stories from jira.
The idea is that each Sprint master, can improve the script in the time between sprints.

Install using Virtual env
----
Execute the next commands, editing the path for python 3
```
git clone https://github.com/ProteinsWebTeam/sprintPrinter.git
cd sprintPrinter
virtualenv --python=/usr/bin/python venv
venv/bin/pip install -r requirements.txt
```
Install using Conda
----
Execute the next commands, editing the path for python 3
```
git clone https://github.com/ProteinsWebTeam/sprintPrinter.git
cd sprintPrinter
conda create --name sprintprinter python=3.3.1 reportlab=3.2.0
source activate sprintprinter
#Test run
python3 sprint-pdf.py -i sprint_76.tsv -o test.pdf
```

Usage
----
1. You need to have a TSV file that can be obtained from from the xls provided by Jira. The columns of the file should be:

   *  Key
   *  Component/s
   *  Priority Code
   *  Original Estimate
   *  Assignee
   *  Summary
   *  Description

   Currently the TSV file can't have empty values.

2. Run the script with:

   ```
   venv/bin/python sprint-pdf.py -h
   ```

   It should display the help, you can tghen choose what you want to do

3. The file ```sprint-stories.pdf``` should be created in the same path, you can then use it to print the stories.

Ideas to improve:
----
 * get the input file from the CLI
 * Use the XML export instead of going through xls
 * Use the Jira API to get the file automatically.

Current bugs:
----
 * Unable to write output file to stdout
 * Breaks on empty fields
