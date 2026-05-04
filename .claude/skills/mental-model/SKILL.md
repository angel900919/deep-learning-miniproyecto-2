---
name: mental-model
description: Build a "C-header" mental model for a concept — the smallest set of mental primitives + interactions that lets you reason about everything else in the topic. Produces topics/<topic>/mental-models.md entries. Use for hard concepts that resist memorisation, when the user says "/mental-model", "build a mental model for X", or before applying a concept in a worked example.
---

# mental-model

Produce or extend `topics/<topic>/mental-models.md` — concise, decision-oriented mental models for the most leverage-bearing concepts. A mental model is what lets you derive the answer instead of recalling it.

## Inputs required

- `topics/<topic>/CONTEXT.md`
- The relevant `concepts/<concept-id>.md`
- Source material citations from that concept
- `STUDY-ANCHOR.md` (mode + Bloom level)

## Process

1. **Identify the leverage points** — what core abstractions, when held in mind, let you answer most questions about this concept without lookup?

2. **Force atomicity** — a mental model is 3–7 mental primitives, not a chapter summary. If yours has 20 things, you have 3 mental models, not 1.

3. **Frame as decision-aid** — what does this model let you DO that you couldn't before?

4. **Sketch the relationships** as ASCII (not Mermaid; this is for your head, not a diagram tool).

5. **Add a "when this model breaks"** section — every model has limits. Naming them prevents misapplication.

6. **Add a "test yourself"** prompt — one question that, if you can answer, proves you hold the model.

7. **Write to `topics/<topic>/mental-models.md`** as one section per model. Hard cap: 80 lines per model.

## Template — section in `mental-models.md`

```markdown
## Model: <name>

### Primitives
1. <primitive 1> — one line
2. <primitive 2> — one line
3. <primitive 3> — one line
(3–7 max)

### Relationships (ASCII)

```
<simple ASCII showing how primitives interact>
```

### What this model lets you DO
- <decision/derivation 1>
- <decision/derivation 2>

### When this model breaks
- <edge case 1>
- <edge case 2>

### Test yourself
> <one question that, if answered, proves the model is held>

### Source
- material/<path>:<loc>
```

## Constraints

- 7 primitives max. More = you have multiple models bundled.
- Decision-aid framing is mandatory. "What you can do with it" beats "what it is".
- Test-yourself question must be answerable from the primitives alone.
- No external citations in the model body — link them at the end.

## Anti-patterns

- Mental models that read like definitions. Definition lives in the concept file; model lives here.
- Skipping "when this model breaks". Half the value of holding a model is knowing when not to apply it.
- Writing one giant model for the whole topic. Mental models are atomic.
