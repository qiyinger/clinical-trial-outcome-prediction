# HINT: Hierarchical Interaction Network for Predicting Clinical Trial Approval Probability

This repository hosts HINT, a deep learning based method for clinical trial approval prediction. 
The repository can be mainly divided into two parts:
- `benchmark` describes the process of curating benchmark dataset named **Trial Approval Prediction (TAP)** for clinical trial approval prediction. 
- `HINT` is the Hierarchical Interaction Network, a deep learning based method. 


The following figure illustrates the pipeline of HINT. 

<p align="center"><img src="./HINT/hint.png" alt="logo" width="810px" /></p>



## Table Of Contents 

- Installation
- Benchmark
  - Raw Data 
    - clinicaltrial.gov
    - DrugBank
    - MoleculeNet 
  - Data Curation Process
    - Collect all the records
    - diseases to icd10 
    - drug to SMILES 
    - ICD-10 code hierarchy
    - Sentence Embedding for trial protocol 
    - Selection of clinical trial
    - Data split 
    - Statistics of Dataset 
- HINT: Learn and Inference 
  - Phase I/II/III prediction
  - Indication prediction 
  - Tutorial (Jupyter Notebook)
- Contact 

--- 

## Installation

We build conda environment and uses `conda` or `pip` to install the required packages. See `conda.yml` for all the packages. 

```bash
conda create -n predict_drug_clinical_trial python==3.7 
conda activate predict_drug_clinical_trial 
conda install -c rdkit rdkit  
pip install tqdm scikit-learn 
pip install torch
pip install seaborn 
pip install scipy
pip install icd10-cm
```

We use following command to activate conda environment. 
```bash
conda activate predict_drug_clinical_trial
```

---

## Benchmark

To standardize the clinical trial approval prediction, we create a benchmark dataset for Trial Approval Prediction named TAP, which incorporate rich data components about clinical trials, including drug, disease and protocol (eligibility criteria). 
All the scripts are in the folder `benchmark`. 
Please see `benchmark/README.md` for details. 

---

## HINT: Learn and Inference 

After processing the data, we learn the Hierarchical Interaction Network (HINT) on the following four tasks. The following figure illustrates the pipeline of HINT. All the scripts are available in the folder `HINT`. 
Please see `HINT/README.md` for details. 



## Contact

Please contact futianfan@gmail.com for help or submit an issue. This is a joint work with [Kexin Huang](https://www.kexinhuang.com/), [Cao(Danica) Xiao](https://sites.google.com/view/danicaxiao/), Lucas M. Glass and [Jimeng Sun](http://sunlab.org/). 


















