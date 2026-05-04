---
name: study-postmortem
description: After an exam, project, or interview, produce exams/<date>-<name>/postmortem.md — what was missed, why, and concrete artifact updates (new concepts, new flashcards, demoted progress states, new mental models). Closes the loop from real-world test back into the study folder. Use after any graded assessment, when the user says "/study-postmortem", "I just took an exam", "review my mistakes".
---

# study-postmortem

Produce `exams/<YYYY-MM-DD>-<name>/postmortem.md`. Blameless-on-yourself, action-oriented. The post-mortem's value is not in the doc — it's in the artifacts that change because of it.

## Inputs required

- `exams/<date>-<name>/paper.md` (the exam paper or task)
- `exams/<date>-<name>/my-attempt.md` (your answers)
- The grading or known correct answers
- All `topics/*/concepts/`, `flashcards.md`, `progress-tracker.md`

## Process

1. **Lock the questions and answers first.** Save `paper.md` and `my-attempt.md` verbatim before opinions form.

2. **Per question, classify the outcome:**
   - **Correct + confident** — fine
   - **Correct + uncertain** — note (mastery is shallow)
   - **Wrong + I knew the concept** — application failure (drill via `/worked-example` or `/worked-problem`)
   - **Wrong + concept-gap** — knowledge failure (re-ingest, new concept file, new flashcards)
   - **Wrong + question-misread** — exam-skill issue (note pattern)
   - **Skipped/blank** — time/strategy issue

3. **Diagnose root cause** per wrong answer. Five-whys lite. Map back to a specific concept ID where possible.

4. **Generate concrete artifact updates** — every lesson maps to ONE of:
   - **New concept** — `/extract-concepts` on a missing topic
   - **New flashcard rows** — `/make-flashcards` for under-covered facts
   - **Demoted state** — concept moves from APPLIED back to UNDERSTOOD or READING
   - **New mental model** — `/mental-model` for an idea the exam exposed as fragile
   - **Stale-knowledge flag** — concept goes back into `/spaced-review` immediately, not at next interval
   - **Exam-skill note** — appended to `notes/exam-strategy.md` (not a concept; a meta-skill)

5. **Write `postmortem.md`** using the template.

6. **Schedule the follow-up** — append the new flashcards to tomorrow's review queue; queue any new `/explain-back` sessions.

## Template

```markdown
# Post-mortem — <date> <exam name>

## Summary
Score: <X/Y>. Time used: <m/n minutes>.

## Question outcomes
| # | Topic | Outcome | Root cause | Action |
|---|---|---|---|---|
| 1 | consensus-algorithms | wrong + concept-gap | didn't know FLP impossibility | new concept file + 2 flashcards |
| 2 | consensus-algorithms | wrong + I knew the concept | misapplied Paxos roles | /worked-example paxos-basic |
| 3 | vector-spaces | correct + uncertain | guessed; basis dimension still fuzzy | demote basis-and-dimension to READING; /explain-back |
| 4 | — | wrong + question-misread | rushed first scan | strategy note |

## Five whys (Q1)
1. Got Q1 wrong → didn't know FLP exists.
2. → never appeared in any source material I'd ingested.
3. → original lecture notes skipped impossibility theorems.
4. → curriculum gap (textbook ch.4 covers it; not in lectures).
5. → root: I treated lecture notes as exhaustive.

## Action: lesson learned
- Always cross-check lecture topics against the textbook TOC for missing chapters.

## Follow-ups
| # | Type | Action | Done |
|---|---|---|---|
| F1 | new concept | /extract-concepts on textbook ch.4 (FLP) | [ ] |
| F2 | flashcards | /make-flashcards for FLP-related facts | [ ] |
| F3 | worked example | /worked-example paxos-basic with the misapplied case | [ ] |
| F4 | demote | basis-and-dimension → READING in tracker | [ ] |
| F5 | strategy | "first 5 min: scan the whole paper, mark hard ones, attack easy first" → notes/exam-strategy.md | [ ] |

## Strategy notes
<exam-skill issues — pacing, panic, misreading — go here, not in concept files>
```

## Constraints

- Every wrong answer maps to exactly one root cause. "I forgot" is a symptom, not a cause.
- Every lesson generates an artifact change. A post-mortem with no artifact updates is decoration.
- Demote progress immediately — don't wait for the next session to find it stale.
- Strategy issues are tracked separately from knowledge issues.

## Anti-patterns

- Self-flagellation. The post-mortem is for artifact updates, not punishment.
- Generic actions ("study more"). Be specific: which file, which skill, which concept.
- Skipping the post-mortem because the score was good. "Correct + uncertain" is the highest-leverage signal.
