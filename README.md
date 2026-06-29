# 🔗 Social Network Link Prediction

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-2.5%2B-orange?style=flat-square)](https://networkx.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.19%2B-013243?style=flat-square&logo=numpy)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)


## 📊 Overview

Comprehensive implementation of 8 link prediction algorithms tested on real-world social networks.

### Algorithms Implemented
- Common Neighbors
- Adamic-Adar
- Jaccard Similarity
- Preferential Attachment
- Hub Promoted
- Hub Depressed
- Allocation Index
- Degree Distribution Analysis

### Networks Analyzed
- Twitter (4,000+ nodes)
- Google+ (3,000+ nodes)
- Wikipedia Vote (7,000+ nodes)

### Evaluation Method
AUC-ROC metrics for objective performance ranking

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python commonneighbors/commonneighborstwitter.py
```
