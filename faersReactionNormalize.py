# coding: utf-8
# author: Jing Li
# date: 2019/04/01
import os
import warnings
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime

# local directory to save files.
data_dir = "FAERSdataMerge"
directoryPath = os.getcwd() + '/' + data_dir

filename = "drugNorm.csv"  # file before process
savefile = 'drugReacNorm.csv'  # file after process

# ignore warnings
warnings.filterwarnings('ignore')


def main():
    print('Loading data...')
    # load file CONCEPT.csv
    concept_df = pd.read_csv("Norm/CONCEPT.csv", sep="\t", low_memory=False, error_bad_lines=False)
    concept_df.drop(
        ["domain_id", "vocabulary_id", "concept_class_id", "standard_concept", "concept_code", "valid_start_date",
         "valid_end_date", "invalid_reason"], inplace=True, axis=1, errors='ignore')
    concept_df = concept_df[pd.notnull(concept_df['concept_name'])]
    concept_df['concept_name'] = concept_df['concept_name'].str.strip().str.lower()

    # load file CONCEPT_SYNONYM.csv
    conceptSynonym_df = pd.read_csv("Norm/CONCEPT_SYNONYM.csv", sep="\t", low_memory=False, error_bad_lines=False)
    conceptSynonym_df.drop(["language_concept_id"], inplace=True, axis=1, errors='ignore')
    conceptSynonym_df = conceptSynonym_df[pd.notnull(conceptSynonym_df['concept_synonym_name'])]
    conceptSynonym_df['concept_synonym_name'] = conceptSynonym_df['concept_synonym_name'].str.strip().str.lower()

    # process
    print("Process " + filename + "\t" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # load file
    pt_df = pd.read_csv(directoryPath + "/" + filename, low_memory=False, error_bad_lines=False)

    pt_names = pt_df.drop_duplicates(subset='pt', keep='first')['pt']
    print("Total reaction names before normalization: " + str(pt_names.count()))
    for pt_name in tqdm(pt_names):
        pt_concept_df = concept_df[concept_df['concept_name'].isin([pt_name])]
        if not pt_concept_df.empty:
            pt_df.loc[pt_df.pt == pt_name, 'pt_id'] = pt_concept_df.iloc[0, 0]
        else:
            pt_conceptSynonym_df = conceptSynonym_df[
                conceptSynonym_df['concept_synonym_name'].isin([pt_name])]
            if not pt_conceptSynonym_df.empty:
                pt_df.loc[pt_df.pt == pt_name, 'pt_id'] = pt_conceptSynonym_df.iloc[0, 0]
            else:
                pt_df = pt_df[~pt_df['pt'].isin([pt_name])]

    pt_names = pt_df.drop_duplicates(subset='pt_id', keep='first')['pt_id']
    print("Total pt names after normalization: " + str(pt_names.count()))
    pt_df.drop(["pt"], inplace=True, axis=1, errors='ignore')

    # save file
    pt_df.to_csv(directoryPath + "/" + savefile, header=True, index=False)
    print("Process " + filename + " done.\t" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")


if __name__ == '__main__':
    main()
