# Phase I — Bioactivity & Toxicity Prediction

Screens chemical compounds against **acetylcholinesterase (AChE)**, the enzyme implicated in the cholinergic decline seen in Alzheimer's disease. Given a set of SMILES strings, this stage predicts how potently each compound inhibits AChE and whether it is likely to be toxic.

Its output — a shortlist of bioactive, low-toxicity scaffolds — is what Phase II generates from.

## How it works

```
SMILES input (.txt)
   ├── PaDEL-Descriptor ──▶ PubChem fingerprints (881-bit) ──▶ regression ──▶ pIC50
   └── RDKit ──▶ Lipinski descriptors (MW, LogP, HBD, HBA) ──▶ classification ──▶ toxicity
```

**pIC50** is the negative log of IC50 — higher means more potent. Following a Mann–Whitney U test on the ChEMBL data, compounds are labelled *active* above pIC50 6 and *inactive* below 5.

## Models

Ten regressors were compared for bioactivity: Decision Tree, Linear, Ridge, ExtraTrees, ExtraTree, Bagging, XGBoost, AdaBoost, KNeighbors and Random Forest.

| | Winner | Train R² | Test R² |
|---|---|---|---|
| Bioactivity (pIC50) | Random Forest Regressor | 0.943 | 0.649 |
| Toxicity | Extra Trees Classifier | — | — |

The gap between train and test R² is a real overfit — the model memorises fingerprint patterns. Treat predictions as a ranking signal for triage, not as calibrated potency estimates.

## Contents

```
app.py                          Streamlit interface
bioactivity_prediction.ipynb    Data curation, model comparison, training
PaDEL-Descriptor/               Vendored PaDEL tool + PubChem fingerprint config
descriptor_list.csv             Feature subset retained after selection
example_acetylcholinesterase.txt  Sample input
requirements.txt
```

## Setup

Java is required — PaDEL-Descriptor is a JAR, invoked as a subprocess.

```bash
java -version    # need JRE 8 or later

conda create -n pharmaicist-p1 python=3.9 -y
conda activate pharmaicist-p1
conda install -c conda-forge rdkit -y
pip install -r requirements.txt
```

## Required: the trained model file

`app.py` loads `acetylcholinesterase_model.pkl` from this directory. **That file is not in the repository** — it exceeded what was committed originally.

You have two options:

1. Obtain the pickle from the original project archive and drop it in this folder.
2. Regenerate it by running `bioactivity_prediction.ipynb` end to end, which refits the Random Forest on the ChEMBL CHEMBL220 data and writes the pickle out.

Option 2 is the safer one — a pickle is tied to the scikit-learn version that produced it, and an old one may fail to deserialise.

## Running

```bash
streamlit run app.py
```

Upload a `.txt` file of SMILES strings (see `example_acetylcholinesterase.txt` for the format — one SMILES and one identifier per line, tab-separated). The app computes descriptors, predicts pIC50, assigns activity classes, and offers the results as a CSV download.

The PaDEL step writes `molecule.smi` and `descriptors_output.csv` into the working directory during a run. Both are gitignored.

## Data

- **ChEMBL** — bioactivity for target CHEMBL220 (human acetylcholinesterase). Roughly 15M activity records across 1.9M compounds overall; the AChE subset is what's used here.
- **Tox21 / TOXNET** — toxicity labels, including HSDB and CCRIS.

## Notes

`requirements.txt` as originally committed listed stdlib modules (`os`, `pickle`) as pip packages and omitted several real dependencies. If you hit import errors, the actual runtime needs: `streamlit`, `pandas`, `numpy`, `pillow`, `rdkit`, `mols2grid`, `scikit-learn`.
