# coding: utf-8
# author: Jing Li
# date: 2019/04/01
import os
import warnings
import pandas as pd
import numpy as np

# local directory to save files.
data_dir = "FAERSdata"
directoryPath = os.getcwd() + '/' + data_dir

# ignore warnings
warnings.filterwarnings('ignore')


def processDemo():
    for filename in os.listdir(directoryPath):
        if "DEMO" in filename.upper() and "TXT" in filename.upper():
            print("Process " + filename)
            demo_df = pd.read_csv(directoryPath + "/" + filename, low_memory=False, sep='$', error_bad_lines=False)

            # keep primaryid, caseid, age, sex, wt
            demo_df.drop(
                ['caseversion', 'i_f_code', 'lit_ref', 'event_dt', 'auth_num', 'fda_dt', 'age_grp', 'e_sub',
                 'rept_dt', 'to_mfr', 'reporter_country', 'mfr_dt', 'init_fda_dt', 'rept_cod', 'mfr_num',
                 'mfr_sndr', 'occp_cod', 'occr_country'], inplace=True, axis=1, errors='ignore')

            # process sex
            demo_df['sex'] = demo_df['sex'].fillna('UNK')
            sex_map = {'M': "0", 'F': "1", 'UNK': "2"}
            demo_df['sex'] = demo_df['sex'].map(sex_map)

            # process age
            demo_df = demo_df[pd.notnull(demo_df['age'])]
            # unified age unit
            demo_df = demo_df[demo_df.age_cod != 'dec'].reset_index(drop=True)
            demo_df['age'] = demo_df['age'].apply(pd.to_numeric, errors='coerce')
            demo_df['age'] = np.where(demo_df['age_cod'] == 'MON', demo_df['age'] * 1 / 12, demo_df['age'])  # mounth
            demo_df['age'] = np.where(demo_df['age_cod'] == 'WK', demo_df['age'] * 1 / 52, demo_df['age'])  # week
            demo_df['age'] = np.where(demo_df['age_cod'] == 'DY', demo_df['age'] * 1 / 365, demo_df['age'])  # day
            demo_df['age'] = np.where(demo_df['age_cod'] == 'HR', demo_df['age'] * 1 / 8760, demo_df['age'])  # hour
            demo_df = demo_df.drop(['age_cod'], axis=1)
            # age discretization and label encode
            # Newborn, Infant, Child Preschool, Child, Adolescent, Young Adult, Adult,Middle Aged, Aged, Aged+
            age_bins = [0, 1, 2, 5, 12, 18, 24, 44, 64, 79, 123]
            demo_df['age'] = pd.cut(demo_df.age, age_bins, labels=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            demo_df = demo_df.dropna(axis=0, subset=["age"])  # drop unreasonable age <0 or >123

            # process weight(wt)
            demo_df = demo_df[pd.notnull(demo_df['wt'])]
            # unified weight unit
            demo_df['wt'] = demo_df['wt'].apply(pd.to_numeric, errors='coerce')
            demo_df['wt'] = np.where(demo_df['wt_cod'] == 'LBS', demo_df['wt'] * 0.453592, demo_df['wt'])  # pounds
            demo_df['wt'] = np.where(demo_df['wt_cod'] == 'GMS', demo_df['wt'] * 0.001, demo_df['wt'])  # grams
            demo_df = demo_df.drop(['wt_cod'], axis=1)
            # weight discretization and label encode
            wt_bins = [0, 5, 10, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300]
            demo_df['wt'] = pd.cut(demo_df.wt, wt_bins, labels=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
            demo_df = demo_df.dropna(axis=0, subset=["wt"])  # drop unreasonable weight <0 or >300

            # save file
            demo_df.to_csv(directoryPath + "/" + filename[:-4] + '.csv', header=True, index=False)


def processDrug():
    for filename in os.listdir(directoryPath):
        if "DRUG" in filename.upper() and "TXT" in filename.upper():
            print("Process " + filename)
            drug_df = pd.read_csv(directoryPath + "/" + filename, low_memory=False, sep="$", error_bad_lines=False)

            # keep primaryid, caseid, role_cod, drugname
            drug_df.drop(
                ['drug_seq', 'val_vbm', 'dose_vbm', 'dose_form', 'dose_amt', 'dose_unit', 'cum_dose_chr', 'prod_ai',
                 'cum_dose_unit', 'dechal', 'rechal', 'lot_num', 'exp_dt', 'nda_num', 'route', 'dose_freq'],
                inplace=True, axis=1, errors='ignore')

            # process role_cod label encode
            drug_df = drug_df[pd.notnull(drug_df['role_cod'])]
            rolecod_map = {'PS': '0', 'SS': '1', 'C': '2', 'I': '3'}
            drug_df['role_cod'] = drug_df['role_cod'].map(rolecod_map)

            # process drugname
            drug_df = drug_df[pd.notnull(drug_df['drugname'])]
            drug_df['drugname'] = drug_df['drugname'].str.strip().str.lower()  # to lowercase
            drug_df = drug_df[~drug_df['drugname'].isin(['unknown'])]  # drop unknown
            drug_df['drugname'] = drug_df['drugname'].str.replace('\\', '/')  # fix slashes
            drug_df['drugname'] = drug_df['drugname'].map(
                lambda x: x[:-1] if str(x).endswith(".") else x)  # fix ending with period

            # save file
            drug_df.to_csv(directoryPath + "/" + filename[:-4] + '.csv', header=True, index=False)


def processReac():
    for filename in os.listdir(directoryPath):
        if "REAC" in filename.upper() and "TXT" in filename.upper():
            print("Process " + filename)
            reac_df = pd.read_csv(directoryPath + "/" + filename, low_memory=False, sep="$", error_bad_lines=False)

            # keep primaryid, caseid, pt
            reac_df.drop(['drug_rec_act'], inplace=True, axis=1, errors='ignore')

            # process pt
            reac_df = reac_df[pd.notnull(reac_df['pt'])]
            reac_df['pt'] = reac_df['pt'].str.strip().str.lower()  # to lowercase
            reac_df = reac_df[~reac_df['pt'].isin(['unknown'])]  # drop unknown
            reac_df['pt'] = reac_df['pt'].map(
                lambda x: x[:-1] if str(x).endswith(".") else x)  # fix ending with period

            # save file
            reac_df.to_csv(directoryPath + "/" + filename[:-4] + '.csv', header=True, index=False)


def processOutc():
    for filename in os.listdir(directoryPath):
        if "OUTC" in filename.upper() and "TXT" in filename.upper():
            print("Process " + filename)
            outc_df = pd.read_csv(directoryPath + "/" + filename, low_memory=False, sep="$", error_bad_lines=False)

            # process outc_cod
            outc_df = outc_df[pd.notnull(outc_df['outc_cod'])]
            outc_df = outc_df[outc_df['outc_cod'].isin(['DE', 'LT', 'HO', 'DS', 'CA', 'RI', 'OT'])]
            outccod_map = {'DE': '0', 'LT': '1', 'HO': '2', 'DS': '3', 'CA': '4', 'RI': '5', 'OT': '6'}
            outc_df['outc_cod'] = outc_df['outc_cod'].map(outccod_map)

            # save file
            outc_df.to_csv(directoryPath + "/" + filename[:-4] + '.csv', header=True, index=False)


def main():
    processDemo()
    processDrug()
    processReac()
    # processOutc()


if __name__ == '__main__':
    main()
