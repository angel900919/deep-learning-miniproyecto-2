---
name: build-glossary
description: Maintain GLOSSARY.md at the study root — canonical terms, single-line definitions, and pointer to where each term is fully explained. The vocabulary spine of the subject. Use when the user says "glossary", "/build-glossary", "what does X mean", or after /extract-concepts surfaces new terms.
---

# build-glossary

Maintain `GLOSSARY.md` at the study root. Acts as the subject's domain glossary — canonical wording, one entry per term, pointers to fuller treatment elsewhere.

## Inputs required

- `STUDY-ANCHOR.md`
- All `topics/*/concepts/*.md`
- All `material/` files (sampled)

## Process

1. **Inventory terms** — scan all concept files and material for capitalised terms, jargon, acronyms, named theorems/algorithms/laws.

2. **For each term:**
   - Pick the canonical form (full name + acronym if applicable)
   - Write a one-line definition (≤25 words)
   - Point to the fullest treatment: `→ topics/<topic>/concepts/<concept>.md`

3. **Resolve conflicts** — if two materials define the same term differently, pick one per the source-of-truth policy in `STUDY-ANCHOR.md` and add a `<small>(see also: alternative usage in <source>)</small>` note.

4. **Write `GLOSSARY.md`** alphabetically. Cap at ~300 lines; if longer, split by topic into `topics/<topic>/glossary.md` and keep root as the master index.

## Template

```markdown
# Glossary — <subject>

(canonical terms; one-line definitions; pointer to full treatment)

## A
- **Aggregate** — A consistency boundary owning related entities. → topics/ddd/concepts/aggregate.md
- **Algorithm** — A finite, deterministic procedure for solving a problem. → topics/algorithms/concepts/algorithm.md

## B
- **Big-O notation** — Upper bound on asymptotic complexity. → topics/complexity/concepts/big-o.md

...
```

## Constraints

- One-line definitions only. Full treatment lives in the linked concept file.
- Cite the canonical source (often a textbook, RFC, or seminal paper).
- Conflicting definitions get the policy-winner in the body and the alternative in a small note.
- Acronyms get their own row pointing to the full term: `**CAP** → see Consistency-Availability-Partition`.

## Anti-patterns

- Definitions that drift over time. The glossary is a contract; if a definition changes, update the concept file too.
- Using the glossary as a "thoughts" page. Those go in `notes/`.
- Letting the glossary grow past 300 lines without splitting.
