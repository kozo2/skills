"""
Create an mzTab-M file for plasma metabolomics data processed with XCMS 3.18.
Study: 4 treated + 4 untreated samples, LC-MS positive and negative ionization mode.
16 total .mzML files (8 positive, 8 negative). HMDB used for identification.
3 example metabolites: glucose, alanine, citric acid.
"""

import sys
sys.path.insert(0, "/Users/knishida/Documents/GitHub/pymzTab-m")

import mztab_m_io as mztabm
from mztab_m_io.model.common import (
    CV, Assay, Database, MsRun, Parameter, Sample, Software, SpectraRef, StudyVariable,
)
from mztab_m_io.model.section.mtd import Metadata
from mztab_m_io.model.section.sml import SmallMoleculeSummary
from mztab_m_io.model.section.smf import SmallMoleculeFeature
from mztab_m_io.model.section.sme import SmallMoleculeEvidence
from mztab_m_io.model.mztabm import MzTabM

OUTPUT_PATH = "/Users/knishida/.claude/plugins/cache/claude-plugins-official/skill-creator/6b70f99f769f/skills/mztab-m-writer-workspace/iteration-1/eval-2-xcms/with_skill/outputs/plasma_metabolomics_xcms.mztab"

# ---------------------------------------------------------------------------
# MS Runs
# 8 positive mode runs (4 treated, 4 untreated) + 8 negative mode runs
# Naming convention: treated_1..4, untreated_1..4 for each polarity
# ms_run IDs 1-8 = positive, 9-16 = negative
# ---------------------------------------------------------------------------

pos_run_names = [
    ("treated_1_pos", "treated"),
    ("treated_2_pos", "treated"),
    ("treated_3_pos", "treated"),
    ("treated_4_pos", "treated"),
    ("untreated_1_pos", "untreated"),
    ("untreated_2_pos", "untreated"),
    ("untreated_3_pos", "untreated"),
    ("untreated_4_pos", "untreated"),
]

neg_run_names = [
    ("treated_1_neg", "treated"),
    ("treated_2_neg", "treated"),
    ("treated_3_neg", "treated"),
    ("treated_4_neg", "treated"),
    ("untreated_1_neg", "untreated"),
    ("untreated_2_neg", "untreated"),
    ("untreated_3_neg", "untreated"),
    ("untreated_4_neg", "untreated"),
]

ms_runs = []
for i, (name, _) in enumerate(pos_run_names, start=1):
    ms_runs.append(MsRun(
        id=i,
        location=f"file:///data/plasma_metabolomics/{name}.mzML",
        format=Parameter(cv_label="MS", cv_accession="MS:1000584", name="mzML file"),
        id_format=Parameter(cv_label="MS", cv_accession="MS:1001530", name="mzML native ID format"),
        scan_polarity=[Parameter(cv_label="MS", cv_accession="MS:1000130", name="positive scan")],
    ))

for i, (name, _) in enumerate(neg_run_names, start=9):
    ms_runs.append(MsRun(
        id=i,
        location=f"file:///data/plasma_metabolomics/{name}.mzML",
        format=Parameter(cv_label="MS", cv_accession="MS:1000584", name="mzML file"),
        id_format=Parameter(cv_label="MS", cv_accession="MS:1001530", name="mzML native ID format"),
        scan_polarity=[Parameter(cv_label="MS", cv_accession="MS:1000129", name="negative scan")],
    ))

# ---------------------------------------------------------------------------
# Assays — one assay per sample (combining pos + neg runs for that sample)
# Assay IDs 1-4 = treated, 5-8 = untreated
# Each assay references its pos AND neg ms_run
# ---------------------------------------------------------------------------

assays = []
# Treated samples: assay 1-4 -> pos runs 1-4 + neg runs 9-12
for i in range(1, 5):
    assays.append(Assay(
        id=i,
        name=f"treated_{i}",
        ms_run_ref=[i, i + 8],     # pos run i, neg run i+8
    ))

# Untreated samples: assay 5-8 -> pos runs 5-8 + neg runs 13-16
for i in range(1, 5):
    assays.append(Assay(
        id=i + 4,
        name=f"untreated_{i}",
        ms_run_ref=[i + 4, i + 12],  # pos run i+4, neg run i+12
    ))

