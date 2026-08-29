# Phase II — Enhanced Molecular Generation

Generates novel drug-like molecules biased toward high predicted potency against **acetylcholinesterase**. Where Phase I scores compounds that already exist, this stage invents new ones.

Built on the **ReLeaSE** framework (Reinforcement Learning for Structural Evolution, Popova, Isayev & Tropsha, *Science Advances* 2018).

> This phase was published as a Springer conference paper.
> *(Add full citation and DOI here.)*

## How it works

Two networks, trained separately, then coupled through reinforcement learning:

```
        ┌──────────────────────────────────────┐
        │                                      │
        ▼                                      │
  Stack-augmented GRU  ──▶  generated SMILES ──┤
     (generator)                               │
        ▲                                      ▼
        │                            Random Forest predictor
        └──────── policy gradient ◀──── reward R(s) = exp(pIC50 / 3)
```

The **generator** is a stacked GRU with an augmented memory stack, trained on ChEMBL SMILES to minimise cross-entropy against ground-truth tokens. It learns SMILES grammar well enough to emit syntactically valid strings, with an RDKit filter discarding the rest.

The **predictor** is the Random Forest carried over from Phase I, scoring each generated molecule's pIC50.

The **reward function** `R(s) = exp(predictor(s) / 3)` makes the return grow exponentially with predicted potency, so the policy gradient pushes the generator hard toward the high-pIC50 region of chemical space. The loss is the standard REINFORCE objective with discount factor γ.

Two objectives are explored, one per notebook:

| Notebook | Objective |
|---|---|
| `ReinlogP.ipynb` | Optimise toward a target logP range (drug-likeness / lipophilicity) |
| `ReinMinMax.ipynb` | Maximise and minimise pIC50, to show the reward genuinely steers generation |

## Results

- **84% of generated strings are valid SMILES.**
- **Mean Tanimoto similarity 0.70** against known AChE-active molecules in the [Polypharmacology Browser 2 (PPB2)](https://ppb2.gdb.tools/). The closest match is CHEMBL59782 at 0.71.
- The pIC50 distribution shifts from the training data's dense band around **4–6** into **10–12** for generated molecules.

That last point needs context — see limitations below.

## Contents

```
ReinlogP.ipynb        RL optimisation toward target logP
ReinMinMax.ipynb      RL optimisation maximising / minimising pIC50
Assets/data/
  data_train.txt      SMILES corpus for generator pretraining
  LogP_data.csv       logP labels for the property predictor
Assets/images/        Architecture diagrams, dataset distribution plots
Output/
  generated_molecules.png
  min_max.png
  output.txt          Generated SMILES with predicted pIC50
```

## Setup

The notebooks import `stackRNN`, `data`, `predictor` and related modules **from the ReLeaSE repository, not from this folder.** Clone it as a sibling directory:

```bash
git clone https://github.com/isayev/ReLeaSE.git
cd ReLeaSE
```

Then create the environment:

```bash
conda create -n pharmaicist-p2 python=3.7 -y
conda activate pharmaicist-p2
conda install -c rdkit rdkit -y
pip install torch numpy pandas scikit-learn matplotlib seaborn mordred tqdm jupyter
```

Point the notebooks at the ReLeaSE `release/` directory — the committed cells contain absolute paths from the original author's machine (`~/manikanta/ReLeaSE/release/`), so adjust the `sys.path.append` calls before running.

A CUDA GPU is strongly recommended:

```bash
export CUDA_VISIBLE_DEVICES=0
jupyter notebook
```

## Data

`Assets/data/data_train.txt` holds the SMILES corpus used for generator pretraining, drawn from ChEMBL. The dataset skews toward molecules of 30–40 atoms, single and aromatic bonds (order 1.0 and 1.5), and is carbon-dominated — the elemental distribution plots in `Assets/images/` show this.

## Limitations

**Predicted pIC50 above ~12 is reward hacking, not chemistry.** The generator is optimised against the Phase I Random Forest, which was trained on a pIC50 range of roughly 2–12. Pushing generation into 10–12 (and, in some outputs, well beyond) moves the molecules outside the predictor's support, where its estimates are extrapolation. The generator is effectively finding inputs that fool the scoring function. This is a known failure mode of predictor-in-the-loop generative models and is why the PPB2 similarity check matters more than the pIC50 numbers.

**Tanimoto 0.70 means structural resemblance, not activity.** A generated molecule scoring 0.70 against a known AChE inhibitor shares substructure with it. It has not been shown to bind anything.

**No synthesisability filter.** Generated SMILES are not screened for synthetic accessibility, so some may be chemically valid but impractical to make.

## Credit

The generator architecture, stack-augmented RNN implementation, and RL training loop come from [isayev/ReLeaSE](https://github.com/isayev/ReLeaSE) (MIT licence). The contribution here is the AChE-specific predictor, reward shaping, and validation pipeline.

> Popova M, Isayev O, Tropsha A. *Deep reinforcement learning for de novo drug design.* Science Advances, 4(7), 2018. doi:10.1126/sciadv.aap7885
