# File Synchronization Test Task

This program has the objective to synchronize two folders, a source and a replica. If a file is added, edited or deleted from the source folder, then, after a time interval selected by the user, the same operation happens to the file on the replica folder. 

## Code explanation

The objective was to provide to the console the folder paths, the synchronization interval and the log file path. For that, I implemented a parser function called ``` "parse_arguments" ```. 

For the synchronization of the files, I started by creating a snapshot function called ```snapshot_source_folder```. This function creates a snapshot of the source folder by generating a dictionary. This dictionary contains the relative paths of all files in the source folder as keys and their respective MD5 hashes as values. This will be used to compare the current state of the source with the replica folder.

After that, for the synchronization logic, I implemented a function for each fold action (new, update and delete). The ```sync_new_files``` function verifies if the file does not exist in the replica folder, then it logs the action, ensures the directory structure exists in the folder and copies the file from the source to the replica folder.
The ```sync_updated_files``` function verifies if the file exists in the replica folder and then calculates the MD5 of the file. Then it verifies if the MD5 is different, and if so, it logs the action and then updates the replica file to match the source file.
The ```sync_deleted_files``` verifies if the replica file is in snapshot dictionary, and if not, it logs the action and deletes the replica file.

## Code Execution

To run the code type these commands:

```bash
pip install -r requirements.txt
```
Version of python used: python 3.7.9
```bash
python sync_app.py ./Source_Folder ./Replica_Folder 10 ./Log_File.log
```
Where, ./Source_Folder and ./Replica_Folder are the folder paths; 10 is the time interval between synchronizations, in seconds and ./Log_File is log file path, where the name can be changed.

## Unit Tests

The Unit Tests will test if the functions are working as expected. These tests will generate temporary folders with temporary files, that after the test execution disappear. They will test if the new file in the replica exists; if the file in the replica folder was updated and if the file in the replica was deleted.


## Unit Tests Execution

To run the  unit tests type this command: 

```bash
pytest test_sync_files.py
```
