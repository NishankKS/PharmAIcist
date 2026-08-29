# 🧬 PharmAIcist: AI in the Discovery of Drugs

A three-stage machine learning pipeline for early-stage drug discovery in Alzheimer's disease, targeting the **acetylcholinesterase (AChE)** enzyme. Submitted as a B.E. final year project in Artificial Intelligence & Machine Learning at Dayananda Sagar College of Engineering (VTU), 2023-24.

The pipeline goes from *screening known compounds*, to *generating new ones*, to *predicting whether they bind*. Each stage feeds the next.

---

## 🔬 Pipeline

```
ChEMBL (AChE, CHEMBL220)
         │
         ▼
┌────────────────────────────┐
│ Phase I                    │   PubChem fingerprints + Lipinski descriptors
│ Bioactivity & Toxicity     │──▶ regression for pIC50, classification for toxicity
└────────────────────────────┘
         │ shortlisted bioactive scaffolds
         ▼
┌────────────────────────────┐
│ Phase II                   │   Stack-augmented GRU generator + RF predictor,
│ Molecule Generation        │──▶ optimised by policy-gradient reinforcement learning
└────────────────────────────┘
         │ novel SMILES biased toward high pIC50
         ▼
┌────────────────────────────┐
│ Phase III                  │   Drug fingerprints + AlphaFold-derived protein
│ Drug-Target Interaction    │──▶ sequence/structure embeddings → binding classifier
└────────────────────────────┘
         │
         ▼
   candidates for further study
```

---

## 📊 Phases

| | Phase | What it does | Best model | Reported result |
|---|---|---|---|---|
| **I** | 🧪 [Bioactivity & Toxicity](phase-1-bioactivity-toxicity/) | Predicts pIC50 potency and toxicity for compounds against AChE | Random Forest (bioactivity), Extra Trees (toxicity) | Test R² 0.649, train R² 0.943 |
| **II** | ⚗️ [Molecule Generation](phase-2-molecule-generation/) | Generates novel drug-like SMILES optimised for potency and logP | Stacked GRU + RL (ReLeaSE) | 84% valid SMILES, Tanimoto 0.70 vs. PPB2 |
| **III** | 🔗 [Drug-Target Interaction](phase-3-drug-target-interaction/) | Predicts whether a drug-protein pair binds | Random Forest | 76% test accuracy, MCC 0.41 |

📌 The Phase II work was published at ICICV 2024 (Springer LNNS), first author. Citation below.

Each phase folder has its own README with setup, data sources, and how to run it.

---

## 📁 Repository layout

```
PharmAIcist/
├── phase-1-bioactivity-toxicity/     Streamlit app + PaDEL descriptor pipeline
├── phase-2-molecule-generation/      RL notebooks, training data, generated output
├── phase-3-drug-target-interaction/  Streamlit app, trained models, DTI datasets
├── docs/
│   └── Bachelors_Final_Thesis.pdf    Full project report
└── README.md
```

---

## 🗂️ Data sources

| Source | Used in | Purpose |
|---|---|---|
| [ChEMBL](https://www.ebi.ac.uk/chembl/) (CHEMBL220) | I, II, III | AChE bioactivity data, IC50 → pIC50 |
| [Tox21](https://tripod.nih.gov/tox21/) / TOXNET | I | Toxicity labels |
| [PubChem](https://pubchem.ncbi.nlm.nih.gov/) | I, III | Molecular fingerprints (via PaDEL) |
| [UniProt](https://www.uniprot.org/) | III | Protein sequences |
| [AlphaFold DB](https://alphafold.ebi.ac.uk/) | III | Predicted 3D structures for embeddings |
| [PPB2](https://ppb2.gdb.tools/) | II | Validation of generated molecules |

The Phase III dataset comprises roughly 163,000 curated drug-target interactions.

---

## ⚙️ Running the code

The three phases have **incompatible dependency sets**. Phase II needs PyTorch and an older RDKit, while Phase III pins `scikit-learn==1.2.0` for model deserialisation. Use a separate environment per phase:

```bash
conda create -n pharmaicist-p1 python=3.9 && conda activate pharmaicist-p1
cd phase-1-bioactivity-toxicity && pip install -r requirements.txt
```

Repeat with `-p2` and `-p3`. Per-phase instructions live in each folder's README.

📦 **Large files.** Phase III ships several serialised datasets over 50 MB. GitHub warns about these but they clone normally.

---

## ⚠️ Notes and limitations

Worth being upfront about, for anyone reading this as reference rather than as a finished tool:

- **Phase I generalisation gap.** Train R² 0.943 against test R² 0.649 indicates the Random Forest overfits the fingerprint space. The 86% figure quoted in the report is a classification accuracy at the pIC50 > 6 activity threshold, not a regression score.
- **Phase II pIC50 values are extrapolations.** The generator is rewarded by the Phase I predictor, so it learns to exploit that predictor's blind spots. Some generated molecules receive predicted pIC50 values well outside the range present in the training data (roughly 2 to 12). These are not experimental measurements and should not be read as such. Tanimoto similarity against PPB2 peaks at 0.70, which is structural resemblance to known actives rather than validated activity.
- **Phase III class balance.** The dummy classifier reaches 68% test accuracy, so the Random Forest's 76% is a modest lift over the majority baseline. MCC (0.41) is the more informative metric here.
- **No wet-lab validation.** Every result is computational.

---

## 📄 Publication

The Phase II work was published at the International Conference on Innovations in Computational Intelligence and Computer Vision (ICICV 2024).

> Satish, N., Bukapindi, M., K, S., Akhil, G., Malagi, V.P. (2024).
> *Innovating Drug Design for Alzheimer's Disease via Reinforcement Learning for Enhanced Molecular Generation.*
> In: Roy, S., Sinwar, D., Dey, N., Perumal, T., R. S. Tavares, J.M. (eds)
> Innovations in Computational Intelligence and Computer Vision. ICICV 2024.
> Lecture Notes in Networks and Systems, vol 1117. Springer, Singapore.
> [https://doi.org/10.1007/978-981-97-6992-6_20](https://doi.org/10.1007/978-981-97-6992-6_20)

---

## 👥 Authors

B.E. Artificial Intelligence & Machine Learning, Dayananda Sagar College of Engineering, Bengaluru.

- **Nishank K S** (1DS20AI036)
- **Manikanta B** (1DS20AI018)
- **Shreyas K** (1DS20AI052)
- **Guru Akhil M** (1DS20AI031)

🎓 Under the guidance of **Dr. Vindhya P Malagi**, Professor and Head, Department of AI & ML, DSCE.

This repository consolidates work originally developed across three separate repositories maintained by the team. The original repositories remain the historical record of contribution.

---

## 📦 Third-party components

- **[ReLeaSE](https://github.com/isayev/ReLeaSE)** (Popova, Isayev & Tropsha). Phase II's generator architecture is built on this framework. MIT licence.
- **[PaDEL-Descriptor](http://www.yapcwsoft.com/dd/padeldescriptor/)** (Yap, 2011), vendored in Phase I for fingerprint calculation. Built on the CDK toolkit (LGPL).

## 📜 Licence

MIT, see [LICENSE](LICENSE). Third-party components retain their own licences.