# ---------------------------------------------------------------------------
# Study Variables
# ---------------------------------------------------------------------------

study_variables = [
    StudyVariable(
        id=1,
        name="treated",
        assay_refs=[1, 2, 3, 4],
        description="Plasma samples from treated subjects",
    ),
    StudyVariable(
        id=2,
        name="untreated",
        assay_refs=[5, 6, 7, 8],
        description="Plasma samples from untreated (control) subjects",
    ),
]

# ---------------------------------------------------------------------------
# Samples
# ---------------------------------------------------------------------------

samples = []
for i in range(1, 5):
    samples.append(Sample(
        id=i,
        name=f"plasma_treated_{i}",
        species=[Parameter(cv_label="NCBITAXON", cv_accession="NCBITaxon:9606", name="Homo sapiens")],
        tissue=[Parameter(cv_label="BTO", cv_accession="BTO:0000131", name="blood plasma")],
    ))
for i in range(1, 5):
    samples.append(Sample(
        id=i + 4,
        name=f"plasma_untreated_{i}",
        species=[Parameter(cv_label="NCBITAXON", cv_accession="NCBITaxon:9606", name="Homo sapiens")],
        tissue=[Parameter(cv_label="BTO", cv_accession="BTO:0000131", name="blood plasma")],
    ))

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

metadata = Metadata(
    mztab_version="2.0.0-M",
    mztab_id="PLASMA_METABOLOMICS_XCMS_001",
    title="Plasma Metabolomics Study: Treated vs Untreated (XCMS 3.18)",
    description=(
        "Untargeted LC-MS metabolomics of human blood plasma comparing treated "
        "and untreated groups. Data was acquired in both positive and negative "
        "ionization mode (8 files each, 16 total). Peak picking and feature "
        "alignment performed with XCMS 3.18 in R. Metabolites identified against "
        "the Human Metabolome Database (HMDB)."
    ),

    quantification_method=Parameter(
        cv_label="MS",
        cv_accession="MS:1001834",
        name="LC-MS label-free quantitation analysis",
    ),

    software=[
        Software(
            id=1,
            parameter=Parameter(
                cv_label="MS",
                cv_accession="MS:1001582",
                name="XCMS",
                value="3.18",
            ),
        ),
    ],

    ms_run=ms_runs,
    assay=assays,
    study_variable=study_variables,
    sample=samples,

    cv=[
        CV(
            label="MS",
            full_name="Mass Spectrometry Ontology",
            version="4.1.38",
            uri="https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo",
        ),
        CV(
            label="NCBITAXON",
            full_name="NCBI organismal classification",
            version="2023-06-20",
            uri="http://purl.obolibrary.org/obo/ncbitaxon.owl",
        ),
        CV(
            label="BTO",
            full_name="BRENDA Tissue Ontology",
            version="2021-10-26",
            uri="http://purl.obolibrary.org/obo/bto.owl",
        ),
        CV(
            label="HMDB",
            full_name="Human Metabolome Database",
            version="5.0",
            uri="https://hmdb.ca",
        ),
    ],

    small_molecule_quantification_unit=Parameter(
        cv_label="MS", cv_accession="MS:1001839", name="area",
    ),
    small_molecule_feature_quantification_unit=Parameter(
        cv_label="MS", cv_accession="MS:1001839", name="area",
    ),
    small_molecule_identification_reliability=Parameter(
        cv_label="MS", cv_accession="MS:1002896",
        name="compound identification confidence level",
    ),

    database=[
        Database(
            id=1,
            param=Parameter(cv_label="HMDB", name="Human Metabolome Database"),
            prefix="HMDB",
            version="5.0",
            uri="https://hmdb.ca",
        ),
    ],
)

# ---------------------------------------------------------------------------
# Example abundance values (peak areas) per assay (8 assays total)
# Treated assays: 1-4, Untreated assays: 5-8
# ---------------------------------------------------------------------------

