import os
import shutil
import argparse
import logging
import hashlib

def parse_arguments():
    parser = argparse.ArgumentParser(description= "Synchronize Source and Replica Folders") #create the object for command-line interfaces

    # Define how each command-line argument should be parsed
    parser.add_argument("source_folder")
    parser.add_argument("replica_folder")
    parser.add_argument("sync_interval", type = int)
    parser.add_argument("log_file")

    return parser.parse_args()


def setup_logs(log_file):
    # Define the file path, level and message format (Timestamp and message)
    logging.basicConfig(filename=log_file,  level=logging.INFO,  format='%(asctime)s - %(message)s' )

    console_output = logging.StreamHandler() 
    console_output.setLevel(logging.INFO) 

    formatter = logging.Formatter('%(asctime)s - %(message)s') # define format of log messages on the output
    console_output.setFormatter(formatter)
    
    logging.getLogger().addHandler(console_output) # log messages will output both on the log file and console


def calculate_MD5(file_path):
    hash_md5 = hashlib.md5()

    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()
    
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error calculating MD5 for {file_path}: {e}")
        return None
    

   
def snapshot_source_folder(source_folder_path): # create a dictionary with file paths and MD5 hashes
    snapshot = {}
    for root, _, files in os.walk(source_folder_path):
        for file in files:
            source_file_path = os.path.join(root,file) # full path to the file in the source folder
            relative_path = os.path.relpath(source_file_path, source_folder_path) # path relative to the source folder
            md5_hash = calculate_MD5(source_file_path)
            snapshot[relative_path] = md5_hash

    return snapshot


def sync_new_files(snapshot, source_folder_path, replica_folder_path):
    for relative_path, md5_hash in snapshot.items(): #iterates through the dictionary
        source_file_path = os.path.join(source_folder_path, relative_path)
        replica_file_path = os.path.join(replica_folder_path, relative_path)

        if not os.path.exists(replica_file_path):
            logging.info(f"New file to copy: {relative_path}")
            os.makedirs(os.path.dirname(replica_file_path), exist_ok=True)
            shutil.copy2(source_file_path, replica_file_path)
            logging.info(f"Copied: {relative_path}")


def sync_updated_files(snapshot, source_folder_path, replica_folder_path):
    for relative_path, source_md5 in snapshot.items():
        source_file_path = os.path.join(source_folder_path, relative_path)
        replica_file_path = os.path.join(replica_folder_path, relative_path)

        if os.path.exists(replica_file_path):
            replica_md5 = calculate_MD5(replica_file_path)

            if source_md5 != replica_md5:
                logging.info(f"Update needed: {relative_path}")
                shutil.copy2(source_file_path, replica_file_path)
                logging.info(f"Updated: {relative_path}")
#            else:
#                logging.info(f"No update needed: {relative_path}")


def sync_deleted_files(snapshot, replica_folder_path):
    for root, _, files in os.walk(replica_folder_path):
        for file in files:
            replica_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(replica_file_path, replica_folder_path)

            if relative_path not in snapshot:
                logging.info(f"File no longer exists in source and should be deleted from replica: {relative_path}")
                os.remove(replica_file_path)
                logging.info(f"Removed: {relative_path}")


def sync_folders(source_folder_path, replica_folder_path):
    try:
        snapshot = snapshot_source_folder(source_folder_path)

        sync_new_files(snapshot, source_folder_path, replica_folder_path)
        sync_updated_files(snapshot, source_folder_path, replica_folder_path)
        sync_deleted_files(snapshot, replica_folder_path)

    except Exception as e:
        logging.error(f"Error synchronizing folders: {e}")
        raise Exception(f"Error synchronizing folders: {e}")


