import os
import shutil
import argparse
import logging

# by Dan-Armand Stancu 
# it is laso compatible with online IDE's (ex.: Replit)
def sync_folders(source_folder, replica_folder, log_file):
  # Create replica folder if it doesn't exist
  if not os.path.exists(replica_folder):
    os.makedirs(replica_folder)

  # Configure logging to log file and console
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler(log_file),
              logging.StreamHandler()])

  # Iterate over files and subfolders in the source folder
  for root, dirs, files in os.walk(source_folder):
    # Determine the relative path in the source folder
    relative_path = os.path.relpath(root, source_folder)

    # Create the corresponding folder in the replica folder
    replica_path = os.path.join(replica_folder, relative_path)
    if not os.path.exists(replica_path):
      os.makedirs(replica_path)

    # Copy files from source to replica folder
    for file in files:
      source_file = os.path.join(root, file)
      replica_file = os.path.join(replica_path, file)

      # Copy the file if it doesn't exist in the replica folder or it's different
      if not os.path.exists(replica_file) or \
         os.path.getmtime(source_file) > os.path.getmtime(replica_file):
        shutil.copy2(source_file, replica_file)
        logging.info(f"Copied file: {source_file} to {replica_file}")

    # Delete files in the replica folder that no longer exist in the source folder
    replica_files = set(os.listdir(replica_path))
    source_files = set(files)
    for file in replica_files - source_files:
      file_path = os.path.join(replica_path, file)
      if os.path.isfile(file_path):
        os.remove(file_path)
        logging.info(f"Deleted file: {file_path}")


# Parse command line arguments
parser = argparse.ArgumentParser(description='Folder synchronization program')
parser.add_argument('source_folder', help='Path to the source folder')
parser.add_argument('replica_folder', help='Path to the replica folder')
parser.add_argument('log_file', help='Path to the log file')
args = parser.parse_args()

# Example usage
source_folder = args.source_folder
replica_folder = args.replica_folder
log_file = args.log_file

sync_folders(source_folder, replica_folder, log_file)

#To run the program, you can use the command line and provide the necessary arguments:

#python sync_folders.py /path/to/source/folder /path/to/replica/folder /path/to/log/file.log

#Replace sync_folders.py, /path/to/source/folder, /path/to/replica/folder, and /path/to/log/file.log with the actual filenames and paths for your situation.

#This  code uses the argparse module to parse command line arguments for the source folder, replica folder, and log file. It configures logging to log both to the specified log file and to the console. File operations (copying and deletion) are logged using the logging.info() function.

#Now, when you run the program, it will synchronize the folders and log the file operations to both the specified log file and the console output.
