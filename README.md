# Mito-Aberrant-Peptide-Predictor

## Overview

MitoAberrantPeptidePredictor is an in silico mitochondrial translation simulator designed to model abnormal translation events that may occur under altered tRNA modification conditions.

The project was inspired by ongoing research on TRIT1 knockout cells and the potential effects of defective tRNA modifications on mitochondrial translation fidelity.

The tool predicts how translation outcomes may change when specific codons trigger ribosomal frameshift events during mitochondrial translation, generating alternative peptide products that may not exist under normal conditions.

These aberrant peptides may potentially become a source of non-canonical antigens and contribute to peptide presentation observed in immunopeptidomics experiments.

---

## Biological Motivation

Transfer RNA (tRNA) modifications are critical for maintaining translation fidelity and proper decoding of codons.

TRIT1 (tRNA Isopentenyltransferase 1) introduces the i6A (N6-isopentenyladenosine) modification into specific tRNAs. This modification improves decoding efficiency and translational accuracy.

TRIT1 deficiency has been associated with mitochondrial dysfunction and altered mitochondrial tRNA biology.

The broader goal of our research is to understand whether disruption of TRIT1 activity may contribute to abnormal translation events that generate aberrant peptide sequences.

Such peptides could potentially:

- Alter mitochondrial protein synthesis
- Affect respiratory complex function
- Generate non-canonical peptide products
- Contribute to immunopeptidome diversity

This project creates a computational framework to investigate this hypothesis.

---

## Project Goal

The purpose of this project is to simulate mitochondrial translation and artificially introduce frameshift events at user-defined codons.

The initial version focuses on serine-associated codons because of their biological relevance to ongoing TRIT1-related studies.

The software compares normal translation to altered translation and identifies peptide regions generated exclusively after frameshift events.

---

## Input

The program expects:

### 1. FASTA sequence

A nucleotide FASTA file corresponding to one of the 13 mitochondrial protein-coding genes.

Example:

```fasta
>MT-ND1
ATGATATGATTTGCTGCTGCTGCTGCTTAA
```

### 2. Frameshift trigger codon

A codon specified by the user:

```text
UCU
```

When the simulated ribosome encounters this codon, a programmed frameshift event may occur.

### Optional future parameters

- Frameshift direction (+1 or -1)
- Number of allowed frameshifts
- Frameshift probability
- Specific translation positions
- Output peptide length threshold

---

## Output

The tool generates:

### Wild-type translation

```text
MFLASV...
```

### Altered translation

```text
MFLSGWP...
```

### Frameshift report

```text
Frameshift event detected

Position: 21
Codon: UCU
Shift: +1
```

### Candidate aberrant peptides

Peptide sequences appearing only in the altered translation:

```text
SGWPKLV
AFGTRVL
```

These peptides may represent potential candidates for future immunopeptidomics analyses.

---

## Planned Features

Future versions may include:

- Support for additional codons
- Automatic comparison of WT vs KO translation
- Codon usage analysis
- Visualization of frameshift locations
- Peptide window generation for immunopeptidomics workflows
- CSV export
- Graphical interface
- Integration with mass spectrometry candidate analysis

---

## Installation

Clone repository:

```bash
git clone https://github.com/shirshance/MitoAberrantPeptidePredictor.git
```

Move into project directory:

```bash
cd MitoAberrantPeptidePredictor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the program

Example:

```bash
python mt_translation.py \
-f MT-ND1.fasta \
-c UCU \
-shift +1
```

---

## Running tests

```bash
pytest
```

---

## Repository Structure

```text
MitoAberrantPeptidePredictor/

├── mt_translation.py
├── translation_lib.py
├── test_translation.py
├── requirements.txt
├── example_data/
│   └── MT-ND1.fasta
└── README.md
```

---

## Example Workflow

Input:

FASTA sequence → mitochondrial coding sequence

↓

Translate using mitochondrial codon table

↓

Introduce frameshift event at selected codon

↓

Generate altered protein sequence

↓

Identify novel peptide regions

↓

Predict candidate aberrant peptides

---

## Course Information

This project was developed as part of a Python programming course project.

The biological inspiration comes from ongoing studies investigating TRIT1 function, mitochondrial translation fidelity, and generation of potentially novel peptide products.
