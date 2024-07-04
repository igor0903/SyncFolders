#use "python setup.py /home/user/source /home/user/replica 60 /home/user/sync.log" to start
#the time unit is seconds

import os
import shutil
import time
import hashlib #to verify integrity
import argparse #to be able to read the arguments on command line
import logging #to prepare the log file

def setup_logging(log_file_path):
    # Set up logging to file and console
    logging.basicConfig(filename=log_file_path, level=logging.INFO,
                        format='%(asctime)s - %(message)s')
    logging.info("Logging started. Log file: " + log_file_path)

def calculate_md5(file_path):
    # Calculate MD5 checksum for a file to check if it's the same
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def synchronize_folders(source, replica):
    # Walk through the source directory
    for root, _, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, relative_path)

        # Create directories in replica if they don't exist
        if not os.path.exists(replica_root):
            os.makedirs(replica_root)
            logging.info(f"Created directory: {replica_root}")
            print(f"Created directory: {replica_root}")

        for file_name in files:
            source_file = os.path.join(root, file_name)
            replica_file = os.path.join(replica_root, file_name)

            # Check if file needs to be copied or updated
            if os.path.exists(replica_file):
                if calculate_md5(source_file) != calculate_md5(replica_file):
                    shutil.copy2(source_file, replica_file)
                    logging.info(f"Updated file: {replica_file}")
                    print(f"Updated file: {replica_file}")
            else:
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied file: {replica_file}")
                print(f"Copied file: {replica_file}")

    # Now, clean up replica directory: remove files/dirs not in source
    for root, _, files in os.walk(replica):
        relative_path = os.path.relpath(root, replica)
        source_root = os.path.join(source, relative_path)

        if not os.path.exists(source_root):
            shutil.rmtree(root)
            logging.info(f"Removed directory: {root}")
            print(f"Removed directory: {root}")
        else:
            for file_name in files:
                replica_file = os.path.join(root, file_name)
                source_file = os.path.join(source_root, file_name)

                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    logging.info(f"Removed file: {replica_file}")
                    print(f"Removed file: {replica_file}")

def main(source, replica, interval, log_file_path):
    setup_logging(log_file_path)
    while True:
        synchronize_folders(source, replica)
        logging.info(f"Synchronization complete. Next sync in {interval} seconds.")
        print(f"Synchronization complete. Next sync in {interval} seconds.")
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Synchronize two folders.')
    parser.add_argument('source', type=str, help='Source folder path')
    parser.add_argument('replica', type=str, help='Replica folder path')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, help='Log file path')
    args = parser.parse_args()

    main(args.source, args.replica, args.interval, args.log_file)
