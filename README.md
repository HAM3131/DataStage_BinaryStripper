# README
This program exists to strip the compiled section of a DataStage `.dsx` file out, reducing file size for commits. Because DataStage stores the compiled version of a job in the same file as the source, files are much larger than necessary, requiring this solution.

# Arguments
* **Positional Arguments**
    * `filename`
        * Path of the target
* **Optional Arguments**
    * `-d, --delimiter`
        * Delimiter to strip all contents after. Defaults to 'BEGIN DSEXECJOB'
    * `-f, --force`
        * Force changes without confirmation messages
    * `-r, --recursive`
        * Strip directories and their contents recursively