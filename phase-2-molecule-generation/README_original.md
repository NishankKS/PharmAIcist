# PharmAIcist-Phase-I
 
# ReLeaSE: Reinforcement Learning for Molecule Generation

This repository contains the code for the ReLeaSE (Reinforcement Learning for Structural Evolution) project, which focuses on leveraging Reinforcement Learning (RL) techniques to generate novel molecular structures. CHEMBL220

## Overview

The ReLeaSE framework incorporates a Stack Augmented Recurrent Neural Network (StackAugmentedRNN) for molecule generation, along with a Random Forest Regressor used as a predictor for molecule properties. The RL agent is trained to generate molecules with desired properties through a defined reward function and policy gradient methods.

![System Overview_Phase-I](https://github.com/Manikanta-7342/PharmAIcist-Phase-I/assets/92366177/9ed808f2-3e74-4190-8301-2e6d01d02a24)


## Getting Started

### Prerequisites

- Python 3.x
- PyTorch
- RDKit
- Mordred
- Other dependencies (specified in requirements.txt)

### Installation

1. Clone the ReLeaSE repository:

    ```bash
    git clone https://github.com/isayev/ReLeaSE.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the environment variables:

    ```bash
    export CUDA_VISIBLE_DEVICES=0
    ```

4. Move to the release directory:

    ```bash
    cd ReLeaSE/release
    ```
