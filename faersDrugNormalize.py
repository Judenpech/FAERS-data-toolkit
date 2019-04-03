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

filename = "faersDataLightGBM.csv"  # file before process
savefile = 'drugNorm.csv'  # file after process

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
    drug_df = pd.read_csv(directoryPath + "/" + filename, low_memory=False, error_bad_lines=False)

    drug_names = drug_df.drop_duplicates(subset='drugname', keep='first')['drugname']
    print("Total drug names before normalization: " + str(drug_names.count()))
    for drug_name in tqdm(drug_names):
        drug_concept_df = concept_df[concept_df['concept_name'].isin([drug_name])]
        if not drug_concept_df.empty:
            drug_df.loc[drug_df.drugname == drug_name, 'drug_id'] = drug_concept_df.iloc[0, 0]
        else:
            drug_conceptSynonym_df = conceptSynonym_df[
                conceptSynonym_df['concept_synonym_name'].isin([drug_name])]
            if not drug_conceptSynonym_df.empty:
                drug_df.loc[drug_df.drugname == drug_name, 'drug_id'] = drug_conceptSynonym_df.iloc[0, 0]
            else:
                drug_df = drug_df[~drug_df['drugname'].isin([drug_name])]

    drug_names = drug_df.drop_duplicates(subset='drug_id', keep='first')['drug_id']
    print("Total drug names after normalization: " + str(drug_names.count()))
    drug_df.drop(["drugname"], inplace=True, axis=1, errors='ignore')

    # # call RxNorm RESTful Web API to get approximate match
    # drug_names = drug_df.drop_duplicates(subset='drugname', keep='first')['drugname']
    # for drug_name in tqdm(drug_names):
    #     url = "https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term={" + str(drug_name) + "}&maxEntries=1"
    #     res = requests.get(url).json()
    #     candidate = res['approximateGroup'].get('candidate')
    #     if candidate:
    #         drug_df.loc[drug_df.drugname == drug_name, 'rxcui'] = candidate[0]['rxcui']
    #
    # drug_names = drug_df.drop_duplicates(subset='rxcui', keep='first')['rxcui']
    # print("Total drug names after normalization: " + str(drug_names.count()))

    # save file
    drug_df.to_csv(directoryPath + "/" + savefile, header=True, index=False)
    print("Process " + filename + " done.\t" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")


if __name__ == '__main__':
    main()
