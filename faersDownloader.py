# coding: utf-8
# author: Jing Li
# date: 2019/04/01

import os
import re
import lxml
import time
import shutil
import warnings
import requests
from tqdm import tqdm
from io import BytesIO
from zipfile import ZipFile
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

# this script will find target in this list pages.
target_page = ["https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html"]

# local directory to save files.
source_dir = "FAERSsrc"
data_dir = "FAERSdata"

# ignore warnings
warnings.filterwarnings('ignore')


def downloadFiles(faers_files, source_dir, data_dir):
    """
    download faers data files.
    :param faers_files: dict faers_files = {"name":"url"}
    :param source_dir: FAERSsrc
    :param data_dir: FAERSdata
    :return: none
    """
    for file_name in tqdm(faers_files):
        try:
            print("Download " + file_name + "\t" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            r = requests.get(faers_files[file_name], timeout=200)
            z = ZipFile(BytesIO(r.content))
            z.extractall(source_dir)
            r.close()

            # delete and copy files to FAERSdata.
            deleteUnwantedFiles(source_dir)
            copyFiles(source_dir, data_dir)
            print("Download " + file_name + " success!\t" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            print("Download " + file_name + " failed! Error: " + str(e))
        print("Sleep 30 seconds before starting download a new file.\n")
        time.sleep(30)


def deleteUnwantedFiles(path):
    """
    delete unwanted files.
    :param path: FAERSsrc
    :return: none
    """
    print("Delete unwanted files.\t" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for parent, dirnames, filenames in os.walk(path):
        for fn in filenames:
            # FDA Adverse Event Reporting System (FAERS) began 2012Q4.
            # keep data from 2012Q4 and after.
            if fn[4:8] < "12Q4":
                print("Delete " + fn)
                os.remove(os.path.join(parent, fn))
            if fn.lower().endswith('.pdf') or fn.lower().endswith('.doc'):
                print("Delete " + fn)
                os.remove(os.path.join(parent, fn))
            elif fn.upper().startswith(("RPSR", "INDI", "THER", "SIZE", "STAT", "OUTC")):
                print("Delete " + fn)
                os.remove(os.path.join(parent, fn))
    print("Delete unwanted files done!\t" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def copyFiles(source_dir, data_dir):
    """
    Copy files from FAERSsrc to FAERSdata.
    :param source_dir: FAERSsrc
    :param data_dir: FAERSdata
    :return: none
    """
    print("Copy files from " + source_dir + " to " + data_dir + ".    ", end="")
    RootDir = os.getcwd() + '/' + source_dir
    TargetFolder = os.getcwd() + '/' + data_dir
    for root, dirs, files in os.walk((os.path.normpath(RootDir)), topdown=False):
        for name in files:
            if name.lower().endswith('.txt'):
                SourceFolder = os.path.join(root, name)
                shutil.move(SourceFolder, TargetFolder)
    print("Done! ")


def getFilesUrl():
    """
    find all web urls in target page.
    :return: dict files = {"name":"url"}
    """
    print("Get web urls.\t")
    files = {}
    for page_url in target_page:
        try:
            request = urlopen(page_url)
            page_bs = BeautifulSoup(request, "lxml")
            request.close()
        except:
            request = urlopen(page_url)
            page_bs = BeautifulSoup(request)
        for url in page_bs.find_all("a"):
            a_string = str(url)
            if "ASCII" in a_string.upper():
                t_url = url.get('href')
                files[str(url.get('href'))[-16:-4]] = t_url

    # save urls to FaersFilesWebUrls.txt
    save_path = os.getcwd() + "/FaersFilesWebUrls.txt"
    if (os.path.exists(save_path)):
        os.remove(save_path)
    with open(save_path, 'a+') as f:
        for k in files.keys():
            f.write(k + ":" + files[k] + "\n")

    print("Done!")
    return files


def main():
    # creating the source directory if not exits.
    if not os.path.isdir(source_dir):
        os.makedirs(source_dir)
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    # get faers data file's url and download them.
    faers_files = getFilesUrl()
    downloadFiles(faers_files, source_dir, data_dir)


if __name__ == '__main__':
    main()
