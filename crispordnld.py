from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import argparse
import pandas as pd
import xlsTocsv as xtc

import os
import time

#read fasta file as a string
def read_fasta_as_string(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Skip header line (starts with >) and join the rest
    sequence = ''.join(line.strip() for line in lines if not line.startswith('>'))
    return sequence


def crisporDownload(fasta, genome, fileName):
    fastaSeq=read_fasta_as_string(fasta)

    # Set up download directory
    download_dir = os.path.abspath("crispor_downloads")
    os.makedirs(download_dir, exist_ok=True)

    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://crispor.gi.ucsc.edu/")

        # Fill in sequence and genome
        sequence_box = driver.find_element(By.NAME, "seq")
        sequence_box.clear()
        sequence_box.send_keys(fastaSeq)

        #press tab button to exit from the text box to go to the next
        sequence_box.send_keys(Keys.TAB) 
        
        # seq_input.send_keys(Keys.TAB)
        time.sleep(0.5)  # Give time for focus change

        # 3. DOWN arrow to open dropdown
        from selenium.webdriver.common.action_chains import ActionChains

        ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(0.3)

        # 4. Type the name (starts searching in dropdown)
        ActionChains(driver).send_keys(genome).perform()
        time.sleep(0.3)

        # 5. Press ENTER to select
        ActionChains(driver).send_keys(Keys.ENTER).perform()

        #6: press the submit button
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()


        # Wait for the results page to load and show the download link

        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "guideTableDiv")))

        download_link = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Guides, all scores"))
        )
        download_link.click()
        print("Download started...")

        # Wait for the download to complete
        time.sleep(10)

    finally:
        driver.quit()
        print(f"Done. Check your download in: {download_dir}")
        xtc.convert(download_dir, fileName)


#get inputs from arguments        
# def getInputs():
#     parser = argparse.ArgumentParser(
#         description="Download csv file from CRISPOR website, given Fasta file, name of genome, and download directory"
#     )
#     parser.add_argument("fasta_file", help="Path to input fasta file")
#     parser.add_argument(
#         "--name", type=str, default="Mus musculus - Mouse (reference) - UCSC Dec. 2011 (mm10=C57BL/6J) + SNPs: C57BL/10J, C57BR/cdJ",
#         help="name of the genome to search in, using keywords on the dropdown menu"
#     )
#     parser.add_argument(
#         "--output", type=str,
#         help="Download directory of final .xsl spreadsheet and .csv data"
#     )
#     args = parser.parse_args()

#     return (args.fasta_file, args.name, args.output)

# crisporDownload(getInputs())