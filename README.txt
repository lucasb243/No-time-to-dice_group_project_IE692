#############################################################################
##                                                                         ##
##  How to execute the code of our replication study on "No Time To Dice"  ## 
##                                                                         ##
#############################################################################

1. Relevant files for the execution of the code

    a. "learn_all.ipynb" is the only Jupyter Notebook, that is relevant for the execution of the code in order to replicate the author's original results. It also includes the results with the timezone Amsterdam. Graphs and visualizations of decision trees are created.
    Three sets of execution contexts are learned using slightly different event logs:
        1. the event log used and provided by the author
        2. recreated event log from base xes files with timezone Australia --> same results as using the authors event log
        3. recreated event log from base xes files with timezone Netherlands
    b. "learn_all 2019.ipynb" is the Jupyter Notebook that needs to be executed in order to see how the ODT Miner introduced by the authors performs on another event log (the one from the BPI Challenge 2019)

2. Relevant output files

    a. Most visual ouputs will automatically show up in the "learn_all.ipynb" or "learn_all 2019.ipynb" Jupyter Notebooks when they are being executed.
    b. The visualizations of the decision trees are stored to the seperate files "tree_paper.svg", "tree.svg" and "treebpic15_AEST.svg" in the folder "trees/".
    c. the event logs with added execution context (column: CO_rule) are stored in "data/added_execution_contexts"

3. Additional info for some files

    a. The "OrdinoR-dev/" folder contains a version of the OrdinoR package that is still in development. It was used because the current stable version does not include the ODTminer. The package was also further adjusted in this project.
    b. The base files are stored in "base_xes_files". These are then preprocessed and learned on in "learn_all.ipynb". They are saved in multiple version in the "data/" folder
    c. "tree.py" was created to visualize the decision trees. It is automatically used in "learn_all.ipynb"
    d. "bpic15_amended_typed" was the only event log in the authors repository. It contains the execution context in the column "CO". The readability of this is higher than in our files("data/added_execution_contexts") because the execution contexts were added manually.

4. If you are furthermore interested in the original code files by the authors of the paper "No Time To Dice", take a look at the following GitHub Repository: https://github.com/roy-jingyang/Org-Learn_Exe_Context 
