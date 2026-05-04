---
name: derive-from-first-principles
description: CONCEPT-LEARN only. Walk a derivation from named axioms or first-principles to a target formula or theorem, narrating every step's reason. Produces topics/<topic>/derivations/<name>.md. The strongest test of understanding for theory-heavy subjects (math, physics, EE, accounting standards). Use when the user says "/derive-from-first-principles", "derive X", or to promote a concept from APPLIED to ANALYSE/EVALUATE.
---

# derive-from-first-principles (CONCEPT-LEARN)

Produce a step-by-step derivation from named starting points to a target. Every step has a reason; every leap is justified. The point is reproducibility — the user must be able to re-derive in an exam without lookup.

## Inputs required

- Target (formula, theorem, identity)
- Starting axioms / postulates / first principles (named, cited)
- `concepts/<concept-id>.md` for the target
- `topics/<topic>/formula-sheet.md` (for intermediate identities)

## Process

1. **State the target.** What are we deriving? In what notation?

2. **State the starting points.** Axioms or accepted prior results. Each cited.

3. **Decompose the path** — outline 4–10 milestone equations from start to target. Show this skeleton before filling in.

4. **Fill in each step** with:
   - The equation
   - The operation applied (substitution, integration, identity invocation, algebraic rearrangement)
   - The reason (which rule, which axiom, which prior result)

5. **Name every identity and theorem invoked.** "Apply integration by parts" not "integrate".

6. **Surface every assumption** as it's introduced. Continuity, differentiability, finiteness — all named.

7. **Conclude** with the target equation and a sanity check (limiting cases, dimensional analysis, special-case agreement with known results).

8. **Write to `topics/<topic>/derivations/<name>.md`.** Cap: 250 lines (derivations earn the extra room).

## Template

```markdown
# Derivation: <name>

**Target:** $<equation>$
**Topic:** <topic>
**Concept:** topics/<topic>/concepts/<concept-id>.md

## Starting points
1. <axiom or prior result> — cited from <source>
2. <axiom or prior result>
3. ...

## Path skeleton
1. From axioms → milestone A
2. Milestone A → milestone B (via <operation>)
3. Milestone B → target

## Derivation

### Step 1 — <action>
$$<equation 1>$$
*From:* axiom 1.
*Why:* <one line>

### Step 2 — <action>
$$<equation 2>$$
*Operation:* substitute axiom 2.
*Why:* <one line>

### Step 3 — <action>
$$<equation 3>$$
*Operation:* integration by parts (cite GLOSSARY).
*Why:* <one line>

...

### Step N — Result
$$<target equation>$$ ✓

## Assumptions used
- <list, each cited where introduced>

## Sanity checks
- Dimensional: ✓
- Limiting case <X → 0>: reduces to <known result>
- Limiting case <X → ∞>: reduces to <known result>

## Source
- Reference derivation: <material/path>
```

## Constraints

- Every step has a reason. "Algebra" is not a reason.
- Every invoked theorem is named, not just used.
- Assumptions named at point of use, not in a footer.
- Sanity check by limiting cases is mandatory.
- If you can't justify a step, mark `[GAP]` — don't paper over.

## Anti-patterns

- Skipping "obvious" steps. What's obvious to one author isn't to the user re-deriving in 6 weeks.
- Substituting numbers mid-derivation. Stay symbolic until the very end.
- Skipping the sanity check. It catches sign and dimension errors that destroy answers.
- Treating named theorems as anonymous. "By Stokes' theorem" beats "rearranging".
