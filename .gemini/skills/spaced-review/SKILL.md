---
name: spaced-review
description: Generate today's spaced-repetition queue from flashcards.md across all topics, weighted by progress-tracker state and last-reviewed date. Writes to reviews/<date>.md and lets the user mark each card pass/fail. Pass updates progress; fail flags for /explain-back. Use daily, when the user says "/spaced-review", "what should I review today", "review queue".
---

# spaced-review

Produce `reviews/<YYYY-MM-DD>.md` — today's spaced-repetition session as a checklist. Pulls from all topics, weighted by mastery state and last-review interval (SM-2-style).

## Inputs required

- All `topics/*/flashcards.md`
- `reviews/` history (recent files)
- `.study/progress-tracker.md`

## Process

1. **Compute eligibility per card:**
   - Never reviewed → eligible (high priority for UNDERSTOOD-or-above concepts)
   - Last review FAILED → eligible (high priority)
   - Last review PASSED → eligible if `today >= last_review + interval`
   - Interval grows on success: 1 → 3 → 7 → 14 → 30 → 90 (days)
   - Interval resets to 1 on fail

2. **Weight by mastery target** — concepts whose target is APPLIED or higher get more frequent review.

3. **Cap the queue** — default 30 cards/day; configurable in `STUDY-ANCHOR.md`.

4. **Shuffle within priority bands** so the same topic doesn't dominate.

5. **Write `reviews/<date>.md`** with one card per row, each as a markdown checkbox.

6. **After session** — read the user's marks (pass/fail/skip), update concept state in `.study/progress-tracker.md`, append a `## Result` block to today's review file.

7. **Surface "fail spirals"** — if the same card has failed ≥3 reviews in a row, suggest `/explain-back` on the underlying concept.

## Template — `reviews/2026-05-04.md`

```markdown
# Review queue — 2026-05-04

Cards: 24. Time-box: ~15 min.

## Queue
- [ ] q-001 — What does CAP stand for? <sub>(consensus-algorithms / cap-theorem; last 2026-04-27 PASS)</sub>
- [ ] q-014 — Linear independence: definition? <sub>(vector-spaces; last 2026-04-30 FAIL)</sub>
- [ ] q-027 — Difference between Paxos and Raft on leader election? <sub>(consensus-algorithms / raft-leader-election; never reviewed)</sub>
...

## Result (filled by user)
- q-001 PASS
- q-014 PASS
- q-027 FAIL → suggest /explain-back raft-leader-election
```

## Constraints

- Default cap 30 cards/day. Larger queues kill the habit.
- Same card can't appear twice in one queue.
- Fail spirals (≥3 fails in a row) trigger `/explain-back` suggestion automatically.
- Interval algorithm is SM-2-lite; full SM-2 lives in your dedicated tool (Anki/Mochi) if used.

## Anti-patterns

- Skipping days. The interval algorithm assumes continuous days.
- Marking PASS when you peeked. Honest fail teaches; dishonest pass deceives.
- Ignoring fail spirals. They mean the concept needs re-teaching, not more reviews.
