---
name: mztab-m-writer
description: >
  Create mzTab-M files from scratch using the pymzTab-m Python library. Use this skill whenever a
  metabolomics or lipidomics researcher wants to create, generate, or write an mzTab-M file for their
  study data — even if they just say "make an mzTab file", "create a mzTab-M for my experiment",
  "I need to export my data to mzTab format", or "help me fill in the metadata for my mzTab". The
  skill guides the user through gathering study details, building the Metadata section, assembling
  the molecule tables (SML, SMF, SME), and writing a valid .mztab file.
---

# mzTab-M File Creator

This skill guides you through building a valid mzTab-M (version 2.0.0-M) file from scratch using the
`pymzTab-m` Python library (`mztab_m_io`).

mzTab-M is a tab-separated text format used to report quantitative results from metabolomics and
lipidomics experiments. It has four sections:
- **MTD** (Metadata) — study info, instruments, samples, software. **Required.**
- **SML** (Small Molecule Summary) — one row per identified molecule. **Required.**
- **SMF** (Small Molecule Feature) — individual MS features (m/z, RT, adducts). Recommended.
- **SME** (Small Molecule Evidence) — database search evidence per identification. Recommended.

---

## Step 1: Interview the user

Before writing any code, ask the user for the information below. You don't need everything — gather
what they have and use sensible defaults or `null` for optional fields.

**Required information:**
- `mzTab-ID`: a short unique ID for this file (e.g., a MetaboLights accession like `MTBLS263`, or an
  internal lab ID like `LAB001_batch3`)
- Software used for data processing (name and version, e.g., "MZmine 3.9", "XCMS 3.18", "MS-DIAL 5.0")
- MS run file locations (file paths or URLs to the raw .mzML or .raw files)
- Quantification method (e.g., "LC-MS label-free", "DDA", "targeted MRM")
- Assay/study variable structure: how many assays, how replicates are grouped

**Helpful but optional:**
- Study title and description
- Contact name(s), affiliation(s), email(s)
- Publication DOI or PubMed ID
- Instrument name, ion source, mass analyzer
- Sample details (species, tissue, disease, treatment)
- Sample processing steps
- Reference database(s) used for identification (e.g., HMDB, LipidMaps, ChEBI)
- Identification confidence measure (e.g., fragmentation score)

---

## Step 2: Build the Metadata section

The `Metadata` object is the most complex part. Here is the standard pattern:

```python
from mztab_m_io.model.common import (
    CV, Assay, Contact, Database, Instrument, MsRun,
    Parameter, Publication, Sample, SampleProcessing, Software, StudyVariable, Uri,
)
from mztab_m_io.model.section.mtd import Metadata

metadata = Metadata(
    mztab_version="2.0.0-M",         # always use this exact string
    mztab_id="YOUR_STUDY_ID",        # e.g., "MTBLS263" or "LAB001_batch3"
    title="Your Study Title",         # optional but recommended
    description="Detailed description of your study...",  # optional

    # --- REQUIRED: quantification method ---
    # Use a CV term from the PSI-MS ontology (MS:) when possible.
    # Common examples:
    #   MS:1001834 = LC-MS label-free quantitation analysis
    #   MS:1001335 = selected reaction monitoring (SRM/MRM)
    #   MS:1002038 = unlabeled sample (untargeted)
    quantification_method=Parameter(
        cv_label="MS",
        cv_accession="MS:1001834",
        name="LC-MS label-free quantitation analysis",
    ),

    # --- REQUIRED: at least one software entry ---
    software=[
        Software(id=1, parameter=Parameter(
            cv_label="MS",
            cv_accession="MS:1002342",   # use CV term if known, else just name=
            name="MZmine",
            value="3.9",
        )),
    ],

    # --- REQUIRED: MS run file locations ---
    ms_run=[
        MsRun(
            id=1,
            location="file://path/to/sample1_pos.mzML",
            format=Parameter(cv_label="MS", cv_accession="MS:1000584", name="mzML file"),
            id_format=Parameter(cv_label="MS", cv_accession="MS:1001530", name="mzML native ID format"),
            scan_polarity=[Parameter(cv_label="MS", cv_accession="MS:1000130", name="positive scan")],
        ),
    ],

    # --- REQUIRED: at least one assay (links samples to MS runs) ---
    assay=[
        Assay(id=1, name="sample_A_replicate_1", ms_run_ref=[1]),
    ],

    # --- REQUIRED: at least one study variable (groups assays) ---
    study_variable=[
        StudyVariable(
            id=1,
            name="control",
            assay_refs=[1],
            description="Control group",
        ),
    ],

    # --- REQUIRED: controlled vocabulary declarations ---
    # List every CV prefix used in Parameter objects above.
    cv=[
        CV(
            label="MS",
            full_name="Mass Spectrometry Ontology",
            version="4.1.38",
            uri="https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo",
        ),
    ],

    # --- REQUIRED: quantification units ---
    small_molecule_quantification_unit=Parameter(
        cv_label="MS", cv_accession="MS:1001839", name="area",
    ),
    small_molecule_feature_quantification_unit=Parameter(
        cv_label="MS", cv_accession="MS:1001839", name="area",
    ),

    # --- REQUIRED: identification reliability level ---
    small_molecule_identification_reliability=Parameter(
        cv_label="MS", cv_accession="MS:1002896",
        name="compound identification confidence level",
    ),

    # --- RECOMMENDED: reference database ---
    database=[
        Database(
            id=1,
            param=Parameter(cv_label="MTBLS", name="HMDB"),
            prefix="HMDB",
            version="5.0",
            uri="https://hmdb.ca",
        ),
    ],
)
```

