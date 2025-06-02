# ECDSA Anomalies: Algebraic Signature Vulnerabilities

This repository accompanies the research paper:

**"Algebraic Anomalies in ECDSA Signatures Enabling Private Key Recovery Under Ideal Random Nonces"**

## 🔍 Overview

This work explores algebraic anomalies in ECDSA signatures that allow deterministic recovery of private keys under ideal randomness assumptions. We describe two classes of vulnerabilities (Case A and Case B), backed by analytical formulas, simulations, and experimental transaction datasets.

## 📁 Structure

```
ECDSA-Anomalies/
├── README.md
├── LICENSE
├── src/
│   |── find_curve.py                          # Script to find test elliptic curve parameters
│   |── secp256k1.py                           # Script to generate millions of test transactions
│   |── verify_case_a.py                       # Script to verify case A using public data
│   └── verify_case_b.py                       # Script to verify case B using public data
├── data/
│   ├── transaction_list_20250529191555.txt    # Sample categorized anomalies
│   ├── transaction_list_20250529194848.txt    # Sample categorized anomalies
│   ├── transaction_list_20250529202417.txt    # Sample categorized anomalies
│   ├── transaction_list_20250529205625.txt    # Sample categorized anomalies
│   ├── transaction_list_20250529212843.txt    # Sample categorized anomalies
│   └── transaction_list_20250529220308.txt    # Sample categorized anomalies
└── paper/
    ├── Algebraic_Anomalies_in_ECDSA.pdf
    └── Algebraic_Anomalies_in_ECDSA.tex
```

## 📜 Included

- Python scripts for full simulation over test elliptic curve
- Reproducible anomaly detection for Case A and B
- Verified examples of deterministic private key recovery
- LaTeX source and PDF of the final research article

## 📘 Citation

If you use this repository for your research or teaching, please cite the original paper:

```
[To be filled after publication or preprint DOI]
```

## 🔗 License

Released under MIT License (see LICENSE file).

## 📎 Link to the Paper

The full research paper can be viewed and downloaded here:

📄 [Algebraic_Anomalies_in_ECDSA.pdf](./paper/Algebraic_Anomalies_in_ECDSA.pdf)

## 🚀 Quick Start

Clone the repository and run the transaction generator:

```bash
git clone https://github.com/YOUR_USERNAME/ECDSA-Anomalies.git
cd ECDSA-Anomalies/src
python secp256k1.py
```

### 🔐 Verification Tool

Run this to validate Case A, B transactions using public parameters:

```bash
python src/verify_case_a.py
python src/verify_case_b.py
```

# Research paper: Algebraic Anomalies in ECDSA Signatures Enabling Private Key Recovery Under Ideal Random Nonces

[![Download PDF](https://img.shields.io/badge/Paper-Download-blue)](./paper/Algebraic_Anomalies_in_ECDSA.pdf)

This repository accompanies the research paper: