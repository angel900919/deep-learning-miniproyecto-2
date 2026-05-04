---
name: study-anchor
description: Interview the learner and write STUDY-ANCHOR.md — the immovable substrate decisions for a study subject (mode, goal, exam date, success criteria, retention strategy, source-of-truth policy). Pick CODE-LEARN (software/CS/AI) or CONCEPT-LEARN (general non-coding subjects). Use when starting a new subject, when no STUDY-ANCHOR.md exists, or when the user says "anchor this study", "set up study", "/study-anchor".
---

# study-anchor

Produce `STUDY-ANCHOR.md` at the study folder root. One-time, hand-aligned. Everything downstream reads this first.

## Process

1. **Check** — if `STUDY-ANCHOR.md` exists, read it and ask what to update. Don't overwrite without confirmation.

2. **Interview** — one question at a time, recommended answer each:
   - **Subject** — short kebab-case ID (e.g. `distributed-systems`, `linear-algebra`, `cfa-l1-ethics`)
   - **Mode** — `CODE-LEARN` (software/CS/AI — runnable code is part of the loop) or `CONCEPT-LEARN` (general subjects — derivations and worked problems instead of code)
   - **Why** — one sentence: what success looks like (pass an exam? Ship a project? Career pivot?)
   - **Deadline** — date or "ongoing"
   - **Bloom level target** per topic — Remember / Understand / Apply / Analyse / Evaluate / Create
   - **Time budget** — hours/week
   - **Retention strategy** — spaced repetition tool (Anki, Mochi, plain markdown queue), review cadence
   - **Source-of-truth policy** — when material conflicts (textbook vs lecture vs blog), which wins?
   - **Output format** — for CODE-LEARN: target stack/language; for CONCEPT-LEARN: notation/units convention
   - **Fallback policy** — when material is silent, may the agent answer from general knowledge? If yes, how must it flag the answer?

3. **Confirm** the choices in plain English. Wait for "yes".

4. **Write `STUDY-ANCHOR.md`** using the template below.

5. **Write `AGENTS.md`** at the study root telling the agent to read STUDY-ANCHOR + GLOSSARY + the relevant topic CONTEXT before answering anything.

6. **Bootstrap the folder skeleton** if it doesn't exist (see `agentic_study/template/`).

## Template

```markdown
# Study anchor — <subject>

## Mode
CODE-LEARN | CONCEPT-LEARN

## Why
<one sentence>

## Deadline
<date | ongoing>

## Bloom target
- <topic>: <Remember | Understand | Apply | Analyse | Evaluate | Create>
- <topic>: ...

## Time budget
<hours/week>

## Retention
- Spaced-rep tool: <name>
- Review cadence: <e.g. daily 15 min>

## Source-of-truth policy
When sources conflict, the order is:
1. <e.g. course textbook>
2. <e.g. official spec>
3. <e.g. lecturer notes>
4. <general knowledge — flagged as such>

## Output format (CODE-LEARN only)
- Target language: <e.g. Python 3.12>
- Convention: <PEP 8, type hints, docstrings>

## Notation (CONCEPT-LEARN only)
- Units: <SI | imperial>
- Symbols: <e.g. ASA notation, prefer Greek for angles>

## Fallback policy
- May the agent answer from general knowledge when material is silent? YES | NO
- If YES, every fallback answer MUST start with: `[OUTSIDE MATERIAL]` and cite the gap.
```

## Constraints

- Force decisions; reject "we'll figure that out later".
- Bloom target shapes everything — Apply demands worked examples; Analyse demands compare/contrast; Create demands projects.
- The fallback policy is load-bearing for every Q&A skill downstream.
- Cap output at 80 lines.

## Anti-patterns

- Skipping the Why. A studyfolder without an outcome rots.
- Picking both modes. Split into two subjects.
- Setting Bloom = Create on day one. Climb the ladder.
