---
name: carpentries-translation
description: >
  Translates Carpentries lesson .Rmd files into any target language while
  preserving all technical markup intact. Handles Pandoc Fenced Divs callout
  blocks (objectives, challenge, solution, keypoints, etc.), R code chunks,
  inline backtick code, URLs, YAML frontmatter, R/Pandoc citations, and
  cross-references. Use this skill whenever the user asks to translate a
  Carpentries episode, lesson, or .Rmd file — even if they just say "translate
  this" or "翻訳して" without mentioning the file format explicitly.
---

# Carpentries Lesson Translation

Carpentries lessons are written in R Markdown (.Rmd) using Pandoc's Fenced
Divs to create structured callout blocks (challenges, solutions, objectives,
etc.). The goal is to translate all human-readable prose into the target
language while leaving every piece of technical syntax exactly as it appears
in the source — character for character.

## Workflow

1. **Read the file** — Read the entire .Rmd before starting.
2. **Confirm the target language** — Ask if not specified.
3. **Translate sequentially** — Work top to bottom. For files over ~400 lines,
   output in clearly marked chunks and confirm with the user before continuing.
4. **Write the output file** — Follow the user's naming convention, or default
   to inserting the language code before `.Rmd` (e.g., `40-visualization.ja.Rmd`).
5. **Report** — After writing, note any ambiguous elements that may need human review.

---

## What to Translate

- Prose paragraphs and narrative sentences
- Section headings — translate the text; keep the `#` / `##` / `###` markers
- Bullet and numbered list text
- Block quote content — keep the `>` prefix, translate the text
- YAML `title:` value (only this key among all YAML fields)
- Link display text: `[translate this part](keep-url-unchanged)`
- `fig.alt="..."` and `fig.cap="..."` values inside code chunk headers — these
  are human-readable accessibility text
- Text content inside Fenced Div callout blocks (see rules below)
- Heading text inside callout blocks, e.g., `## Challenge`, `## Solution`

---

## What NOT to Translate — Preserve Exactly As-Is

### YAML Frontmatter
The entire `---` block at the top. Only `title:` is translatable. All other
keys and values (`source`, `teaching`, `exercises`, etc.) stay unchanged.

```
---
source: Rmd
title: Data visualization   ← translate this value only
teaching: 60
exercises: 60
---
```

### R Code Chunks
Preserve everything from the opening ` ```{r ` to the closing ` ``` `,
including the chunk name and all chunk options. The R code inside is never
translated.

The only exception: `fig.alt="..."` and `fig.cap="..."` string values in the
chunk header are human-readable — translate those strings in-place.

**Example (translating to Japanese):**
````
```{r boxplot, cache=FALSE, purl=TRUE, fig.alt="Boxplot showing expression values."}
ggplot(data = rna, mapping = aes(y = expression_log, x = sample)) +
  geom_boxplot()
```
````
becomes:
````
```{r boxplot, cache=FALSE, purl=TRUE, fig.alt="各サンプルの発現量を示すボックスプロット。"}
ggplot(data = rna, mapping = aes(y = expression_log, x = sample)) +
  geom_boxplot()
```
````

### Fenced Div Callout Blocks — Delimiters and Class Names
The colon sequences and class names must be preserved character-for-character.
Only the prose content between the delimiters is translated.

```
:::::::::::::::::::::::::::::::::::::::  challenge    ← preserve exactly

## Challenge                                          ← translate heading text

Prose to translate...

:::::::::::::::  solution                             ← preserve exactly

## Solution                                           ← translate heading text

Solution prose to translate...

:::::::::::::::::::::::::                             ← preserve exactly

::::::::::::::::::::::::::::::::::::::::::::::::::    ← preserve exactly
```

Valid class names (never translate these identifiers):
`objectives`, `questions`, `challenge`, `solution`, `callout`, `keypoints`,
`prereq`, `checklist`, `discussion`, `testimonial`, `instructor`, `caution`,
`warning`, `tip`

### Inline Code
Anything inside single backticks is never translated:
`` `geom_point()` ``, `` `tidyverse` ``, `` `rna_fc` ``, `` `TRUE` ``

### Plain (Non-R) Code Blocks
Fenced blocks without `{r ...}` are preserved entirely:
````
```
ggplot(data = <DATA>, mapping = aes(<MAPPINGS>)) + <GEOM_FUNCTION>()
```
````

### URLs
In `[text](URL)`, never touch the URL. Translate the display text only if it
is natural-language prose. If the display text is itself a URL, preserve it:
- `[Data Visualization Cheat Sheet](https://raw.githubusercontent.com/...)` →
  translate "Data Visualization Cheat Sheet"
- `[https://ggplot2.tidyverse.org](https://ggplot2.tidyverse.org)` →
  preserve both parts as-is

### R/Pandoc Citations
`@Wilkinson:2005`, `@ggplot2book` — preserve exactly.

### Cross-References
`@ref(fig:paintermodel)`, `@ref(tab:...)` — preserve exactly.

### Footnote Labels
`[^label]` in-text references and `[^label]:` definitions — preserve the
label identifier; translate only the definition prose.

### Package and Function Names Mentioned in Prose
Proper names of R packages and functions are technical identifiers, not
ordinary words. Do not translate them even when they appear without backticks:
`ggplot2`, `tidyverse`, `patchwork`, `dplyr`, `geom_point()`, `facet_wrap()`.

When styled as `` **`ggplot2`** `` (bold + backtick), preserve both the
`**` markers and the backtick content.

---

## Common Edge Cases

| Pattern | Action |
|---|---|
| `> This episode is based on ...` | Translate the prose after `>` |
| `[^footnote_label]` in text | Preserve the label |
| `(@Wilkinson:2005)` in sentence | Preserve the citation |
| `*Grammar of Graphics*` (italic title) | Translate if it has a natural-language equivalent; otherwise keep |
| `## Challenge` inside a callout | Translate the heading text |
| `fig.alt="..."` in chunk header | Translate the string value |
| Variable names like `rna_fc` in prose | Keep as-is (code identifier) |
| Package names like **`ggplot2`** | Keep as-is |
| `install.packages("hexbin")` in prose | Keep as-is (code) |

---

## Output Naming Convention

| Target language | Default filename |
|---|---|
| Japanese (ja) | `<basename>.ja.Rmd` |
| Spanish (es) | `<basename>.es.Rmd` |
| French (fr) | `<basename>.fr.Rmd` |
| Other | `<basename>.<lang-code>.Rmd` |

If the Carpentries project uses a different structure (e.g., `locale/ja/episodes/`),
follow the user's instruction.