### Adding contacts and samples (optional)

```python
from mztab_m_io.model.common import Contact, Sample

metadata.contact = [
    Contact(id=1, name="Jane Smith", affiliation="University of Somewhere",
            email="jane.smith@university.edu"),
]

metadata.sample = [
    Sample(
        id=1,
        name="plasma_control",
        species=[Parameter(cv_label="NCBITAXON", cv_accession="NCBITaxon:9606", name="Homo sapiens")],
        tissue=[Parameter(cv_label="BTO", cv_accession="BTO:0000131", name="blood plasma")],
        disease=[Parameter(cv_label="DOID", cv_accession="DOID:0000000", name="normal")],
    ),
]
```

### Using `Parameter` correctly

`Parameter` represents a CV-term-tagged value. The format in the file is `[cv_label, cv_accession, name, value]`.

```python
# With CV term (preferred):
Parameter(cv_label="MS", cv_accession="MS:1000130", name="positive scan")

# With free text (when no CV term exists):
Parameter(name="in-house method", value="custom notes")

# With a value:
Parameter(cv_label="MS", cv_accession="MS:1000031", name="instrument model", value="Q Exactive HF")
```

Common CV prefixes to declare in `cv=`:
| Prefix | Ontology | Common use |
|--------|----------|-----------|
| MS | PSI-MS | instruments, ionization, software |
| NCBITAXON | NCBI Taxonomy | species |
| BTO | BRENDA Tissue | tissues |
| DOID | Disease Ontology | diseases |
| CHEBI | ChEBI | small molecules |
| HMDB | HMDB | metabolites |
| LM | LipidMaps | lipids |

---

## Step 3: Build the molecule tables

### Small Molecule Summary (SML) — required

```python
from mztab_m_io.model.section.sml import SmallMoleculeSummary

sml_rows = [
    SmallMoleculeSummary(
        sml_id=1,
        smf_id_refs=[1],          # references to SMF rows
        database_identifier=["HMDB:HMDB0000122"],
        chemical_formula=["C6H12O6"],
        smiles=["OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O"],
        inchi=["InChI=1S/C6H12O6/..."],
        chemical_name=["glucose"],
        uri=["https://hmdb.ca/metabolites/HMDB0000122"],
        theoretical_neutral_mass=[180.0634],
        adduct_ions=["[M+H]+"],
        reliability="1",          # 1=confirmed, 2=probable, 3=putative, 4=unequivocal
        best_id_confidence_measure=Parameter(
            cv_label="MS", cv_accession="MS:1002890", name="fragmentation score"
        ),
        best_id_confidence_value=0.92,
        # abundance columns: one per assay, named abundance_assay[N]
        abundance_assay={1: 125000.0},
    ),
]
```

### Small Molecule Feature (SMF) — recommended

```python
from mztab_m_io.model.section.smf import SmallMoleculeFeature

smf_rows = [
    SmallMoleculeFeature(
        smf_id=1,
        sme_id_refs=[1],          # references to SME rows (if available)
        adduct_ion="[M+H]+",
        exp_mass_to_charge=181.0712,
        charge=1,
        retention_time_in_seconds=312.5,
        abundance_assay={1: 125000.0},
    ),
]
```

