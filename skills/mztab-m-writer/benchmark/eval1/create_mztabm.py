"""
Create an mzTab-M file for a mouse liver lipidomics experiment.

Experiment details:
- Instrument: Q Exactive HF, positive mode ESI
- Software: MS-DIAL 5.0
- Study: MTBLS9999 (MetaboLights)
- Samples: 3 control mice + 3 high-fat diet mice, each with one .mzML file
- Files: ctrl_1.mzML, ctrl_2.mzML, ctrl_3.mzML, hfd_1.mzML, hfd_2.mzML, hfd_3.mzML
"""

import sys
import os

# Ensure pymzTab-m is importable
sys.path.insert(0, "/Users/knishida/Documents/GitHub/pymzTab-m")

import mztab_m_io as mztabm
from mztab_m_io.model.common import (
    CV, Assay, Database, Instrument, MsRun, Parameter, Sample, Software, SpectraRef, StudyVariable,
)
from mztab_m_io.model.section.mtd import Metadata
from mztab_m_io.model.section.sml import SmallMoleculeSummary
from mztab_m_io.model.section.smf import SmallMoleculeFeature
from mztab_m_io.model.section.sme import SmallMoleculeEvidence
from mztab_m_io.model.mztabm import MzTabM

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "MTBLS9999.mztab")

# ---------------------------------------------------------------------------
# MS Runs — one per input .mzML file
# ---------------------------------------------------------------------------
ms_runs = [
    MsRun(
        id=1,
        location="file://studies/MTBLS9999/ctrl_1.mzML",
        format=Parameter(cv_label="MS", cv_accession="MS:1000584", name="mzML file"),
        id_format=Parameter(cv_label="MS", cv_accession="MS:1001530", name="mzML native ID format"),
        scan_polarity=[Parameter(cv_label="MS", cv_accession="MS:1000130", name="positive scan")],
    ),
    MsRun(
        id=2,
        location="file://studies/MTBLS9999/ctrl_2.mzML",
        format=Parameter(cv_label="MS", cv_accession="MS:1000584", name="mzML file"),
        id_format=Parameter(cv_label="MS", cv_accession="MS:1001530", name="mzML native ID format"),
        scan_polarity=[Parameter(cv_label="MS", cv_accession="MS:1000130", name="positive scan")],
    ),
    MsRun(
        id=3,
        location="file://studies/MTBLS9999/ctrl_3.mzML",
        format=Parameter(cv_label="MS", cv_accession="MS:1000584", name="mzML file"),
        id_format=Parameter(cv_label="MS", cv_accession="MS:1001530", name="mzML native ID format"),
        scan_polarity=[Parameter(cv_label="MS", cv_accession="MS:1000130", name="positive scan")],
    ),
    MsRun(
        id=4,
        location="file://studies/MTBLS9999/hfd_1.mzML",
        format=Parameter(cv_label="MS", cv_accession="MS:1000584", name="mzML file"),
        id_format=Parameter(cv_label="MS", cv_accession="MS:1001530", name="mzML native ID format"),
        scan_polarity=[Parameter(cv_label="MS", cv_accession="MS:1000130", name="positive scan")],
    ),
    MsRun(
        id=5,
        location="file://studies/MTBLS9999/hfd_2.mzML",
        format=Parameter(cv_label="MS", cv_accession="MS:1000584", name="mzML file"),
        id_format=Parameter(cv_label="MS", cv_accession="MS:1001530", name="mzML native ID format"),
        scan_polarity=[Parameter(cv_label="MS", cv_accession="MS:1000130", name="positive scan")],
    ),
    MsRun(
        id=6,
        location="file://studies/MTBLS9999/hfd_3.mzML",
        format=Parameter(cv_label="MS", cv_accession="MS:1000584", name="mzML file"),
        id_format=Parameter(cv_label="MS", cv_accession="MS:1001530", name="mzML native ID format"),
        scan_polarity=[Parameter(cv_label="MS", cv_accession="MS:1000130", name="positive scan")],
    ),
]

# ---------------------------------------------------------------------------
# Assays — one per MS run
# ---------------------------------------------------------------------------
assays = [
    Assay(id=1, name="ctrl_1", ms_run_ref=[1]),
    Assay(id=2, name="ctrl_2", ms_run_ref=[2]),
    Assay(id=3, name="ctrl_3", ms_run_ref=[3]),
    Assay(id=4, name="hfd_1", ms_run_ref=[4]),
    Assay(id=5, name="hfd_2", ms_run_ref=[5]),
    Assay(id=6, name="hfd_3", ms_run_ref=[6]),
]

# ---------------------------------------------------------------------------
# Study variables — control vs high-fat diet
# ---------------------------------------------------------------------------
study_variables = [
    StudyVariable(
        id=1,
        name="control",
        assay_refs=[1, 2, 3],
        description="Control diet mouse liver",
    ),
    StudyVariable(
        id=2,
        name="high_fat_diet",
        assay_refs=[4, 5, 6],
        description="High-fat diet mouse liver",
    ),
]