# Glucose (positive mode detected, [M+H]+ and [M+Na]+)
# Higher in untreated group
glucose_abundance = [98500.0, 102300.0, 95700.0, 99100.0, 198000.0, 205000.0, 192500.0, 201300.0]
alanine_abundance = [455000.0, 461000.0, 448000.0, 457000.0, 450000.0, 467000.0, 443000.0, 460000.0]
citrate_abundance = [320000.0, 315000.0, 328000.0, 322000.0, 158000.0, 163000.0, 155000.0, 161000.0]

# ---------------------------------------------------------------------------
# Small Molecule Evidence (SME)
# ---------------------------------------------------------------------------

sme_rows = [
    # Glucose — positive mode [M+H]+
    SmallMoleculeEvidence(
        sme_id=1,
        evidence_input_id="feat_001",
        database_identifier="HMDB:HMDB0000122",
        chemical_formula="C6H12O6",
        smiles="OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
        inchi="InChI=1S/C6H12O6/c7-1-2-3(8)4(9)5(10)6(11)12-2/h2-11H,1H2/t2-,3-,4+,5-,6?/m1/s1",
        chemical_name="glucose",
        uri="https://hmdb.ca/metabolites/HMDB0000122",
        theoretical_neutral_mass=180.0634,
        spectra_ref=[SpectraRef(ms_run=1, reference="scan=1234")],
        identification_method=Parameter(
            cv_label="MS", cv_accession="MS:1001207", name="Mascot",
        ),
        ms_level=Parameter(
            cv_label="MS", cv_accession="MS:1000511", name="ms level", value="2",
        ),
        id_confidence_measure=[0.95],
        rank=1,
    ),
    # Alanine — positive mode [M+H]+
    SmallMoleculeEvidence(
        sme_id=2,
        evidence_input_id="feat_002",
        database_identifier="HMDB:HMDB0000161",
        chemical_formula="C3H7NO2",
        smiles="C[C@@H](N)C(O)=O",
        inchi="InChI=1S/C3H7NO2/c1-2(4)3(5)6/h2H,4H2,1H3,(H,5,6)/t2-/m0/s1",
        chemical_name="alanine",
        uri="https://hmdb.ca/metabolites/HMDB0000161",
        theoretical_neutral_mass=89.0477,
        spectra_ref=[SpectraRef(ms_run=1, reference="scan=876")],
        identification_method=Parameter(
            cv_label="MS", cv_accession="MS:1001207", name="Mascot",
        ),
        ms_level=Parameter(
            cv_label="MS", cv_accession="MS:1000511", name="ms level", value="2",
        ),
        id_confidence_measure=[0.88],
        rank=1,
    ),
    # Citric acid — negative mode [M-H]-
    SmallMoleculeEvidence(
        sme_id=3,
        evidence_input_id="feat_003",
        database_identifier="HMDB:HMDB0000094",
        chemical_formula="C6H8O7",
        smiles="OC(CC(O)(C(O)=O)CC(O)=O)C(O)=O",
        inchi="InChI=1S/C6H8O7/c7-3(8)1-6(13,5(11)12)2-4(9)10/h13H,1-2H2,(H,7,8)(H,9,10)(H,11,12)",
        chemical_name="citric acid",
        uri="https://hmdb.ca/metabolites/HMDB0000094",
        theoretical_neutral_mass=192.0270,
        spectra_ref=[SpectraRef(ms_run=9, reference="scan=543")],
        identification_method=Parameter(
            cv_label="MS", cv_accession="MS:1001207", name="Mascot",
        ),
        ms_level=Parameter(
            cv_label="MS", cv_accession="MS:1000511", name="ms level", value="2",
        ),
        id_confidence_measure=[0.91],
        rank=1,
    ),
]

# ---------------------------------------------------------------------------
# Small Molecule Features (SMF)
# ---------------------------------------------------------------------------

smf_rows = [
    # Glucose [M+H]+ (positive mode)
    SmallMoleculeFeature(
        smf_id=1,
        sme_id_refs=[1],
        adduct_ion="[M+H]+",
        exp_mass_to_charge=181.0712,
        charge=1,
        retention_time_in_seconds=312.5,
        abundance_assay=glucose_abundance,
    ),
    # Alanine [M+H]+ (positive mode)
    SmallMoleculeFeature(
        smf_id=2,
        sme_id_refs=[2],
        adduct_ion="[M+H]+",
        exp_mass_to_charge=90.0550,
        charge=1,
        retention_time_in_seconds=145.2,
        abundance_assay=alanine_abundance,
    ),
    # Citric acid [M-H]- (negative mode)
    SmallMoleculeFeature(
        smf_id=3,
        sme_id_refs=[3],
        adduct_ion="[M-H]-",
        exp_mass_to_charge=191.0197,
        charge=1,
        retention_time_in_seconds=228.8,
        abundance_assay=citrate_abundance,
    ),
]

