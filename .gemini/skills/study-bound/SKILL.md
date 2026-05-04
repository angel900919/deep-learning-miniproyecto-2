---
name: study-bound
description: Bound a topic within the subject — produce topics/<topic>/CONTEXT.md (≤200 lines) covering scope, prerequisites, learning goals, key concepts, source materials, and out-of-scope. The "topic quantum". Use when starting a new topic area, when the user says "/study-bound", "bound this topic", or before ingesting material on a new subject area.
---

# study-bound

Produce `topics/<topic>/CONTEXT.md` and the topic folder skeleton. A topic is the unit of study — small enough to master in days, large enough to deserve its own page.

## Inputs required

- `STUDY-ANCHOR.md`
- `GLOSSARY.md` (if it exists)

## Process

1. **Choose the topic name** — short, kebab-case (e.g. `consensus-algorithms`, `vector-spaces`, `ratio-analysis`). Avoid "intro-to-X" or "advanced-X" — those are book chapters, not topics.

2. **Interview** — one question at a time, recommended answer each:
   - One-line **purpose** — what does mastering this enable?
   - **Prerequisites** — list other topics or external knowledge required
   - **Learning goals** — 3-7 bullets at the Bloom level set in STUDY-ANCHOR
   - **Key concepts** to cover (placeholder — will be filled by `/extract-concepts`)
   - **Out of scope** — what's adjacent but NOT in this topic
   - **Source materials** — which `material/` files cover this topic (paths)

3. **Create the topic skeleton:**
   ```
   topics/<topic>/
   ├─ CONTEXT.md
   ├─ concepts/                # one .md per concept (filled by /extract-concepts)
   ├─ mental-models.md
   ├─ flashcards.md            # filled by /make-flashcards
   ├─ examples/                # CODE-LEARN: code; CONCEPT-LEARN: worked problems
   └─ progress.md
   ```

4. **Write `CONTEXT.md`** using the template. **Hard cap: 200 lines.**

5. **Cross-link** in root `GLOSSARY.md` if new terms emerged.

## Template

```markdown
# Topic: <name>

## Purpose
<one sentence>

## Prerequisites
- <topic-id or external knowledge>
- ...

## Learning goals (Bloom level: <from STUDY-ANCHOR>)
- [ ] Goal 1
- [ ] Goal 2
...

## Key concepts
(filled by /extract-concepts — placeholder)
- <concept-id> — <one line>

## Out of scope
- <thing>

## Source materials
- material/lectures/<file> — <what's covered>
- material/readings/<file> — <what's covered>
- material/code-samples/<file> — <what's covered>

## Notes for agents
- Source-of-truth order (overrides STUDY-ANCHOR if specified): <list>
- Common confusions to flag: <list>
```

## Constraints

- 200-line hard cap.
- Learning goals are checkable; "understand X" is too vague. Use "explain X to a peer", "implement X in <stack>", "derive X from <axiom>".
- Out-of-scope list is doing real work — it stops the agent from sprawling.

## Anti-patterns

- One topic = one entire textbook chapter. Too big. Split.
- Skipping prerequisites. The agent will hallucinate the foundation.
- Listing source materials that don't exist yet. Ingest first.
