# MitoAberrantPeptidePredictor

## Overview

MitoAberrantPeptidePredictor is an in silico mitochondrial translation simulator designed to model how ribosomal frameshift events may alter mitochondrial protein translation.

Mitochondria possess their own genetic code and translation machinery. Changes in translation fidelity, codon decoding, or ribosome behavior may generate peptide products that differ from canonical mitochondrial proteins.

This tool simulates user-defined frameshift events during mitochondrial translation and identifies peptide sequences that are generated exclusively after the simulated translation alteration.

## Biological Background

Transfer RNA (tRNA) modifications are important for accurate codon recognition and translation fidelity. Disruption of these processes may alter translation dynamics and generate non-canonical protein products.

MitoAberrantPeptidePredictor provides a simple framework for exploring how frameshift events could affect mitochondrial translation and produce alternative peptide sequences that may be relevant for downstream proteomics and immunopeptidomics analyses.

## Project Goal

The software compares:

* Standard mitochondrial translation
* Translation containing simulated frameshift events

and identifies peptide fragments that are present only in the altered translation.

These predicted peptides can be exported as a FASTA database for downstream mass spectrometry searches.

---

## Input

The program requires:

### 1. Mitochondrial FASTA sequence

A nucleotide FASTA file containing one or more mitochondrial protein-coding sequences.

Example:

```text
>Mitochondrial_gene
ATGATATGATTTGCTGCTGCTGCTGCTTAA
```

### 2. Trigger codon

A codon specified by the user that triggers a simulated frameshift event.

Example:

```text
TCT
```

When the simulated ribosome encounters this codon, a frameshift event can be introduced.


---

## Command-Line Options

### Required Arguments

#### `-f`, `--fasta`

Input mitochondrial FASTA file.

Example:

```bash
-f human_mt_COX1.fasta
```

#### `-c`, `--codon`

Trigger codon that causes a simulated frameshift event.

Example:

```bash
-c TCT
```

---

### Optional Arguments

#### `-shift`, `--shift`

Frameshift direction.

Options:

* `1` = +1 frameshift
* `-1` = -1 frameshift

Default:

```bash
-shift 1
```

---

#### `--max-frameshifts`

Maximum number of frameshift events allowed within a sequence.

Default:

```bash
--max-frameshifts 1
```

---

#### `--min-length`

Minimum candidate peptide length.

Default:

```bash
--min-length 8
```

---

#### `--max-length`

Maximum candidate peptide length.

Default:

```bash
--max-length 11
```

---

#### `-o`, `--output`

Output FASTA file containing predicted aberrant peptides.

Default:

```bash
aberrant_peptides.fasta
```

Example:

```bash
-o custom_database.fasta
```

---

## Output

The tool generates:

### Wild-Type Translation

Example:

```text
KKKKWFKFGPF
```

### Altered Translation

Example:

```text
KKKKWLNLGP
```

### Frameshift Report

Example:

```text
Frameshift event detected

Position: 13
Codon: TGA
Shift: +1
```

### Candidate Aberrant Peptides

Candidate aberrant peptides are peptide fragments generated from the altered translation that are absent from the corresponding wild-type translation.

Example:

```text
KKKKWLNL
KKKKWLNLG
KKKKWLNLGP
KKKWLNLG
KKKWLNLGP
KKWLNLGP
```

Peptide lengths are controlled using:

```bash
--min-length
--max-length
```

---

## FASTA Output

All candidate aberrant peptides are automatically written to a FASTA file.

Example:

```text
>MT-CO1|aberrant_peptide_1
KKKKWLNL

>MT-CO1|aberrant_peptide_2
KKKWLNLG
```

If identical peptide sequences are generated from multiple genes, they are stored only once and their FASTA header contains all contributing gene names.

The resulting FASTA file can be used as a custom peptide database for downstream proteomics and immunopeptidomics analyses.

---

## Installation

Clone the repository:

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

## Running the Program

Example:

```bash
python mt_translation.py \
-f human_mt_COX1.fasta \
-c TGA \
-shift 1
```

---

## Running Tests

```bash
py -m pytest
```

For convenience, the repository also includes an example FASTA file containing the human mitochondrial COX1 (MT-CO1) coding sequence, which can be used to test and explore the software without providing a custom input sequence. (source: https://www.ncbi.nlm.nih.gov/nuccore/251831106)

---

## Repository Structure

```text
MitoAberrantPeptidePredictor/

├── mt_translation.py        # Main program workflow
├── mt_codon_table.py        # Human mitochondrial genetic code
├── test_translation.py      # Unit tests
├── human_mt_COX1.fasta      # Human mitochondrial COX1 coding sequence
├── requirements.txt
└── README.md
```

---

## Course Information

This project was developed as part of the Python Programming Course:

https://github.com/Code-Maven/wis-python-course-2026-03

The project combines computational biology and simulation approaches to investigate how altered mitochondrial translation behavior may generate non-canonical peptide products.
