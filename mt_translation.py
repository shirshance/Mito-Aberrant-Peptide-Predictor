#!/usr/bin/env python3

import argparse
import random
from mt_codon_table import CODON_TABLE


def read_fasta(path):
    sequences = {}
    header = None
    seq_parts = []

    with open(path, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if header is not None:
                    sequences[header] = "".join(seq_parts).upper()

                header = line[1:].strip()
                seq_parts = []
            else:
                seq_parts.append(line)

        if header is not None:
            sequences[header] = "".join(seq_parts).upper()

    return sequences


def validate_dna_sequence(seq):
    allowed = {"A", "T", "G", "C"}
    invalid = set(seq) - allowed

    if invalid:
        raise ValueError(f"Invalid DNA letters found: {invalid}")


def validate_codon(codon):
    codon = codon.upper()

    if len(codon) != 3:
        raise ValueError("Codon must be exactly 3 nucleotides long.")

    if codon not in CODON_TABLE:
        raise ValueError(f"{codon} is not found in the mitochondrial codon table.")

    return codon


def translate_standard(seq, stop_at_stop=False):
    peptide = []

    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i + 3]
        aa = CODON_TABLE.get(codon, "X")

        if aa == "_" and stop_at_stop:
            break

        peptide.append(aa)

    return "".join(peptide)


def translate_with_frameshift(
    seq,
    trigger_codon,
    shift,
    max_frameshifts=1,
    probability=1.0,
    seed=None,
    stop_at_stop=False
):
    if seed is not None:
        random.seed(seed)

    peptide = []
    events = []

    i = 0
    frameshift_count = 0

    while i <= len(seq) - 3:
        codon = seq[i:i + 3]
        aa = CODON_TABLE.get(codon, "X")

        if aa == "_" and stop_at_stop:
            break

        peptide.append(aa)

        if (
            codon == trigger_codon
            and frameshift_count < max_frameshifts
            and random.random() <= probability
        ):
            events.append({
                "position": i + 1,
                "codon": codon,
                "shift": shift
            })

            frameshift_count += 1
            i += 3 + shift
        else:
            i += 3

    return "".join(peptide), events


def make_peptides(peptide, min_length=8, max_length=11):
    peptides = set()

    for length in range(min_length, max_length + 1):
        for i in range(0, len(peptide) - length + 1):
            sub_peptide = peptide[i:i + length]

            if "_" not in sub_peptide:
                peptides.add(sub_peptide)

    return peptides


def find_aberrant_peptides(wild_type, altered, min_length=8, max_length=11):
    wt_peptides = make_peptides(wild_type, min_length, max_length)
    altered_peptides = make_peptides(altered, min_length, max_length)

    return sorted(altered_peptides - wt_peptides)


def write_fasta(peptides, output_path):
    with open(output_path, "w") as out:
        for index, peptide in enumerate(peptides, start=1):
            out.write(f">aberrant_peptide_{index}\n")
            out.write(f"{peptide}\n")


def run_analysis(args):
    trigger_codon = validate_codon(args.codon)

    if args.shift not in [-1, 1]:
        raise ValueError("Frameshift must be +1 or -1.")

    sequences = read_fasta(args.fasta)

    for name, seq in sequences.items():
        validate_dna_sequence(seq)

        wild_type = translate_standard(seq, stop_at_stop=args.stop_at_stop)

        altered, events = translate_with_frameshift(
            seq=seq,
            trigger_codon=trigger_codon,
            shift=args.shift,
            max_frameshifts=args.max_frameshifts,
            probability=args.probability,
            seed=args.seed,
            stop_at_stop=args.stop_at_stop
        )

        aberrant_peptides = find_aberrant_peptides(
            wild_type,
            altered,
            min_length=args.min_length,
            max_length=args.max_length
        )

        print("=" * 60)
        print(f"Sequence: {name}")
        print("=" * 60)

        print("\nWild-type translation:")
        print(wild_type)

        print("\nAltered translation:")
        print(altered)

        print("\nFrameshift report:")

        if events:
            for event in events:
                print("Frameshift event detected")
                print(f"Position: {event['position']}")
                print(f"Codon: {event['codon']}")
                print(f"Shift: {event['shift']:+d}")
        else:
            print("No frameshift event detected.")

        print("\nCandidate aberrant peptides:")
        if aberrant_peptides:
            for peptide in aberrant_peptides:
                print(peptide)
        else:
            print("No unique altered peptides found.")

        if args.output:
            write_fasta(aberrant_peptides, args.output)
            print(f"\nAberrant peptides written to: {args.output}")


def main():
    parser = argparse.ArgumentParser(
        description="MitoAberrantPeptidePredictor: simulate mitochondrial frameshift translation."
    )

    parser.add_argument(
        "-f", "--fasta",
        required=True,
        help="Input mitochondrial DNA FASTA file."
    )

    parser.add_argument(
        "-c", "--codon",
        required=True,
        help="Trigger codon that causes simulated frameshift, for example TCT."
    )

    parser.add_argument(
        "-shift", "--shift",
        type=int,
        choices=[-1, 1],
        default=1,
        help="Frameshift direction: +1 or -1. Default: +1."
    )

    parser.add_argument(
        "--max-frameshifts",
        type=int,
        default=1,
        help="Maximum number of frameshift events allowed. Default: 1."
    )

    parser.add_argument(
        "--probability",
        type=float,
        default=1.0,
        help="Probability of frameshift when trigger codon is found. Default: 1.0."
    )

    parser.add_argument(
        "--min-length",
        type=int,
        default=8,
        help="Minimum candidate peptide length. Default: 8."
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=11,
        help="Maximum candidate peptide length. Default: 11."
    )

    parser.add_argument(
        "--stop-at-stop",
        action="store_true",
        help="Stop translation when mitochondrial stop codon is reached."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible probability-based frameshifts."
    )

    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Optional output FASTA file for aberrant peptides."
    )

    args = parser.parse_args()
    run_analysis(args)


if __name__ == "__main__":
    main()