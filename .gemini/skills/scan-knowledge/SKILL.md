---
name: scan-knowledge
description: Scan and index the entire study folder (material/, topics/, notes/, exams/) and answer questions from it. After running, the user can /ask <question>, /code-from-material <task>, or just ask freely — answers are grounded in the corpus and explicitly flagged when they fall back to general knowledge. Use first thing in any new study session, after major /ingest-material runs, or when the user says "/scan-knowledge", "load my notes", "ready to study".
---

# scan-knowledge

Index the study folder and become a grounded Q&A interface for the corpus. This is the skill the user runs once per session before any question-answering.

## Inputs required

- `STUDY-ANCHOR.md` (mode + fallback policy)
- `GLOSSARY.md`
- `.study/ingestion-log.md`
- The whole study folder structure

## Process

1. **Build the index** in working memory. Walk:
   - `topics/*/CONTEXT.md` — topic map
   - `topics/*/concepts/*.md` — concept inventory
   - `topics/*/mental-models.md` — mental models
   - `topics/*/flashcards.md` — atomic facts
   - `material/` — raw sources (note paths and headings only; don't load contents)
   - `notes/` — user-synthesised notes
   - `exams/` — past papers + post-mortems
   - `GLOSSARY.md` — vocabulary spine
   - `.study/progress-tracker.md` — mastery state

2. **Confirm the index** — print: "Indexed N topics, M concepts, K material files. Ask away."

3. **For every question, answer in this priority order:**
   1. **Exact match in concepts/glossary** — quote and cite
   2. **Synthesis from multiple concept files** — cite each source
   3. **Material-direct lookup** — open the cited material file, quote the relevant span, cite
   4. **Mental-model-based derivation** — "from mental-models.md model X, the derivation is…"
   5. **Fallback to general knowledge** — *only* if STUDY-ANCHOR.fallback_policy = YES, and the answer MUST start with `[OUTSIDE MATERIAL]` and name the gap

4. **Always cite.** Format: `(source: topics/<topic>/concepts/<id>.md)` or `(source: material/<path>:L<line>)`.

5. **Flag conflicts** — if two sources disagree, surface both with the source-of-truth policy applied.

6. **Capture stuck questions** — if the user can't get a satisfying answer, append to `.study/current-questions.md` for later resolution. These become candidates for new ingestion or new concepts.

## Output format for an answer

```
<answer text>

Sources:
- topics/<topic>/concepts/<concept>.md
- material/<file>:L<line>

[OUTSIDE MATERIAL]   ← only if fallback was used; lists the gap.
```

## Constraints

- **No silent fallback.** Every general-knowledge answer is flagged. No exceptions.
- **Citations are mandatory** for in-corpus answers.
- **Don't load full material files into context up front.** Index headings and locations; open files on demand.
- **Volume the index**, don't quote it. The user should see "Indexed N/M/K", not the full list.
- **Conflicts are surfaced**, not silently resolved.

## Anti-patterns

- Answering from training data without flagging when the corpus has the answer. This is the worst failure mode.
- Pretending coverage. If the corpus doesn't address the question, say so and offer to ingest or extract.
- Long preambles before the answer. Cite the source first if it's a direct hit; otherwise show the synthesis steps.

## Composes with

- `/code-from-material` — same grounded retrieval, output is code
- `/grill-on-topic` — same index, output is questions FOR the user
- `/explain-back` — same index, the user explains and the agent grades
