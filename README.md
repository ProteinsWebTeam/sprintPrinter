# sprintPrinter
A short script to create a PDF file to print the user stories from jira. 
The idea is that each Sprint master, can improve the script in the time between sprints.

Install
----
Execute the next commands, editing the path for python 2
```
git clone https://github.com/ProteinsWebTeam/sprintPrinter.git
cd sprintPrinter
virtualenv --python=/usr/bin/python venv
venv/bin/pip install -r requirements.txt
```

Usage
----
1. You need to have a TSV file that can be obtained from Jira. The columns of the file should be:
   
   *  Key 
   *  Component/s	
   *  Priority Code	
   *  Original Estimate	
   *  Assignee	
   *  Summary	
   *  Description
   
   Currently the TSV file can't have empty values.
   
2. Edit the file in the line ```178``` to specify the name of the path of the TSV file.
   And run  the script with:
   
   ```
   venv/bin/python sprint-pdf.py
   ```
3. The file ```sprint-stories.pdf``` should be created in the same path, you can then use it to print the stories.

Ideas to Improve
----
 * get the TSV file from the CLI
 * Support emty values in the TSV
 * Use the Jira API to get the file automatically.
