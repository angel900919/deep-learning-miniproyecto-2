---
name: explain-back
description: Feynman technique — the user explains a concept; the agent listens, identifies the gap precisely, and surfaces the source citation that fills it. Promotes a concept's state on success. Use when /grill-on-topic exposed a gap, when the user says "/explain-back", "let me explain X", or for any concept stuck at READING.
---

# explain-back

Run the Feynman test: the user explains the concept aloud (in chat); the agent reads against the canonical material and pinpoints exactly what's missing. The most powerful debugging tool for understanding.

## Inputs required

- Concept ID
- `concepts/<concept-id>.md`
- Cited material spans

## Process

1. **Set the prompt:** "Explain <concept> as if to a peer who's never seen it. Use your own words, no lookup. Stop when you've covered the key idea."

2. **Wait for the user's full explanation.** Do not interrupt.

3. **Compare against the canonical** — load `concepts/<concept-id>.md` plus the cited material spans. Identify:
   - **Missing primitives** — things the canonical defines that the user didn't mention
   - **Wrong claims** — assertions that contradict the source
   - **Vague language** — places where the user used "stuff" or "things" or "kind of"
   - **Strong understanding** — places where the user got it right

4. **Respond in this format:**
   ```
   ## What you got right
   - <bullet>
   - <bullet>

   ## What you missed
   - <missing primitive 1> — see <source>
   - ...

   ## What was wrong
   - <wrong claim> → canonical: <quote + citation>

   ## Vague spots
   - "you said X is kind of Y" — be precise: <canonical wording + citation>

   ## Suggested next step
   - Re-read <source>:L<lines>, then re-explain.
   - OR /worked-example <concept> if the gap is application, not definition.
   ```

5. **Update `progress-tracker.md`** — promote to UNDERSTOOD if no missing/wrong (vague-only is OK); else stay at READING and log the gap to `.study/current-questions.md`.

## Constraints

- Don't hint while the user is explaining. Wait until they're done.
- Identify exact gaps; "you got it kind of right" is itself a vague-spot anti-pattern.
- Always cite. The user needs to know where to re-read.
- Promotion to APPLIED requires `/worked-example` or `/worked-problem`, not Feynman alone.

## Anti-patterns

- Letting the user check the source mid-explanation. The whole point is no-lookup.
- Generic "you should review X" feedback. Be surgical: line and source.
- Promoting from one good explanation. UNDERSTOOD is a state; one good run is evidence, not proof.
