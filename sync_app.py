import logging
import time

from sync_files import parse_arguments, setup_logs, sync_folders

def main():

    args = parse_arguments() # process command-line arguments

    setup_logs(args.log_file) # pass the log file path obtained

    logging.info("Starting process")

    while True:
        try:
            sync_folders(args.source_folder, args.replica_folder)
            logging.info("Synchronization executed") 
            
        except Exception as e:
            logging.error(f"Synchronization failed: {e}")

        time.sleep(args.sync_interval)  # wait the determined time interval



if __name__ == "__main__":
    main()