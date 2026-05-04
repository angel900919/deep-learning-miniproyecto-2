---
name: extract-concepts
description: Read material indexed under a topic and produce one topics/<topic>/concepts/<concept>.md per distinct idea — definition, why-it-matters, prerequisites, common confusions, source citations. Each concept is a self-contained study unit. Use after /ingest-material on new files, when the user says "/extract-concepts", "what are the key concepts in X", or before /mental-model or /make-flashcards.
---

# extract-concepts

Walk the source materials for a topic and produce one `concepts/<concept>.md` per distinct idea. Concepts are the atomic units everything downstream points at.

## Inputs required

- `topics/<topic>/CONTEXT.md` (lists source materials)
- The actual material files
- `GLOSSARY.md`
- `STUDY-ANCHOR.md` (for Bloom target)

## Process

1. **Inventory pass** — read every source material listed in `CONTEXT.md`. Extract a flat list of every distinct idea the material treats as important. Don't filter yet.

2. **Consolidate duplicates** — three lectures that all cover "the CAP theorem" produce one concept file, not three.

3. **Promote to glossary** — if a concept introduces a new term not in `GLOSSARY.md`, add it there.

4. **For each concept, write `concepts/<concept-id>.md`** using the template below. **Hard cap: 120 lines per concept.**

5. **Cite every claim** by source path + line/page/timestamp. Untraceable claims get `[CITATION NEEDED]` — do not silently invent.

6. **Update `topics/<topic>/CONTEXT.md`** Key concepts section with the resulting list.

7. **Suggest next steps** — for each concept, propose which downstream skill to run: `/mental-model` (for hard ideas), `/make-flashcards` (for facts), `/worked-example` or `/worked-problem` (for application-level).

## Template — `concepts/<concept-id>.md`

```markdown
# Concept: <name>

## One-liner
<one sentence a peer could understand>

## Prerequisites
- <other concept-id or external knowledge>

## Definition
<formal definition, ≤4 sentences. Use the canonical wording from the source.>

## Why it matters
<problem it solves; what changes when you understand it>

## Worked intuition
<3–6 sentences walking through the simplest non-trivial case>

## Common confusions
- People mistake X for Y because…
- The source warns against…

## Related concepts
- See also: <concept-id>, <concept-id>

## Citations
- material/lectures/<file>:L120 — <quote or paraphrase>
- material/readings/<file>:p.34 — <…>

## Suggested next steps
- /mental-model <this concept>
- /make-flashcards <this concept>
- /worked-example <this concept>  (CODE-LEARN)
- /worked-problem <this concept>  (CONCEPT-LEARN)
```

## Constraints

- One concept per file. A 5-concept lecture produces 5 files.
- Citations are mandatory. No citation = `[CITATION NEEDED]` placeholder, never silent gap.
- Don't paraphrase past the source's clarity — sometimes the source's exact wording IS the precision.
- Bloom-Apply or higher → must include "Worked intuition" or link to a worked example/problem.

## Anti-patterns

- Re-summarising the entire source as one giant concept. Atomise.
- Inventing connections the source didn't make. Use "Related" only when the source connects them or the connection is canonical in the field.
- Skipping common confusions. Those are the highest-value content.