### Small Molecule Evidence (SME) — recommended

```python
from mztab_m_io.model.section.sme import SmallMoleculeEvidence

sme_rows = [
    SmallMoleculeEvidence(
        sme_id=1,
        evidence_input_id="feat_001",
        database_identifier="HMDB:HMDB0000122",
        chemical_formula="C6H12O6",
        smiles="OC[C@H]1OC(O)...",
        chemical_name="glucose",
        uri="https://hmdb.ca/metabolites/HMDB0000122",
        theoretical_neutral_mass=180.0634,
        spectra_ref="ms_run[1]:scan=1234",
        identification_method=Parameter(
            cv_label="MS", cv_accession="MS:1001207", name="Mascot"
        ),
        ms_level=Parameter(cv_label="MS", cv_accession="MS:1000511", name="ms level", value="2"),
        id_confidence_measure=[0.92],
        rank=1,
    ),
]
```

---

## Step 4: Assemble and write the file

```python
import mztab_m_io as mztabm
from mztab_m_io.model.mztabm import MzTabM

mztabm_obj = MzTabM(
    metadata=metadata,
    small_molecule_summary=sml_rows,
    small_molecule_feature=smf_rows,       # optional
    small_molecule_evidence=sme_rows,       # optional
)

# Write to TSV (.mztab) — the standard format
context = mztabm.write(mztabm_obj, "output.mztab", format="tsv")

# Or write to JSON or YAML
# context = mztabm.write(mztabm_obj, "output.json", format="json")

if context.success:
    print("File written successfully!")
else:
    for msg in context.messages:
        print(f"{msg.message_type}: {msg.message}")
```

---

## Validation tips

- **`StudyVariable` needs an explicit `id`**: `StudyVariable(id=1, name=..., assay_refs=[1])` — the `id` field is often forgotten.
- **`ms_run_ref` is a list of integers** matching `MsRun.id` values: `Assay(id=1, ms_run_ref=[1, 2])`.
- **`assay_refs` is a list of integers** matching `Assay.id` values.
- **`sml_id_refs` and `smf_id_refs`**: SML rows reference SMF IDs, SMF rows reference SME IDs.
- **All `id` fields must be sequential integers** starting from 1.
- **Every `cv_label` prefix used** must be declared in `metadata.cv`.
- If there are validation errors, check `context.messages` — each message includes the field path and reason.

---

## Minimal working example

```python
import mztab_m_io as mztabm
from mztab_m_io.model.common import CV, Assay, Database, MsRun, Parameter, Software, StudyVariable
from mztab_m_io.model.section.mtd import Metadata
from mztab_m_io.model.section.sml import SmallMoleculeSummary
from mztab_m_io.model.mztabm import MzTabM

metadata = Metadata(
    mztab_version="2.0.0-M",
    mztab_id="MY_STUDY_001",
    quantification_method=Parameter(cv_label="MS", cv_accession="MS:1001834",
                                    name="LC-MS label-free quantitation analysis"),
    software=[Software(id=1, parameter=Parameter(name="MZmine", value="3.9"))],
    ms_run=[MsRun(id=1, location="file:///data/sample1.mzML")],
    assay=[Assay(id=1, name="sample_1", ms_run_ref=[1])],
    study_variable=[StudyVariable(id=1, name="group_A", assay_refs=[1])],
    cv=[CV(label="MS", full_name="Mass Spectrometry Ontology", version="4.1.38",
           uri="https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo")],
    small_molecule_quantification_unit=Parameter(cv_label="MS", cv_accession="MS:1001839", name="area"),
    small_molecule_feature_quantification_unit=Parameter(cv_label="MS", cv_accession="MS:1001839", name="area"),
    small_molecule_identification_reliability=Parameter(cv_label="MS", cv_accession="MS:1002896",
                                                        name="compound identification confidence level"),
    database=[Database(id=1, param=Parameter(name="HMDB"), prefix="HMDB", version="5.0",
                       uri="https://hmdb.ca")],
)

sml = [
    SmallMoleculeSummary(
        sml_id=1,
        database_identifier=["HMDB:HMDB0000122"],
        chemical_name=["glucose"],
        reliability="1",
        abundance_assay={1: 125000.0},
    )
]

mztabm_obj = MzTabM(metadata=metadata, small_molecule_summary=sml)
context = mztabm.write(mztabm_obj, "my_study.mztab", format="tsv")
print("Done!" if context.success else context.messages)
```
