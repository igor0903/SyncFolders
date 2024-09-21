# SyncFolders - Python Script
Script to sync a folder and make a backup replica that stay updated 

## Features

   #### - One-way synchronization: The replica folder is updated to match the source folder.
   #### - Periodic synchronization: Synchronization is performed at regular intervals.
   #### - Logging: All file operations (creation, copying, removal) are logged to a file and displayed on the console.
   #### - Command-line arguments: Folder paths, synchronization interval, and log file path are provided via command-line arguments.

## Command to use

### python setup.py /path/to/source /path/to/replica <interval_in_seconds> /path/to/logfile.log
