---
name: code-from-material
description: CODE-LEARN only. Generate code grounded strictly in the indexed study corpus — concepts, mental models, worked examples, code samples — citing every borrowed pattern. Falls back to general knowledge ONLY when corpus is silent, with [OUTSIDE MATERIAL] flag. Use when the user says "/code-from-material", "write X using my notes", "build Y from this material", or after /scan-knowledge has indexed the corpus.
---

# code-from-material (CODE-LEARN)

Generate code where every non-trivial pattern is traced to the corpus. The output is correct from the corpus's point of view, with explicit flags wherever it had to leave the material.

## Inputs required

- The user's task (what to build)
- `STUDY-ANCHOR.md` (mode = CODE-LEARN, target language, fallback policy)
- `/scan-knowledge` index (run it first if not already loaded)

## Process

1. **Confirm mode** — must be CODE-LEARN.

2. **Decompose the task** into the minimum set of concepts it requires.

3. **For each concept, retrieve the corpus material:**
   - `topics/<topic>/concepts/<id>.md` — the definition
   - `topics/<topic>/mental-models.md` — the reasoning frame
   - `topics/<topic>/examples/*` — the canonical implementations
   - `material/code-samples/` — the source code the corpus was built on

4. **Plan the code top-down** — outline functions/classes, pointing each at the corpus retrieval that justifies it. Show this plan to the user before coding.

5. **Write the code** in the target language from STUDY-ANCHOR. For every non-obvious decision:
   - Inline comment with citation: `// pattern from topics/<topic>/concepts/<id>.md`
   - Or: `// per worked example topics/<topic>/examples/<name>/`

6. **Flag fallbacks explicitly.** For any line/block where the corpus is silent and you used general knowledge:
   ```python
   # [OUTSIDE MATERIAL] The corpus doesn't cover async retry policy;
   # using exponential backoff per general convention. Consider adding
   # a concept file if this comes up again.
   ```

7. **Output structure:**
   ```
   <code blocks with inline citations>

   ## Coverage report
   - Grounded in corpus: <list of concepts cited>
   - Outside material: <list of fallback decisions, each with WHY>

   ## Suggested follow-up
   - If the [OUTSIDE MATERIAL] decisions matter for this subject, run:
     /ingest-material <relevant source>
     /extract-concepts <topic>
   ```

## Constraints

- **Every fallback is flagged.** No silent leaning on training data.
- **Citations are inline as comments**, not just in a footer.
- **Plan before code.** Top-down outline keeps the user in the loop.
- **Target language is fixed** by STUDY-ANCHOR. If you need another, justify and ask.
- **Don't write tests unless asked.** This skill produces example/study code; production-grade hygiene belongs in the BUILD workflow, not study.

## Anti-patterns

- Generating code that "feels right" without retrieval. If you're not citing, you're hallucinating.
- Hiding fallbacks in plausible-looking code. The whole point is the user can audit what's grounded vs not.
- Writing 500 LOC for a study question. Smallest thing that exercises the concept.
- Adding error handling, logging, or production scaffolding. This is study code.

## Composes with

- `/scan-knowledge` — the retrieval substrate
- `/worked-example` — the canonical pattern this skill borrows from
- `/compare-implementations` — same task, different languages, side-by-side
