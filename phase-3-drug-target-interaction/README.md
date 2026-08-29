# 🔗 Phase III: Drug-Target Interaction Prediction

Predicts whether a given drug-protein pair binds. Where Phase II produces candidate molecules, this stage asks whether they will actually engage their intended target, and flags unintended interactions that could cause side effects.

Delivered as a multi-page Streamlit application.

## 🔬 How it works

The core idea is that a drug-target pair can be represented as a concatenation of two feature vectors, turning binding into a binary classification problem over that joint representation.

```
Drug (SMILES)          Protein (UniProt)
     │                        │
     ▼                        ▼
PubChem fingerprint    ┌──────┴──────┐
  (via PaDEL)          │             │
     │            sequence      AlphaFold
     │            embedding    3D structure
     │                 │             │
     │                 └──────┬──────┘
     │                        │
     └────────► concatenate ◀─┘
                     │
                     ▼
          feature selection → classifier → binds / does not bind
```

Two model families are trained for comparison:

- 🔹 **Baseline models**, using drug fingerprints plus basic QSAR descriptors only.
- 🔸 **Enhanced models**, adding protein sequence and AlphaFold-derived structure embeddings.

The baseline/enhanced split is the experiment: does structural information about the target improve binding prediction over chemistry alone?

## 📊 Results

Classifiers evaluated: Dummy, Logistic Regression, Linear SVC, K-Nearest Neighbours, Decision Tree, Random Forest, and SGD.

Test set (740 DTIs held out):

| Model | Accuracy | Precision | Recall | F1 | MCC |
|---|---|---|---|---|---|
| Dummy | 0.68 | 0.68 | 1.00 | 0.81 | 0.00 |
| Logistic Regression | 0.72 | 0.73 | 0.92 | 0.82 | 0.28 |
| Linear SVC | 0.72 | 0.77 | 0.85 | 0.80 | 0.32 |
| K-Nearest Neighbours | 0.75 | 0.79 | 0.86 | 0.82 | 0.40 |
| Decision Tree | 0.62 | 0.74 | 0.69 | 0.71 | 0.17 |
| 🏆 **Random Forest** | **0.76** | **0.77** | **0.92** | **0.84** | **0.41** |
| SGD | 0.73 | 0.75 | 0.92 | 0.82 | 0.31 |

Training set: 99,705 DTIs.

⚠️ **Read the MCC column, not the accuracy column.** The dummy classifier, which predicts the majority class for everything, reaches 68% accuracy and 0.81 F1. Random Forest's 76% is an 8-point lift on a badly imbalanced problem. Matthews correlation coefficient accounts for that imbalance, and 0.41 is a moderate signal rather than a strong one.

## 📁 Contents

```
Home.py                          Streamlit entry point / project overview
pages/
  2_Embeddings.py                Protein embedding exploration
  3_Classification_Models.py     Model comparison, metrics, interpretability
utils/
  page_helpers.py                Shared Streamlit layout
  model_prediction_helpers.py    Inference
  model_interpretability_helpers.py  LIME / ELI5 explanations
data/
  Datasets/                      Curated DTI data, protein embeddings
  Baseline_Models/               Trained baseline classifiers (.joblib)
  Enhanced_Models/               Trained enhanced classifiers (.joblib)
  Training_Test_Sets/            Pre-split feature matrices
  Feature_Selection/             Retained feature masks
  Metrics/                       Train and test metrics, CSV
  Plots/                         Methodology and architecture diagrams (SVG)
requirements.txt
```

## ⚙️ Setup

```bash
conda create -n pharmaicist-p3 python=3.10 -y
conda activate pharmaicist-p3
pip install -r requirements.txt
streamlit run Home.py
```

📌 **Pinned versions matter here.** The `.joblib` model files were serialised with `scikit-learn==1.2.0`. Loading them under a different minor version will raise version warnings or fail outright. Don't relax the pin unless you plan to retrain.

## 📦 Large files

Several serialised datasets in this phase are large:

| File | Size |
|---|---|
| `data/Datasets/Regression_Proteins.pkl` | 92 MB |
| `data/Training_Test_Sets/Classification/X_train_feature_selection.pkl` | 72 MB |
| `data/Datasets/Classification_Proteins.pkl` | 48 MB |
| `data/Training_Test_Sets/Regression/X_train_feature_selection.pkl` | 14 MB |

GitHub prints a size warning for the first two on push and clone. They download normally, but expect the clone to take a while.

## 🗂️ Data

The dataset comprises roughly **163,080 drug-target interactions**, assembled from public databases and biochemical APIs. It pairs QSAR descriptors for drugs with sequence and structural features for proteins.

- **ChEMBL**, drug compounds and activity records
- **UniProt**, protein sequences
- **AlphaFold DB**, predicted 3D structures used to derive structure embeddings

The focus target is acetylcholinesterase, though the dataset spans many proteins.

## ⚠️ Limitations

- **Class imbalance is the dominant issue.** With a dummy baseline at 68% accuracy, headline accuracy figures overstate performance considerably. MCC and precision-recall balance are the metrics that carry information.
- **Negative examples are assumed, not observed.** Non-binding pairs in DTI datasets are typically unlabelled pairs treated as negatives. Some are genuinely untested rather than genuinely non-binding, which inflates apparent performance.
- **Only classification models are included in the app.** The regression pipeline, predicting binding affinity as a continuous value, has datasets and metrics committed, but the trained regression models and their Streamlit page are not in this repository.
