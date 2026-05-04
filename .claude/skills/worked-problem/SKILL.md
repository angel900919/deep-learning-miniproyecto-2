---
name: worked-problem
description: CONCEPT-LEARN only. Produce topics/<topic>/examples/<problem-id>.md — a fully worked solution to one problem with every step shown, every formula cited, every assumption named. The general-subject equivalent of /worked-example. Use after /mental-model, when the user says "/worked-problem", "solve this problem step by step", or to promote a concept from UNDERSTOOD to APPLIED.
---

# worked-problem (CONCEPT-LEARN)

Produce a fully-worked problem with EVERY step visible. The point isn't the answer — it's the chain of reasoning the user can re-trace, replicate, and adapt.

## Inputs required

- Concept ID + `concepts/<concept-id>.md`
- `STUDY-ANCHOR.md` (mode = CONCEPT-LEARN; notation conventions)
- The problem statement (from `material/`, past papers, or user-supplied)

## Process

1. **Verify mode** — STUDY-ANCHOR must be CONCEPT-LEARN. If CODE-LEARN, redirect to `/worked-example`.

2. **State the problem verbatim.** No paraphrasing — the user reads it as it would appear on an exam.

3. **List given quantities and unknowns.** Use the project's notation convention.

4. **Name every assumption.** Even "obvious" ones — `assume incompressible flow`, `assume no friction`, `assume per-period accrual`. Assumptions hidden = points lost.

5. **Identify the relevant principle/formula** — cite from the formula sheet (`/formula-sheet`) or the concept file. Never invoke a formula without citation.

6. **Walk every step.** Show algebra. Skip nothing the learner can't fill in mentally. Each step gets a one-line *reason*.

7. **Compute with units.** Carry units through every step. Mismatches are bugs.

8. **State the final answer with units and reasonable precision.**

9. **Sanity-check.** Order of magnitude, sign, units — does the answer make physical/financial sense?

10. **Write to `topics/<topic>/examples/<problem-id>.md`** using the template. Cap: 200 lines.

## Template

```markdown
# Worked problem: <id> — <short title>

**Topic:** <topic>
**Concepts used:** <concept-id>, <concept-id>

## Problem (verbatim)
> <problem statement>

## Given
- <var> = <value> <units>
- ...

## Find
- <unknown> in <units>

## Assumptions
- <assumption 1>
- <assumption 2>

## Strategy
<one paragraph: which principle applies and why; cite the concept or formula sheet>

## Solution

### Step 1 — <what>
$<equation>$
*Reason:* <one line>

### Step 2 — <what>
$<equation with substitution>$
*Reason:* <one line>

### Step 3 — <what>
$<computation>$
*Reason:* <one line>

## Answer
**<unknown> = <value> <units>**

## Sanity check
- Units: ✓ <units make sense>
- Order of magnitude: ✓ <expected range>
- Sign: ✓ <expected sign>

## Variations to try
1. Change <input> from A to B; predict direction of change.
2. Relax assumption <X>; what new term appears?
3. Solve symbolically; identify which variables dominate.

## Source
- Problem: <material/path>
- Concept: topics/<topic>/concepts/<concept-id>.md
- Formula sheet entry: GLOSSARY.md or topics/<topic>/formula-sheet.md
```

## Constraints

- Every step has a reason. "Algebra" is not a reason.
- Units travel with every quantity.
- Assumptions named explicitly, even obvious ones.
- Sanity check is mandatory. Skipped check = often missed sign error.
- Variations section turns one problem into three; this is how UNDERSTOOD becomes APPLIED.

## Anti-patterns

- Skipping algebraic steps to "save space". The user can't follow what they can't see.
- Plugging numbers in at step 1. Solve symbolically as long as you can; substitute at the end.
- Hand-waving units. Units catch most errors before they cost points.
- Rounding intermediate results. Round only at the final answer.
