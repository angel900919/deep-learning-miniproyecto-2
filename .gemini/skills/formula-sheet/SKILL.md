---
name: formula-sheet
description: CONCEPT-LEARN only. Produce topics/<topic>/formula-sheet.md — a single-page reference of all formulas, identities, and constants for a topic, each with name, equation, units of every variable, conditions of validity, and source citation. Use when starting heavy worked-problem practice, when the user says "/formula-sheet", "build a formula sheet", or before any exam.
---

# formula-sheet (CONCEPT-LEARN)

Produce a one-page (densely typeset) reference sheet for a topic. Used during worked problems and exams. Every entry has units, conditions of validity, and a source.

## Inputs required

- `STUDY-ANCHOR.md` (mode = CONCEPT-LEARN; notation convention)
- All `topics/<topic>/concepts/*.md`
- All `topics/<topic>/examples/*.md`
- Source materials cited in concepts

## Process

1. **Inventory formulas** — walk concepts and worked problems. List every distinct formula, identity, or constant. Don't filter.

2. **Group by sub-topic** — kinematics, dynamics, energy; or time-value-of-money, ratios, statements; or subnetting, routing protocols, etc.

3. **For each formula:**
   - Canonical name (cite the source's name; if unnamed, use a descriptive ID)
   - Equation (LaTeX)
   - Variables — name + units + typical range
   - Conditions of validity — when it applies, when it doesn't
   - One-line "use this when" trigger
   - Source citation

4. **Resolve notation conflicts** — pick one symbol per quantity per topic. If sources disagree, document the choice.

5. **Add a "constants" section** at the end with their precision (e.g. `g = 9.81 m/s²`, not `g ≈ 10`).

6. **Write to `topics/<topic>/formula-sheet.md`**. Cap: 200 lines, dense.

7. **Cross-link** every entry from any worked problem that uses it.

## Template

```markdown
# Formula sheet — <topic>

(notation: SI units unless stated; <symbol convention>)

## <Sub-topic 1>

### F-001  Newton's second law
$$F = m a$$
- $F$ — force (N)
- $m$ — mass (kg)
- $a$ — acceleration (m/s²)
**Valid when:** classical regime, constant mass.
**Use when:** computing force from observed motion, or vice versa.
**Source:** material/textbook/ch-2.md:p.34

### F-002  Kinematic — constant acceleration
$$v = v_0 + a t$$
$$x = x_0 + v_0 t + \tfrac{1}{2} a t^2$$
- $v_0, v$ — initial / final velocity (m/s)
- $x_0, x$ — initial / final position (m)
- $a$ — acceleration (m/s²); constant
- $t$ — time (s)
**Valid when:** $a$ constant.
**Use when:** projectile motion, free fall.
**Source:** material/textbook/ch-2.md:p.41

## <Sub-topic 2>
...

## Constants
- $g = 9.81 \text{ m/s}^2$ — standard gravity
- $\pi \approx 3.14159$
- ...

## Notation choices (where sources disagreed)
- We use $\rho$ for density (textbook); some lecture notes use $d$. Stick with $\rho$.
```

## Constraints

- Units on every variable, every entry.
- "Valid when" clause is mandatory. Half of all wrong answers come from applying a formula outside its domain.
- One canonical symbol per quantity per topic. Document conflicts.
- Group by sub-topic, not by alphabet.
- Cap 200 lines, dense. A 5-page formula sheet doesn't fit on the desk during an exam.

## Anti-patterns

- Formulas without variable definitions. The sheet is for re-derivation, not for the formula in isolation.
- Mixing units within one entry (e.g. some quantities cgs, others SI). Pick one, document.
- Skipping "use when". A formula without a trigger is unhelpful under time pressure.
- Decorative formulas the topic doesn't actually use. Cull.
