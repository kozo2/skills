---
name: cytoscape-automation
description: >
  Generate Python scripts using py4cytoscape to automate Cytoscape operations.
  Use this skill whenever the user wants to load networks into Cytoscape, apply
  visual styles or layouts, map node/edge attributes to visual properties, or
  import style files — even if they just say "automate Cytoscape", "py4cytoscape
  script", "load my network in Cytoscape", "style my network", or "apply a
  layout in Cytoscape". Always use this skill for any task involving py4cytoscape
  or Cytoscape automation via Python.
---

# Cytoscape Automation Skill

Generate correct, runnable Python scripts using **py4cytoscape** (v1.13+) to automate Cytoscape. Cytoscape is assumed to already be running locally on the default port (1234).

## Setup Boilerplate

Always begin scripts with:

```python
import py4cytoscape as p4c
import pandas as pd

# Verify connection (Cytoscape must be running)
p4c.cytoscape_ping()
print("Cytoscape version:", p4c.cytoscape_version_info())
```

---

## 1. Loading / Importing Networks

### From a SIF file

```python
network_suid = p4c.import_network_from_file("path/to/network.sif")
```

### From a CSV/TSV edge list

Use pandas to load and pass as a DataFrame:

```python
df = pd.read_csv("edges.csv")  # columns: source, target, [weight, ...]
# Required columns: 'source' and 'target' (node names as strings)
network_suid = p4c.create_network_from_data_frames(
    edges=df,
    title="My Network",
    collection="My Collection"
)
```

### From a Pandas DataFrame (in-memory)

```python
nodes = pd.DataFrame({
    'id': ['A', 'B', 'C'],
    'group': ['kinase', 'tf', 'kinase'],
    'score': [0.9, 0.5, 0.8]
})
edges = pd.DataFrame({
    'source': ['A', 'B'],
    'target': ['B', 'C'],
    'weight': [1.0, 0.7]
})
network_suid = p4c.create_network_from_data_frames(
    nodes=nodes,
    edges=edges,
    title="My Network"
)
```

**Key notes:**
- `id` column in nodes DataFrame = node name
- `source`/`target` in edges DataFrame must match node `id` values
- Extra columns become node/edge attributes automatically

---

## 2. Applying Styles

### Create a new style

```python
style_name = "MyStyle"
p4c.create_visual_style(style_name)
p4c.set_visual_style(style_name)
```

### Set default visual properties

```python
p4c.set_node_color_default("#AED6F1", style_name=style_name)
p4c.set_node_size_default(50, style_name=style_name)
p4c.set_node_shape_default("ELLIPSE", style_name=style_name)
p4c.set_edge_line_width_default(2.0, style_name=style_name)
p4c.set_edge_color_default("#888888", style_name=style_name)
```

Valid node shapes: `ELLIPSE`, `RECTANGLE`, `TRIANGLE`, `DIAMOND`, `HEXAGON`, `OCTAGON`, `PARALLELOGRAM`, `ROUND_RECTANGLE`, `VEE`

### Import a .xml style file

```python
p4c.import_visual_styles("path/to/mystyle.xml")
p4c.set_visual_style("StyleNameFromXml")
```

---

## 3. Attribute Mappings

Map node/edge data columns to visual properties.

### Continuous mapping (numeric → visual property)

```python
# Map 'score' (0.0–1.0) to node size (20–80)
p4c.set_node_size_mapping(
    table_column='score',
    table_column_values=[0.0, 1.0],
    sizes=[20, 80],
    mapping_type='c',  # 'c' = continuous
    style_name=style_name
)

# Map 'weight' to edge width
p4c.set_edge_line_width_mapping(
    table_column='weight',
    table_column_values=[0.0, 1.0],
    widths=[1, 8],
    mapping_type='c',
    style_name=style_name
)
```

### Discrete mapping (categorical → visual property)

```python
# Map 'group' column to node color
p4c.set_node_color_mapping(
    table_column='group',
    table_column_values=['kinase', 'tf'],
    colors=['#E74C3C', '#2ECC71'],
    mapping_type='d',  # 'd' = discrete
    style_name=style_name
)

# Map 'group' to node shape
p4c.set_node_shape_mapping(
    table_column='group',
    table_column_values=['kinase', 'tf'],
    shapes=['ELLIPSE', 'DIAMOND'],
    mapping_type='d',
    style_name=style_name
)
```

### Passthrough mapping (column value → label)

```python
# Use node 'id' as label
p4c.set_node_label_mapping(
    table_column='id',
    mapping_type='p',  # 'p' = passthrough
    style_name=style_name
)
```

### Auto-mapping (let py4cytoscape pick colors/sizes)

```python
# Auto-assign colors to discrete column values
p4c.set_node_color_mapping(
    **p4c.gen_node_color_map('group', mapping_type='d'),
    style_name=style_name
)
```

---

## 4. Layouts

```python
# Force-directed (default Cytoscape layout)
p4c.layout_network("force-directed")

# Hierarchical
p4c.layout_network("hierarchical")

# Grid
p4c.layout_network("grid")

# Circular
p4c.layout_network("circular")

# Prefuse Force Directed (with options)
p4c.layout_network("prefuse-force-directed", network=network_suid)

# List all available layouts
print(p4c.get_layout_names())
```

To pass layout options:

```python
p4c.layout_network(
    layout_name="force-directed",
    params={"numIterations": 500, "defaultSpringCoefficient": 5e-4}
)
```

---

## 5. Common Patterns

### Full workflow: load CSV → style → layout

```python
import py4cytoscape as p4c
import pandas as pd

p4c.cytoscape_ping()

# Load
df = pd.read_csv("edges.tsv", sep="\t")
suid = p4c.create_network_from_data_frames(edges=df, title="My Network")

# Style
style = "WorkflowStyle"
p4c.create_visual_style(style)
p4c.set_node_color_default("#AED6F1", style_name=style)
p4c.set_node_label_mapping(table_column='name', mapping_type='p', style_name=style)
p4c.set_visual_style(style)

# Layout
p4c.layout_network("force-directed")
```

### Get/set node table data

```python
# Read node table
node_table = p4c.get_table_columns(table="node")

# Add new attribute column
p4c.load_table_data(
    pd.DataFrame({'id': ['A', 'B'], 'pvalue': [0.01, 0.05]}),
    data_key_column='id',
    table_key_column='name',
    table='node'
)
```

---

## Tips

- Always call `p4c.cytoscape_ping()` at the top to confirm connection.
- `network_suid` (integer) uniquely identifies a network; pass it to functions when working with multiple networks.
- Style names are case-sensitive.
- Column names in mappings must exactly match column names in the Cytoscape node/edge table.
- For remote/Jupyter use, enable sandboxing: `p4c.sandbox_set("MySandbox")` and use sandbox paths.
