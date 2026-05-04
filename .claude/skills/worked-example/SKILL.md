---
name: worked-example
description: CODE-LEARN only. Produce topics/<topic>/examples/<example>/ — a runnable, well-commented code example that exercises a concept end-to-end, in the language declared in STUDY-ANCHOR. Includes README, code file(s), expected output, and exercises. Use after /mental-model, when the user says "/worked-example", "show me X in code", or to promote a concept from UNDERSTOOD to APPLIED.
---

# worked-example (CODE-LEARN)

Produce a runnable code example that exercises one concept end-to-end. The artifact has four parts: README explaining the example, code file(s), expected output, and a small set of exercises that vary the example.

## Inputs required

- Concept ID + `concepts/<concept-id>.md`
- `STUDY-ANCHOR.md` (mode must be CODE-LEARN; target language)
- Cited material (often `material/code-samples/` has a starting point)

## Process

1. **Verify mode** — STUDY-ANCHOR must be CODE-LEARN. If CONCEPT-LEARN, redirect to `/worked-problem`.

2. **Pick scope** — smallest example that exercises the concept's core mechanism. NOT a tutorial of the language.

3. **Identify the canonical reference implementation** — usually in `material/code-samples/`. If none, check the textbook source. If the user has an opinion, follow it.

4. **Create the folder:**
   ```
   topics/<topic>/examples/<example-name>/
   ├─ README.md           # what it shows, how to run, expected output
   ├─ <code file(s)>      # the example in target language
   ├─ expected.txt        # expected stdout/stderr (for reproducibility)
   └─ exercises.md        # 3–5 variations to attempt
   ```

5. **Write the example:**
   - Self-contained, runnable from this folder
   - Comments explain *why*, not *what* (the code says what)
   - Each non-obvious line cites the concept's source
   - One concept per example

6. **Capture expected output** — run it (in your head or in a sandbox) and write the expected output verbatim. This is what the user diffs against when they tweak.

7. **Write 3–5 exercises** of escalating difficulty. Each exercise modifies the example to test understanding.

8. **Update `concepts/<concept-id>.md`** — link this example.

9. **Update `progress-tracker.md`** — concept moves toward APPLIED once the user successfully runs and modifies it.

## Template — `examples/<example-name>/README.md`

```markdown
# Worked example: <concept> — <example-name>

## What this shows
<one paragraph: which concept, which case, what the user will see>

## How to run
```bash
<command>
```

## Expected output
See `expected.txt`.

## What's interesting
- Line N — uses primitive X from the mental model
- Line M — handles edge case Y; without this you get Z
- Line P — citation: material/<file>:L<line>

## Exercises
1. (easy) Change <input> from A to B. Predict the output before running.
2. (medium) Add handling for <edge case>.
3. (hard) Implement <variation>; compare correctness against expected.txt.
4. (open) Now think: why does this approach win over <alternative>?

## Source
- Concept: topics/<topic>/concepts/<concept>.md
- Reference impl (if any): material/code-samples/<path>
```

## Constraints

- One concept per example. A 200-line example covering 5 concepts is 5 examples.
- Expected output is mandatory. Without it, exercises have no ground truth.
- Comments cite sources for non-obvious lines.
- Target language matches STUDY-ANCHOR. If you NEED another language to make the point, justify in README.
- Run the code (or have the user run it) before declaring the example shipped.

## Anti-patterns

- Tutorials. This is not "teach Python"; it's "demonstrate this concept in our chosen language."
- 500-line examples. Split.
- Copying material/code-samples/ verbatim with no commentary. The point is the *narrated* version.
- Skipping exercises. They're how UNDERSTOOD becomes APPLIED.

## Composes with

- `/code-from-material` — uses worked examples as in-corpus retrievals
- `/compare-implementations` — takes one concept's example and renders it in another language