# ---------------------------------------------------------------------------
# Samples
# ---------------------------------------------------------------------------
samples = [
    Sample(
        id=1,
        name="mouse_liver_control",
        species=[Parameter(cv_label="NCBITAXON", cv_accession="NCBITaxon:10090", name="Mus musculus")],
        tissue=[Parameter(cv_label="BTO", cv_accession="BTO:0000759", name="liver")],
        disease=[Parameter(cv_label="DOID", cv_accession="DOID:4", name="disease")],
    ),
    Sample(
        id=2,
        name="mouse_liver_high_fat_diet",
        species=[Parameter(cv_label="NCBITAXON", cv_accession="NCBITaxon:10090", name="Mus musculus")],
        tissue=[Parameter(cv_label="BTO", cv_accession="BTO:0000759", name="liver")],
        disease=[Parameter(cv_label="DOID", cv_accession="DOID:9970", name="obesity")],
    ),
]

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
metadata = Metadata(
    mztab_version="2.0.0-M",
    mztab_id="MTBLS9999",
    title="Mouse liver lipidomics: control vs high-fat diet",
    description=(
        "Untargeted lipidomics of mouse liver tissue comparing control diet and "
        "high-fat diet groups. Samples were analyzed by LC-MS/MS on a Q Exactive HF "
        "in positive ion mode ESI. Data were processed with MS-DIAL 5.0."
    ),
    # Quantification method: LC-MS label-free
    quantification_method=Parameter(
        cv_label="MS",
        cv_accession="MS:1001834",
        name="LC-MS label-free quantitation analysis",
    ),
    # Instrument
    instrument=[
        Instrument(
            id=1,
            name=Parameter(
                cv_label="MS",
                cv_accession="MS:1002523",
                name="Q Exactive HF",
            ),
            source=Parameter(
                cv_label="MS",
                cv_accession="MS:1000073",
                name="electrospray ionization",
            ),
            analyzer=[
                Parameter(
                    cv_label="MS",
                    cv_accession="MS:1000084",
                    name="time-of-flight",
                )
            ],
            detector=Parameter(
                cv_label="MS",
                cv_accession="MS:1000624",
                name="inductive detector",
            ),
        )
    ],
    # Software
    software=[
        Software(
            id=1,
            parameter=Parameter(
                cv_label="MS",
                cv_accession="MS:1003082",
                name="MS-DIAL",
                value="5.0",
            ),
        )
    ],
    ms_run=ms_runs,
    assay=assays,
    study_variable=study_variables,
    sample=samples,
    # Controlled vocabularies used
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
            version="2023",
            uri="https://www.ebi.ac.uk/ols/ontologies/ncbitaxon",
        ),
        CV(
            label="BTO",
            full_name="BRENDA Tissue Ontology",
            version="2021",
            uri="https://www.ebi.ac.uk/ols/ontologies/bto",
        ),
        CV(
            label="DOID",
            full_name="Human Disease Ontology",
            version="2023",
            uri="https://www.ebi.ac.uk/ols/ontologies/doid",
        ),
        CV(
            label="LM",
            full_name="LipidMaps",
            version="2023",
            uri="https://www.lipidmaps.org",
        ),
    ],
    # Quantification units
    small_molecule_quantification_unit=Parameter(
        cv_label="MS", cv_accession="MS:1001839", name="area"
    ),
    small_molecule_feature_quantification_unit=Parameter(
        cv_label="MS", cv_accession="MS:1001839", name="area"
    ),
    # Identification reliability
    small_molecule_identification_reliability=Parameter(
        cv_label="MS",
        cv_accession="MS:1002896",
        name="compound identification confidence level",
    ),
    # Reference databases
    database=[
        Database(
            id=1,
            param=Parameter(cv_label="LM", name="LipidMaps"),
            prefix="LM",
            version="2023",
            uri="https://www.lipidmaps.org",
        ),
    ],
)

