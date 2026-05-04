---
name: grill-on-topic
description: Quiz the user on a topic — one question at a time, escalating Bloom level until a confident gap is exposed. Different from /spaced-review (which is recall): grill probes Apply/Analyse/Evaluate. Logs gaps to .study/current-questions.md for follow-up. Use when the user says "/grill-on-topic", "grill me on X", "test my understanding of Y", or before an exam.
---

# grill-on-topic

Run a Socratic quiz on a topic, one question at a time, climbing the Bloom ladder until you find a real gap. Different from spaced review: this targets *application and reasoning*, not recall.

## Inputs required

- Topic ID
- `topics/<topic>/CONTEXT.md` (Bloom target)
- `topics/<topic>/concepts/*.md`
- `topics/<topic>/mental-models.md`
- `.study/progress-tracker.md` (state per concept)

## Process

1. **Pick the focus** — concepts in the topic at READING or UNDERSTOOD state. Skip APPLIED/RETAINED unless user requests them.

2. **Start at Understand-level** — "In your own words, what does X do?" Wait for the answer.

3. **Grade silently** — compare to the canonical wording in `concepts/<id>.md`. Note any drift.

4. **Climb the ladder** — if the answer was right, ask an Apply question: "Given input X, what's the output?" If that's right, ask an Analyse: "Why does this approach beat alternative Y?" If that's right, an Evaluate: "When would you choose Y over X anyway?"

5. **Stop on first confident gap** — when the user gets something wrong or hedges, freeze. Don't pile on. Show the canonical answer with citation, and:
   - Suggest `/explain-back <concept>` to repair
   - Append the gap to `.study/current-questions.md`
   - Demote the concept's state in `progress-tracker.md` if needed

6. **One topic per session.** A 15-minute grill on one topic beats 60 minutes across five.

## Question templates by Bloom level

- **Understand** — "Define X without lookup. What's the simplest example?"
- **Apply** — "Given <scenario>, walk through what happens step by step."
- **Analyse** — "What changes if we relax assumption X? Which property breaks?"
- **Evaluate** — "Two approaches A and B. Pick one and defend it under <constraint>."
- **Create** — "Design an X for <novel constraint>. Justify each design choice."

## Constraints

- One question at a time. Never queue.
- Stop on first gap. Repair beats compound failure.
- Silent grading first; reveal canonical only after the user's answer is locked.
- Bloom level escalates only on confident correctness.
- Log every gap to `.study/current-questions.md` — these are next-session priorities.

## Anti-patterns

- Multi-question mega-prompts ("answer these five"). Diffuses focus.
- Praising vague answers. "Yes, kind of" is not correct; it's a gap.
- Ignoring the citation when revealing the canonical. The user needs to know where to re-read.
- Grilling on RETAINED concepts. Those go in `/spaced-review`.