# ---------------------------------------------------------------------------
# Small Molecule Summary (SML)
# ---------------------------------------------------------------------------

sml_rows = [
    SmallMoleculeSummary(
        sml_id=1,
        smf_id_refs=[1],
        database_identifier=["HMDB:HMDB0000122"],
        chemical_formula=["C6H12O6"],
        smiles=["OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O"],
        inchi=["InChI=1S/C6H12O6/c7-1-2-3(8)4(9)5(10)6(11)12-2/h2-11H,1H2/t2-,3-,4+,5-,6?/m1/s1"],
        chemical_name=["glucose"],
        uri=["https://hmdb.ca/metabolites/HMDB0000122"],
        theoretical_neutral_mass=[180.0634],
        adduct_ions=["[M+H]+"],
        reliability="2",
        best_id_confidence_measure=Parameter(
            cv_label="MS", cv_accession="MS:1002890", name="fragmentation score",
        ),
        best_id_confidence_value=0.95,
        abundance_assay=glucose_abundance,
    ),
    SmallMoleculeSummary(
        sml_id=2,
        smf_id_refs=[2],
        database_identifier=["HMDB:HMDB0000161"],
        chemical_formula=["C3H7NO2"],
        smiles=["C[C@@H](N)C(O)=O"],
        inchi=["InChI=1S/C3H7NO2/c1-2(4)3(5)6/h2H,4H2,1H3,(H,5,6)/t2-/m0/s1"],
        chemical_name=["alanine"],
        uri=["https://hmdb.ca/metabolites/HMDB0000161"],
        theoretical_neutral_mass=[89.0477],
        adduct_ions=["[M+H]+"],
        reliability="2",
        best_id_confidence_measure=Parameter(
            cv_label="MS", cv_accession="MS:1002890", name="fragmentation score",
        ),
        best_id_confidence_value=0.88,
        abundance_assay=alanine_abundance,
    ),
    SmallMoleculeSummary(
        sml_id=3,
        smf_id_refs=[3],
        database_identifier=["HMDB:HMDB0000094"],
        chemical_formula=["C6H8O7"],
        smiles=["OC(CC(O)(C(O)=O)CC(O)=O)C(O)=O"],
        inchi=["InChI=1S/C6H8O7/c7-3(8)1-6(13,5(11)12)2-4(9)10/h13H,1-2H2,(H,7,8)(H,9,10)(H,11,12)"],
        chemical_name=["citric acid"],
        uri=["https://hmdb.ca/metabolites/HMDB0000094"],
        theoretical_neutral_mass=[192.0270],
        adduct_ions=["[M-H]-"],
        reliability="2",
        best_id_confidence_measure=Parameter(
            cv_label="MS", cv_accession="MS:1002890", name="fragmentation score",
        ),
        best_id_confidence_value=0.91,
        abundance_assay=citrate_abundance,
    ),
]

# ---------------------------------------------------------------------------
# Assemble and write
# ---------------------------------------------------------------------------

mztabm_obj = MzTabM(
    metadata=metadata,
    small_molecule_summary=sml_rows,
    small_molecule_feature=smf_rows,
    small_molecule_evidence=sme_rows,
)

print(f"Writing mzTab-M file to:\n  {OUTPUT_PATH}\n")
context = mztabm.write(mztabm_obj, OUTPUT_PATH, format="tsv")

if context.success:
    print("File written successfully!")
else:
    print("Errors / warnings during write:")
    for msg in context.messages:
        print(f"  [{msg.message_type}] {msg.message}")
    # Still check if file was created despite validation warnings
    import os
    if os.path.exists(OUTPUT_PATH):
        print(f"\nFile was created at: {OUTPUT_PATH}")
    else:
        print("\nFile was NOT created.")
        sys.exit(1)
