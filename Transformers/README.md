# Agentic Study

A spec-driven study workflow built on the same principles as `agentic_workflow/`: artifacts are the program, the chat session is the runtime, every claim is grounded in cited material, and the agent flags itself when it falls back to general knowledge. Two workflows — one for software / CS / AI study (CODE-LEARN), one for general subjects like engineering, accounting, finance (CONCEPT-LEARN). Same scaffolding for both.

> **Core principle:** the study folder is a knowledge corpus the agent can index, query, and answer from with citations. Everything you ingest becomes addressable. Everything you understand becomes a concept file. Everything you've practised becomes a worked example or worked problem. The mastery state of every concept lives in one tracker.

---

## Setup

```bash
# 1. Create your subject folder by copying the template
cp -R agentic_study/template my-subjects/distributed-systems
cd my-subjects/distributed-systems

# 2. Install the skills
cp -R ../../agentic_study/skills .claude/skills
git init

# 3. Anchor the subject (interactive)
/study-anchor
```

`/study-anchor` interrogates you on subject ID, mode (CODE-LEARN vs CONCEPT-LEARN), Bloom targets, deadline, retention strategy, source-of-truth policy, and fallback policy. Writes `STUDY-ANCHOR.md`. Everything downstream reads it.

---

## The study loop

```
ANCHOR → BOUND → INGEST → EXTRACT → MODEL → PRACTICE → GRILL → REVIEW → POSTMORTEM
                                                                    ▲
                                                                    └── feedback ──┐
```

Eight phases. Same shape for CODE-LEARN and CONCEPT-LEARN — only the **PRACTICE** phase splits (worked examples vs worked problems).

---

## Folder layout

