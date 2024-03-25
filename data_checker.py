import os
import sys
import pandas as pd


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ex: python data_checker.py path/to/directory")
        sys.exit(1)

    directory_path = sys.argv[1]
    
    total_files = 0
    total_size = 0
    
    for root, dirs, files in os.walk(directory_path):
        num_files = len(files)
        dir_size = sum(os.path.getsize(os.path.join(root, name)) for name in files)
        
        total_files += num_files
        total_size += dir_size
        
        print(f"{root}, number of files: {num_files}, size: {dir_size} bytes")
    
    print("")
    print("Total within the specified directory")
    print(f"Total number of files: {total_files}")
    print(f"Total file size: {total_size} bytes")