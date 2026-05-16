# MitoAberrantPeptidePredictor

## Overview

MitoAberrantPeptidePredictor is an in silico mitochondrial translation simulator designed to model abnormal translation events occurring during mitochondrial protein synthesis.

Mitochondria contain their own translation machinery, including a specialized set of mitochondrial transfer RNAs (mt-tRNAs) and a distinct genetic code used to translate the 13 mitochondrially encoded proteins.

Transfer RNA modifications are critical for accurate codon decoding and translation fidelity. Alterations in these processes may affect ribosome behavior and potentially generate unexpected translation products.

This tool predicts how mitochondrial translation outcomes may change when specific codons trigger simulated ribosomal frameshift events, generating alternative peptide products that may not exist under normal conditions.

---

## Biological Motivation

Transfer RNA (tRNA) modifications play an important role in maintaining translation fidelity and proper decoding of codons.

These modifications can influence translation efficiency, ribosome movement, codon recognition, and overall protein synthesis. Disruption of translation-associated pathways has been associated with altered translation dynamics and generation of unexpected translation products.

Abnormal translation events, including altered decoding and frameshifting, may generate peptide sequences that differ from canonical proteins.

Such peptide products are of interest because they may:

- Alter protein synthesis
- Affect cellular function
- Generate non-canonical peptide products
- Contribute to peptide diversity detected in immunopeptidomics studies

Understanding how changes in translation behavior influence peptide generation remains an active area of research.

---

## Project Goal

The purpose of this project is to simulate mitochondrial translation and artificially introduce frameshift events at user-defined codons.

The software compares standard translation with altered translation conditions and identifies peptide regions generated exclusively after simulated translation disruptions.

Initially, the project focuses on mitochondrial coding sequences and provides a flexible framework for testing different translation scenarios.

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

### 2. Trigger codon

A codon specified by the user:

```text
UCU
```

When the simulated ribosome encounters this codon, a frameshift event can be introduced.

### Optional parameters

- Frameshift direction (+1 or -1)
- Number of allowed frameshifts
- Translation position
- Frameshift probability
- Output peptide length threshold

---

## Output

The tool generates:

### Wild-type translation

```text
MMWF...
```

### Altered translation

```text
MMWSGLL...
```

### Frameshift report

```text
Frameshift event detected

Position: 21
Codon: UCU
Shift: +1
```

### Candidate aberrant peptides

Peptide sequences generated only after altered translation:

```text
SGWPKLV
AFGTRVL
```

The predicted peptide products may ultimately be used to generate a custom peptide database for comparison with mass spectrometry datasets, enabling the search for experimentally detected translation-derived peptide candidates.

---

## Installation

Clone repository:

```bash
git clone https://github.com/shirshance/MitoAberrantPeptidePredictor.git
```

Move into the project directory:

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

├── mt_translation.py        # Main program workflow
├── mt_codon_table.py        # Human mitochondrial genetic code
├── test_translation.py      # Unit tests
├── requirements.txt
├── example_data/
│   └── MT-ND1.fasta
└── README.md
```

---



## Course Information

This project was developed as part of a Python programming course project https://github.com/Code-Maven/wis-python-course-2026-03

The project combines computational biology and simulation approaches to investigate how altered translation behavior may affect protein products and generate novel peptide sequences.
