---
name: compare-implementations
description: CODE-LEARN only. Render one concept's worked example in two-or-more languages side by side, highlighting idiomatic differences and where each language's primitives map to the concept. Produces topics/<topic>/examples/<example>/comparison.md. Use when the user says "/compare-implementations", "show this in Rust and Go", "how would this look in <other language>".
---

# compare-implementations (CODE-LEARN)

Render the same concept's worked example in 2–4 languages side by side. The point is to surface what's *concept* vs what's *language ceremony*.

## Inputs required

- A worked example that already exists: `topics/<topic>/examples/<name>/`
- Target languages (2–4)
- `STUDY-ANCHOR.md`

## Process

1. **Pick the canonical version** — the one already in the worked example, in the STUDY-ANCHOR target language.

2. **For each additional language:**
   - Translate, keeping the **same structure** so diffs surface idiom not algorithm
   - Use that language's idiomatic constructs (async style, error handling, generics)
   - Note where the concept's primitives map differently (e.g. immutability in Rust vs Python)

3. **Produce side-by-side `comparison.md`** with three columns: Language A, Language B, [Language C, …].

4. **Highlight per-row what the user should notice** — one-line annotation under each notable row.

5. **Add a "What's the same / what's different" footer** — the takeaway: which parts are concept (invariant across languages) and which are ceremony (language-specific).

## Template — `examples/<example>/comparison.md`

```markdown
# Comparison: <concept> — <example>

| | Python | TypeScript | Rust |
|---|---|---|---|
| Imports | `from collections import deque` | `// none` | `use std::collections::VecDeque;` |
| State | `state = {"a": 0, "b": 0}` | `let state = { a: 0, b: 0 };` | `let mut state = State { a: 0, b: 0 };` |
| Loop | `while pending:` | `while (pending.length) {` | `while !pending.is_empty() {` |
| Mutation | direct dict mutation | direct object mutation | `&mut self` everywhere |
| ... | | | |

### Notable row commentary
- Mutation row: in Rust, the borrow checker forces explicit ownership decisions the other languages defer to runtime. The concept (sequential state update) is the same; the ceremony differs.

## Same across all
- The algorithm: <one line>
- The invariants: <one line>

## Different across languages
- Error handling style — <one line>
- Async model — <one line>
- Memory model — <one line>

## Source
- Original example: topics/<topic>/examples/<example>/
```

## Constraints

- 2–4 languages max. More becomes wallpaper.
- Same structure across columns — diffs should be local, not architectural.
- Annotate only the *interesting* rows. The boring ones speak for themselves.
- Don't extend the original example. If a comparison reveals a new variation, propose a new worked example.

## Anti-patterns

- Picking a language no one in the corpus uses. Compare with stacks the user is actually learning or migrating between.
- Translation that hides the point ("this is more elegant in Haskell"). Stay descriptive, not evaluative — the goal is to see the concept under different ceremony.
- Five-language comparisons. Pick the two or three that teach the most.
