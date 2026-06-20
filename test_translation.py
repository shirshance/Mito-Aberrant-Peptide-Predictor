from mt_translation import (
    translate_standard,
    translate_with_frameshift,
    find_aberrant_peptides,
    validate_codon
)


def test_mitochondrial_translation():
    seq = "ATGATATGATTT"
    peptide = translate_standard(seq)
    assert peptide == "MMWF"


def test_stop_codons_without_stopping():
    seq = "ATGTAAATG"
    peptide = translate_standard(seq, stop_at_stop=False)
    assert peptide == "M_M"


def test_stop_codons_with_stopping():
    seq = "ATGTAAATG"
    peptide = translate_standard(seq, stop_at_stop=True)
    assert peptide == "M"


def test_validate_codon():
    assert validate_codon("TCT") == "TCT"


def test_frameshift_event_detected():
    seq = "ATGTCTAAACCCGGG"
    altered, events = translate_with_frameshift(
        seq=seq,
        trigger_codon="TCT",
        shift=1,
        max_frameshifts=1,
    )

    assert len(events) == 1
    assert events[0]["codon"] == "TCT"
    assert events[0]["shift"] == 1


def test_aberrant_peptides():
    wt = "MMMMMMMMMMMM"
    altered = "MMMMAAAAMMMM"

    aberrant = find_aberrant_peptides(
        wt,
        altered,
        min_length=4,
        max_length=4
    )

    assert "AAAA" in aberrant
