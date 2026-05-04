---
name: study-progress
description: Maintain .study/progress-tracker.md — the per-concept mastery state (UNREAD / READING / UNDERSTOOD / APPLIED / RETAINED) and per-topic Bloom progress. The single file that lets a fresh session resume exactly where you left off. Use after every study session, when the user says "/study-progress", "update progress", "where did I leave off".
---

# study-progress

Maintain `.study/progress-tracker.md` — the always-current view of where you are. Every concept has one mastery state; every topic has aggregate Bloom progress. Updated after every meaningful study session.

## Inputs required

- `STUDY-ANCHOR.md` (Bloom targets per topic)
- All `topics/*/concepts/*.md`
- `reviews/` history
- The session that just happened

## Process

1. **Read the current tracker** — never overwrite blindly.

2. **For the session just completed, update each touched concept's state:**
   - **UNREAD** — exists in `concepts/` but never opened
   - **READING** — actively studying; partial understanding
   - **UNDERSTOOD** — can re-state in own words (Bloom: Understand)
   - **APPLIED** — used in a worked example/problem (Bloom: Apply)
   - **RETAINED** — ≥3 successful spaced-rep reviews ≥7 days apart (Bloom: any, with retention)

3. **Roll up per-topic Bloom progress** — % of concepts at or above the target Bloom level for the topic.

4. **Identify "stale at READING"** — concepts that have been READING for >2 weeks. Surface them as candidates for `/explain-back` or `/grill-on-topic` to unblock.

5. **Note next-session entry point** — one line: "Next: <action>" so a fresh session starts immediately without re-orientation.

## Template — `.study/progress-tracker.md`

```markdown
# Progress tracker

## Last updated
2026-05-04 (after session on consensus-algorithms)

## Next session entry point
Run /grill-on-topic on consensus-algorithms — focus on Paxos vs Raft trade-offs.

## Topic progress
| Topic | Bloom target | Concepts | UNDERSTOOD | APPLIED | RETAINED | At/above target |
|---|---|---|---|---|---|---|
| consensus-algorithms | Apply | 12 | 10 | 7 | 4 | 58% |
| vector-spaces | Understand | 8 | 8 | 3 | 0 | 100% |

## Concept state
### consensus-algorithms
- [APPLIED] paxos-basic — implemented in py 2026-05-02
- [READING] raft-leader-election — stuck on safety proof step 3
- [UNDERSTOOD] cap-theorem
- ...

### vector-spaces
- [UNDERSTOOD] linear-independence
- [READING] basis-and-dimension
- ...

## Stale concepts (READING > 2 weeks)
- raft-leader-election — last touched 2026-04-18; suggest /explain-back

## Recently RETAINED
- 2026-05-04 — cap-theorem (3rd review)
```

## Constraints

- One state per concept. No "kind of understood".
- RETAINED only after spaced-rep evidence; can't self-promote.
- Stale-at-READING is surfaced automatically.
- Next-session entry point is mandatory — without it, the next session burns 10 minutes re-orienting.

## Anti-patterns

- Marking everything UNDERSTOOD after reading once. Bloom-Understand requires re-stating in own words; check via `/explain-back`.
- Ignoring stale concepts. Stuck-and-forgotten is the failure mode.
- Letting the tracker rot. Once it stops being updated, the resume guarantee breaks.
