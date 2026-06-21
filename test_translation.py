from mt_translation import (
    translate_standard,
    translate_with_frameshift,
    find_aberrant_peptides,
    validate_codon,
    write_fasta
)


def test_mitochondrial_translation():
    seq = "ATGATATGATTT"
    peptide = translate_standard(seq)
    assert peptide == "MMWF"


def test_translation_stops_at_stop_codon():
    seq = "ATGTAAATG"
    peptide = translate_standard(seq)
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


def test_write_fasta_with_gene_name(tmp_path):
    output_file = tmp_path / "test_output.fasta"

    peptide_records = [
        ("MT_TEST", "KKKKWLNL"),
        ("COX1", "AAAFGGPP")
    ]

    write_fasta(peptide_records, output_file)

    content = output_file.read_text()

    assert ">MT_TEST|aberrant_peptide_1" in content
    assert "KKKKWLNL" in content
    assert ">COX1|aberrant_peptide_2" in content
    assert "AAAFGGPP" in content
