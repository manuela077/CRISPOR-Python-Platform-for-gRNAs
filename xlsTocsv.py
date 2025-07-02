import os
import time
import pandas as pd

import os
import time

def get_latest_download(download_directory):
    # Wait a few seconds to ensure download finishes
    time.sleep(3)  # you can increase this if needed

    files = os.listdir(download_directory)
    paths = [os.path.join(download_directory, f) for f in files]

    # Get the latest modified file
    latest_file = max(paths, key=os.path.getmtime)
    return latest_file

def convert(download_dir, filename):

    # Load the .xls file (you can also use .xlsx the same way)
    df = pd.read_excel(get_latest_download(download_dir), sheet_name=0)  # or specify sheet name

    # Save it as a .csv file
    df.to_csv(filename+".csv", index=False)