Drop this skeleton into any new study subject (it's pre-built in `agentic_study/template/`).

```
my-subject/
├─ AGENTS.md                          # agent's loading dock — read this first
├─ STUDY-ANCHOR.md                    # mode, goals, fallback policy
├─ GLOSSARY.md                        # canonical terms
│
├─ topics/                            # one folder per topic (capability boundary)
│  └─ <topic>/
│     ├─ CONTEXT.md                   # ≤200 lines — scope, prereqs, learning goals
│     ├─ concepts/<concept>.md        # one file per atomic idea
│     ├─ mental-models.md             # decision-aid models
│     ├─ flashcards.md                # Anki/Mochi-importable
│     ├─ examples/                    # CODE-LEARN: code; CONCEPT-LEARN: worked problems
│     │  ├─ <name>/                   # CODE-LEARN folder
│     │  │  ├─ README.md, code, expected.txt, exercises.md
│     │  └─ <problem-id>.md           # CONCEPT-LEARN file
│     ├─ derivations/<name>.md        # CONCEPT-LEARN only
│     ├─ formula-sheet.md             # CONCEPT-LEARN only
│     └─ progress.md                  # per-topic mastery view
│
├─ material/                          # RAW INPUTS — never edited, only indexed
│  ├─ lectures/                       # transcripts (.txt, .md)
│  ├─ readings/                       # PDFs, articles, .md, .txt
│  ├─ code-samples/<lang>/            # original source code
│  └─ transcripts/                    # video/audio transcripts
│
├─ notes/                             # YOUR synthesised notes (not raw)
│
├─ practice/
│  ├─ problem-sets/                   # CONCEPT-LEARN
│  └─ projects/                       # CODE-LEARN
│
├─ reviews/<YYYY-MM-DD>.md            # daily spaced-repetition queues
├─ exams/<date>-<name>/               # past papers + post-mortems
│  ├─ paper.md, my-attempt.md, postmortem.md
│
├─ .study/                            # tracking metadata
│  ├─ ingestion-log.md                # what's been processed
│  ├─ progress-tracker.md             # per-concept mastery state
│  └─ current-questions.md            # stuck questions (gitignored)
│
└─ .claude/skills/                    # the skill library
```

**Three rules baked into the layout:**
1. `material/` is **immutable**. Originals never change.
2. Every `CONTEXT.md` capped at 200 lines — keeps the agent in the Smart Zone.
3. Fallback to general knowledge requires the `[OUTSIDE MATERIAL]` flag — no silent coverage of gaps.

---

## The 8 phases

### 1. ANCHOR (once per subject)
`/study-anchor` → `STUDY-ANCHOR.md`. Sets the mode (CODE-LEARN / CONCEPT-LEARN), Bloom targets, fallback policy.

### 2. BOUND (once per topic)
`/study-bound` → `topics/<topic>/CONTEXT.md` + folder skeleton. Topic = unit of study, days-to-master.

### 3. INGEST (every time you add material)
`/ingest-material` → tagged entry in `.study/ingestion-log.md`; routes file to the right `material/` subfolder; tags it with topic(s). Original is never modified.

### 4. EXTRACT (after ingestion)
`/extract-concepts` → one `concepts/<id>.md` per atomic idea, every claim cited.
`/build-glossary` → updates root `GLOSSARY.md` with new canonical terms.
`/make-flashcards` → atomic Anki cards into `topics/<topic>/flashcards.md`.

### 5. MODEL (for hard concepts)
`/mental-model` → `topics/<topic>/mental-models.md` entries. 3–7 primitives + relationships + "when this model breaks" + a self-test question. Decision-aid framing, not definition-rephrasing.

### 6. PRACTICE — branches by mode

**CODE-LEARN:**
- `/worked-example` → runnable code in target language (README + code + expected output + exercises)
- `/code-from-material` → grounded code generation, citing every borrowed pattern
- `/compare-implementations` → same example across 2–4 languages, side by side

**CONCEPT-LEARN:**
- `/worked-problem` → fully-shown solution, every step + reason + units
- `/derive-from-first-principles` → axiom → target derivation, every operation justified
- `/formula-sheet` → dense topic reference with units, validity conditions, citations

### 7. GRILL (test understanding)
`/grill-on-topic` → Socratic quiz, one question at a time, climbing Bloom levels until a confident gap appears. Stops on first gap, repairs via:
`/explain-back` → Feynman test: user explains, agent identifies gaps against the canonical with citations.

### 8. REVIEW (daily)
`/spaced-review` → produces `reviews/<date>.md` queue from all `flashcards.md` weighted by progress and last-review interval (SM-2-lite). Pass/fail updates `.study/progress-tracker.md`.

`/study-progress` → maintains the tracker. Promotes concepts through UNREAD → READING → UNDERSTOOD → APPLIED → RETAINED.

### After-the-fact: POST-MORTEM
After any exam/project/interview: `/study-postmortem` → `exams/<date>-<name>/postmortem.md`. Every wrong answer maps to one root cause and one concrete artifact update (new concept, new flashcards, demoted progress, new mental model). A post-mortem with no artifact updates is decoration.

### The "ask anything" entry point
`/scan-knowledge` — run once at the start of any study session. Indexes the corpus and lets you ask freely. Every answer cites its sources. Every fallback to general knowledge is prefixed `[OUTSIDE MATERIAL]`.

---

## CODE-LEARN example: studying distributed systems

```bash
cp -R agentic_study/template my-subjects/distributed-systems
cd my-subjects/distributed-systems
cp -R ../../agentic_study/skills .claude/skills

# 1. Anchor (10 min)
/study-anchor
# Mode: CODE-LEARN
# Why: ship a Raft implementation as portfolio piece; pass MIT 6.824
# Deadline: 2026-09-01
# Bloom: Apply for raft, paxos; Understand for cap, flp
# Time: 8 h/week
# Retention: Anki, daily 15 min
# Source-of-truth order: 6.824 lectures > Designing Data-Intensive Apps > original papers
# Output format: Go 1.22, gofmt, table-driven tests
# Fallback: YES, with [OUTSIDE MATERIAL] flag

# 2. Bound a topic (5 min)
/study-bound consensus-algorithms
# Goals: explain Paxos roles, implement Raft leader election, derive FLP impossibility intuition

# 3. Drop some material into material/ and ingest
cp ~/downloads/lec-04-paxos.txt material/lectures/
cp ~/downloads/raft-paper.pdf material/readings/
cp ~/projects/raft-go/election.go material/code-samples/go/
/ingest-material

# 4. Extract concepts and build the spine
/extract-concepts        # produces concepts/{paxos-basic, raft-leader-election, cap-theorem,
                          #   flp-impossibility, ...}.md
/build-glossary
/make-flashcards consensus-algorithms

# 5. Build mental models for the hard ones
/mental-model paxos-basic           # primitives: proposer, acceptor, learner; ballot; promise/accept
/mental-model raft-leader-election  # primitives: term, vote, log-match; leader/follower/candidate

# 6. Practice (CODE-LEARN flavour)
/worked-example raft-leader-election     # runnable Go example with expected.txt + exercises
/code-from-material "implement RequestVote RPC handler from scratch"
# Output cites: concepts/raft-leader-election.md, examples/raft-leader-election/, material/code-samples/go/election.go
# Outside-material decisions (e.g. specific Go test idiom) are flagged inline.
/compare-implementations raft-leader-election --langs go,rust

# 7. Grill yourself
/grill-on-topic consensus-algorithms
# Q1 (Understand): "In your own words, what does the Raft term solve?"
# (you answer; agent grades against concepts/raft-leader-election.md)
# Q2 (Apply): "Walk through electing a new leader after a partition heals; what messages fire?"
# Confident gap exposed → /explain-back raft-leader-election

# 8. Review (daily)
/spaced-review
# Today's queue: 24 cards, time-box 15 min.
# After: q-001 PASS, q-014 FAIL → suggest /explain-back basis-and-dimension

# After 6.824 problem set
/study-postmortem
# Wrong answer Q3 mapped to: missing concept "log compaction"
# → /extract-concepts on raft paper §7 → 3 new flashcards → demote raft-leader-election to UNDERSTOOD
```

---

## CONCEPT-LEARN example: studying CFA Level 1 ethics + quantitative methods

```bash
cp -R agentic_study/template my-subjects/cfa-l1
cd my-subjects/cfa-l1
cp -R ../../agentic_study/skills .claude/skills

# 1. Anchor
/study-anchor
# Mode: CONCEPT-LEARN
# Why: pass CFA Level 1 May 2026
# Deadline: 2026-05-15
# Bloom: Apply for ethics scenarios; Understand for quant formulas
# Time: 12 h/week
# Source-of-truth order: CFA Institute curriculum > Schweser > Wiley
# Notation: standard finance (NPV, IRR, σ); USD; %ages as 0.05 not 5%
# Fallback: NO  ← regulated material; do not invent

# 2. Bound topics
/study-bound ethics-standards
/study-bound quant-time-value-of-money
/study-bound quant-statistics

# 3. Ingest curriculum chapters
/ingest-material   # processes 5 PDFs + 2 transcript .txt files

# 4. Extract concepts + build glossary + flashcards
/extract-concepts ethics-standards
/extract-concepts quant-time-value-of-money
/build-glossary
/make-flashcards quant-time-value-of-money

# 5. CONCEPT-LEARN-specific: formula sheet + derivations
/formula-sheet quant-time-value-of-money
# Produces dense one-page reference: PV, FV, annuities, perpetuities, with units and validity.

/derive-from-first-principles annuity-due-from-ordinary-annuity
# Walks: ordinary annuity formula → (×(1+r)) shift → annuity-due formula.

# 6. Practice
/worked-problem npv-mutually-exclusive-projects
# Full algebra, units (USD, %), assumption naming, sanity check.

# 7. Mental models for tricky ideas
/mental-model standards-of-conduct
# Primitives: client > employer > self; disclosure default ON; written record always.

# 8. Grill + Feynman
/grill-on-topic ethics-standards
# Q1: "Client A and Client B both want shares in a small IPO. Walk through your duty."
# Gap exposed → /explain-back fair-dealing-standard

# 9. Review
/spaced-review

# After mock exam
/study-postmortem
# Wrong: 3 ethics scenarios, 1 IRR question.
# Root causes:
#   - Ethics: misread "material non-public information" trigger → strategy note + 5 new edge flashcards
#   - IRR: forgot to discount the terminal value → demote npv-mutually-exclusive-projects to READING
```

---

## Multi-format material — what works out of the box

| Format | Where it goes | Indexed by |
|---|---|---|
| Markdown notes (`.md`) | `material/readings/` | yes |
| Plain text (`.txt`) | `material/readings/` (or `material/transcripts/` if a lecture) | yes |
| Lecture transcripts | `material/transcripts/<source>-<date>.txt` | yes |
| PDFs | `material/readings/` | by heading + page; small PDFs auto-extracted to `.extracted.md` |
| Code samples | `material/code-samples/<lang>/` | yes; language tagged |
| Jupyter notebooks | `material/code-samples/<lang>/` | yes |
| Audio/video | not directly — transcribe first, then ingest the transcript | via transcript |
| Images / diagrams | `material/readings/` adjacent to the related text | indexed by reference, not content |

`/ingest-material` routes by extension and content; downstream skills (`/extract-concepts`, `/code-from-material`, `/scan-knowledge`) walk the indexed corpus.

---

## After scanning, what you can do

`/scan-knowledge` indexes the corpus and stays loaded. Then any of:

- **Free question:** "Why does Raft prefer one leader over Paxos's multiple proposers?"
  - Answers from corpus, citing `concepts/` + `material/`.
- **`/code-from-material <task>`** (CODE-LEARN): generates code from corpus, flags any `[OUTSIDE MATERIAL]` decision.
- **`/grill-on-topic <topic>`**: agent quizzes you, climbing Bloom levels.
- **`/explain-back <concept>`**: you explain; agent identifies gaps with citations.
- **`/spaced-review`**: today's review queue from your flashcards.

If a question can't be grounded in the corpus and your fallback policy is YES, the agent answers from general knowledge with the `[OUTSIDE MATERIAL]` prefix and tells you exactly which gap triggered it. That's the cue to `/ingest-material` something new or `/extract-concepts` from existing material.

---

## Skill cheat sheet

| Goal | Skill |
|---|---|
| **Setup** | |
| Anchor a subject | `/study-anchor` |
| Bound a topic | `/study-bound` |
| **Material → corpus** | |
| Process raw input | `/ingest-material` |
| Atomic concept files | `/extract-concepts` |
| Canonical glossary | `/build-glossary` |
| Atomic flashcards | `/make-flashcards` |
| **Understanding** | |
| Decision-aid model | `/mental-model` |
| **Practice — CODE-LEARN** | |
| Runnable code example | `/worked-example` |
| Generate code from corpus | `/code-from-material` |
| Same example, multiple languages | `/compare-implementations` |
| **Practice — CONCEPT-LEARN** | |
| Fully-worked problem | `/worked-problem` |
| Topic formula sheet | `/formula-sheet` |
| Step-by-step derivation | `/derive-from-first-principles` |
| **Test yourself** | |
| Socratic quiz | `/grill-on-topic` |
| Feynman explain-back | `/explain-back` |
| **Memory** | |
| Daily review queue | `/spaced-review` |
| Mastery tracker | `/study-progress` |
| **Use the corpus** | |
| Index + Q&A entry point | `/scan-knowledge` |
| **Close the loop** | |
| Post-exam debrief | `/study-postmortem` |

---

## Three rules that decide everything

If you only remember three things:

1. **Cite or flag.** Every answer from the corpus is cited; every fallback is `[OUTSIDE MATERIAL]`.
2. **Atomicity over batching.** One concept per file, one fact per flashcard, one question per grill turn, one root cause per post-mortem entry.
3. **Promote on evidence, not on optimism.** UNDERSTOOD requires `/explain-back`; APPLIED requires a worked example or problem; RETAINED requires three spaced-rep passes.

Everything else is scaffolding around those three.
