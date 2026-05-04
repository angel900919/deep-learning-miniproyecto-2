---
name: make-flashcards
description: Generate Anki/Mochi-importable flashcards for a topic from concepts/, mental-models, and source material. Produces topics/<topic>/flashcards.md (markdown table) and optionally an Anki .apkg via deck-export script. Each card is atomic (one-fact-per-card) and tagged. Use after /extract-concepts, when the user says "/make-flashcards", "Anki cards for X", "spaced repetition for this".
---

# make-flashcards

Produce `topics/<topic>/flashcards.md` — a flat table of cards in a format every spaced-repetition tool can import. Each card is one fact, one prompt, one answer.

## Inputs required

- `topics/<topic>/CONTEXT.md`
- All `topics/<topic>/concepts/*.md`
- `topics/<topic>/mental-models.md`
- `STUDY-ANCHOR.md`

## Process

1. **One fact per card** — atomic. "Define X and explain Y" is two cards.

2. **Mix card types** by Bloom level:
   - **Recall** — "What is X?" → definition
   - **Cloze** — "The {{c1::CAP theorem}} states that…" (Anki cloze syntax)
   - **Apply** — "Given input X, what's the output of algorithm Y?"
   - **Compare** — "Difference between X and Y?"
   - **Reverse** — front and back swapped (for pairs that need both directions)

3. **Generate cards from each concept file** — at minimum one Recall + one Apply per concept.

4. **Tag every card** — `topic::<topic-id>::<concept-id>` and Bloom level.

5. **Cite source** — every card carries a citation in the back so the learner can re-read context if confused.

6. **Write to `flashcards.md`** as a pipe-table. Compatible with Anki's "Basic + Tags" import via the `mdcards` script (see `scripts/`).

7. **Run dedup** — same prompt across two cards → keep the more general one.

## Template — `flashcards.md`

```markdown
# Flashcards — <topic>

| ID | Front | Back | Tags |
|---|---|---|---|
| q-001 | What does CAP stand for? | Consistency, Availability, Partition tolerance. <br><sub>Source: material/readings/brewer.md:p2</sub> | recall, topic::distributed::cap |
| q-002 | The {{c1::CAP theorem}} says you can pick at most {{c2::two}} of consistency, availability, partition tolerance. |  | cloze, topic::distributed::cap |
| q-003 | A network partition has occurred. Your system chose AVAILABILITY. What is sacrificed and why? | Strong consistency. With the partition, two replicas may diverge; serving requests on both means later reconciliation is required. <br><sub>Source: material/lectures/lec-04.txt:L412</sub> | apply, topic::distributed::cap |
| q-004 | Compare CAP and PACELC: extra dimension PACELC adds? | When there is no partition, the trade-off is between Latency and Consistency. <br><sub>Source: material/readings/abadi-pacelc.md</sub> | compare, topic::distributed::pacelc |
```

## Constraints

- One fact per card. Atomic.
- Cloze cards use Anki syntax `{{c1::...}}`.
- Every card carries a citation.
- Apply-level cards must include the input scenario in the front, never just "what is X".
- Cap per file: 200 cards. More = split by sub-topic.

## Anti-patterns

- Long answers. If the back is more than 3 sentences, split the card.
- Repeating the same fact in 5 different framings. One card; the SR tool handles repetition.
- Cards without source citations — when you forget context months later, the citation saves you.
- Cards on trivia the source treats as decorative. Stick to concepts the topic actually requires.
