"""
Minimal valid mzTab-M file for a plasma metabolomics study.

Study ID: LAB_2026_plasma
Software: MZmine 3.9
MS run: plasma_run1.mzML
Sample group: one sample group (plasma)
"""

import os
import sys

# Ensure the pymzTab-m library is on the path
repo_path = "/Users/knishida/Documents/GitHub/pymzTab-m"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import mztab_m_io as mztabm
from mztab_m_io.model.common import (
    CV, Assay, Database, MsRun, Parameter, Software, StudyVariable,
)
from mztab_m_io.model.section.mtd import Metadata
from mztab_m_io.model.section.sml import SmallMoleculeSummary
from mztab_m_io.model.mztabm import MzTabM

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
metadata = Metadata(
    mztab_version="2.0.0-M",
    mztab_id="LAB_2026_plasma",

    # Required: quantification method
    quantification_method=Parameter(
        cv_label="MS",
        cv_accession="MS:1001834",
        name="LC-MS label-free quantitation analysis",
    ),

    # Required: software
    software=[
        Software(
            id=1,
            parameter=Parameter(
                cv_label="MS",
                cv_accession="MS:1002342",
                name="MZmine",
                value="3.9",
            ),
        ),
    ],

    # Required: MS run file(s)
    ms_run=[
        MsRun(
            id=1,
            location="file://plasma_run1.mzML",
            format=Parameter(
                cv_label="MS",
                cv_accession="MS:1000584",
                name="mzML file",
            ),
            id_format=Parameter(
                cv_label="MS",
                cv_accession="MS:1001530",
                name="mzML native ID format",
            ),
        ),
    ],

    # Required: assay (links sample to MS run)
    assay=[
        Assay(id=1, name="plasma_assay_1", ms_run_ref=[1]),
    ],

    # Required: study variable (one sample group)
    study_variable=[
        StudyVariable(
            id=1,
            name="plasma_group",
            assay_refs=[1],
            description="Plasma sample group",
        ),
    ],

    # Required: CV declarations
    cv=[
        CV(
            label="MS",
            full_name="Mass Spectrometry Ontology",
            version="4.1.38",
            uri="https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo",
        ),
    ],

    # Required: quantification units
    small_molecule_quantification_unit=Parameter(
        cv_label="MS",
        cv_accession="MS:1001839",
        name="area",
    ),
    small_molecule_feature_quantification_unit=Parameter(
        cv_label="MS",
        cv_accession="MS:1001839",
        name="area",
    ),

    # Required: identification reliability
    small_molecule_identification_reliability=Parameter(
        cv_label="MS",
        cv_accession="MS:1002896",
        name="compound identification confidence level",
    ),

    # Recommended: database
    database=[
        Database(
            id=1,
            param=Parameter(name="no database"),
            prefix="null",
            version="Unknown",
            uri="null",
        ),
    ],
)

# ---------------------------------------------------------------------------
# Small Molecule Summary (SML) — required, at least one placeholder row
# ---------------------------------------------------------------------------
sml = [
    SmallMoleculeSummary(
        sml_id=1,
        database_identifier=["null"],
        chemical_name=["unknown"],
        reliability="4",                 # 4 = unequivocal mass spectrometry evidence
        abundance_assay=[None],            # no abundance yet; researcher will fill in
    ),
]

# ---------------------------------------------------------------------------
# Assemble and write
# ---------------------------------------------------------------------------
output_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(output_dir, "LAB_2026_plasma.mztab")

mztabm_obj = MzTabM(
    metadata=metadata,
    small_molecule_summary=sml,
)

context = mztabm.write(mztabm_obj, output_file, format="tsv")

if context.success:
    print(f"mzTab-M file written successfully: {output_file}")
else:
    print("Errors encountered:")
    for msg in context.messages:
        print(f"  [{msg.message_type}] {msg.message}")
    sys.exit(1)