# ---------------------------------------------------------------------------
# SME rows — evidence per identification
# ---------------------------------------------------------------------------
sme_rows = [
    # PC(16:0/18:1)
    SmallMoleculeEvidence(
        sme_id=1,
        evidence_input_id="feat_001",
        database_identifier="LM:LMGP01010005",
        chemical_formula="C42H80NO8P",
        smiles="CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(=O)([O-])OCC[N+](C)(C)C)OC(=O)CCCCCCC/C=C\\CCCCCCCC",
        chemical_name="PC(16:0/18:1(9Z))",
        uri="https://www.lipidmaps.org/databases/lmsd/LMGP01010005",
        theoretical_neutral_mass=759.5778,
        spectra_ref=[SpectraRef(ms_run=1, reference="scan=1023")],
        identification_method=Parameter(
            cv_label="MS", cv_accession="MS:1001207", name="Mascot"
        ),
        ms_level=Parameter(
            cv_label="MS", cv_accession="MS:1000511", name="ms level", value="2"
        ),
        id_confidence_measure=[0.95],
        rank=1,
    ),
    # TG(16:0/18:1/18:2)
    SmallMoleculeEvidence(
        sme_id=2,
        evidence_input_id="feat_002",
        database_identifier="LM:LMGL03010001",
        chemical_formula="C55H100O6",
        smiles=None,
        chemical_name="TG(16:0/18:1/18:2)",
        uri="https://www.lipidmaps.org/databases/lmsd/LMGL03010001",
        theoretical_neutral_mass=872.7481,
        spectra_ref=[SpectraRef(ms_run=1, reference="scan=2045")],
        identification_method=Parameter(
            cv_label="MS", cv_accession="MS:1001207", name="Mascot"
        ),
        ms_level=Parameter(
            cv_label="MS", cv_accession="MS:1000511", name="ms level", value="2"
        ),
        id_confidence_measure=[0.87],
        rank=1,
    ),
]

# ---------------------------------------------------------------------------
# SMF rows — individual MS features
# ---------------------------------------------------------------------------
smf_rows = [
    # PC(16:0/18:1) [M+H]+, m/z 760.5856
    SmallMoleculeFeature(
        smf_id=1,
        sme_id_refs=[1],
        adduct_ion="[M+H]+",
        exp_mass_to_charge=760.5856,
        charge=1,
        retention_time_in_seconds=312.5,
        abundance_assay=[1.25e6, 1.18e6, 1.31e6, 2.45e6, 2.38e6, 2.51e6],
    ),
    # TG(16:0/18:1/18:2) [M+NH4]+, m/z 890.7749
    SmallMoleculeFeature(
        smf_id=2,
        sme_id_refs=[2],
        adduct_ion="[M+NH4]+",
        exp_mass_to_charge=890.7749,
        charge=1,
        retention_time_in_seconds=478.3,
        abundance_assay=[8.70e5, 9.10e5, 8.50e5, 3.20e6, 3.45e6, 3.10e6],
    ),
]

# ---------------------------------------------------------------------------
# SML rows — small molecule summary (one row per identified lipid)
# ---------------------------------------------------------------------------
sml_rows = [
    SmallMoleculeSummary(
        sml_id=1,
        smf_id_refs=[1],
        database_identifier=["LM:LMGP01010005"],
        chemical_formula=["C42H80NO8P"],
        smiles=["CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(=O)([O-])OCC[N+](C)(C)C)OC(=O)CCCCCCC/C=C\\CCCCCCCC"],
        inchi=["InChI=1S/C42H80NO8P/c1-6-7-8-9-10-11-12-13-14-15-16-17-18-19-26-38(44)"
               "-50-30-32(31-51-52(46,47)49-33-34-43(3,4)5)48-39(45)27-20-21-22-23-24-25-35-36-37(41)42/h13-14H,6-12,15-33,35-37H2,1-5H3"],
        chemical_name=["PC(16:0/18:1(9Z))"],
        uri=["https://www.lipidmaps.org/databases/lmsd/LMGP01010005"],
        theoretical_neutral_mass=[759.5778],
        adduct_ions=["[M+H]+"],
        reliability="2",
        best_id_confidence_measure=Parameter(
            cv_label="MS", cv_accession="MS:1002890", name="fragmentation score"
        ),
        best_id_confidence_value=0.95,
        abundance_assay=[1.25e6, 1.18e6, 1.31e6, 2.45e6, 2.38e6, 2.51e6],
    ),
    SmallMoleculeSummary(
        sml_id=2,
        smf_id_refs=[2],
        database_identifier=["LM:LMGL03010001"],
        chemical_formula=["C55H100O6"],
        smiles=["null"],
        inchi=["null"],
        chemical_name=["TG(16:0/18:1/18:2)"],
        uri=["https://www.lipidmaps.org/databases/lmsd/LMGL03010001"],
        theoretical_neutral_mass=[872.7481],
        adduct_ions=["[M+NH4]+"],
        reliability="2",
        best_id_confidence_measure=Parameter(
            cv_label="MS", cv_accession="MS:1002890", name="fragmentation score"
        ),
        best_id_confidence_value=0.87,
        abundance_assay=[8.70e5, 9.10e5, 8.50e5, 3.20e6, 3.45e6, 3.10e6],
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

print(f"Writing mzTab-M file to: {OUTPUT_FILE}")
context = mztabm.write(mztabm_obj, OUTPUT_FILE, format="tsv")

if context.success:
    print("File written successfully!")
    print(f"Output: {OUTPUT_FILE}")
else:
    print("Errors or warnings during writing:")
    for msg in context.messages:
        print(f"  {msg.message_type}: {msg.message}")
    # Still check if file was created
    if os.path.exists(OUTPUT_FILE):
        print(f"File was created despite warnings: {OUTPUT_FILE}")
    else:
        sys.exit(1)
