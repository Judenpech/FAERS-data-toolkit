# FAERS Data Toolkit

This repository contains some script tools to download and process  [FDA Adverse Event Reporting System **(FAERS)**](https://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/) ASCII dataset. The toolkit uses [FAERS data files](https://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm082193.htm) which is available online. 



## What can FAERS Data Toolkit do?

- Get all FAERS/AERS data files download link and save them to a txt file.

- Download all(2004Q1-now) FAERS/AERS data files and delete unwanted files(you can customize this).

- Data preprocess(DEMO, DRUG, REAC, OUTC in FAERS data files only). See [script](https://github.com/jl223vy/FAERS-data-toolkit/blob/master/faersPreprocess.py) for more information.

- Merge all DEMO, DRUG, REAC/OUTC into a CSV file.

- Standardize DRUGNAME and generate the unique DRUG_ID using [RxNorm RESTful Web API](<https://rxnav.nlm.nih.gov/RxNormAPIREST.html>) to get approximate match. The other way is standardize DRUGNAME to [OHDSI OMOP Common Data Model (CDM)](<https://www.ohdsi.org/>) and generate the unique DRUG_ID.

- Standardize PT to  [OHDSI OMOP Common Data Model (CDM)](<https://www.ohdsi.org/>) and generate the unique PT_ID.

## How to use FAERS Data Toolkit?

  Simply download or fork this repository, and run scripts below.

- **faersDownloader.py**

  FAERS/AERS data files download link is saved in local **FaersFilesWebUrls.txt** file.

  The source data files are saved in the local **FAERSsrc**(automatically generated) folder.

  The data files are saved in the local **FAERSdata**(automatically generated) folder.

  **PS:** Run **faersDownloader_backup.py** if you request too much times and get blocked by FDA :(

- **faersPreprocess.py**

  The data files after preprocess are saved in the local **FAERSdata** folder.

- **faersDataMerge.py**

  The merged file is named **faersDataLightGBM.csv** and saved in **FAERSdataMerge**(automatically generated) folder.

- **faersDrugNormalize.py**

  The file after DRUGNAME standardized process is named **drugNorm.csv** and saved to **FAERSdataMerge** folder.

  **Requirements:** Download **CONCEPT.csv** and **CONCEPT_SYNONYM.csv** from [OHDSI OMOP Common Data Model (CDM)](<https://www.ohdsi.org/>) , and keep them in **Norm** folder.

- **faersReactionNormalize.py**

  The file after PT standardized process is named **drugReacNorm.csv** and saved to **FAERSdataMerge** folder.

  **Requirements:** Download **CONCEPT.csv** and **CONCEPT_SYNONYM.csv** from [OHDSI OMOP Common Data Model (CDM)](<https://www.ohdsi.org/>) , and keep them in **Norm** folder.

  



