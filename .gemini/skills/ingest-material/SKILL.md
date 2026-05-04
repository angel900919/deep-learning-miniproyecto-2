---
name: ingest-material
description: Process raw study material (markdown, .txt, lecture transcripts, PDFs, code samples) and route it into the structured folder. Produces .study/ingestion-log.md entries and tags each file with the topic(s) it covers. Use when adding new material to the study folder, when the user says "/ingest-material", "ingest this", "process this lecture", or drops a file into material/.
---

# ingest-material

Take raw input from `material/` (or a path the user provides) and produce a structured ingestion record. Does not transform the source — it catalogues, tags, and indexes so downstream skills can find it.

## Inputs required

- The file path(s) to ingest, OR scan `material/` for unindexed files
- `STUDY-ANCHOR.md`
- Existing `topics/*/CONTEXT.md` (to know which topics exist)

## Process

1. **Detect format and route:**
   - `.md` → leave in place; index
   - `.txt` (lecture transcript) → move to `material/transcripts/<source>-<date>.txt` if not already there
   - `.pdf` → leave in place; index. If small (<10 pages), also extract text to `material/readings/<name>.extracted.md`
   - Code file (`.py`, `.ts`, `.rs`, `.go`, `.ipynb`, etc.) → move to `material/code-samples/<lang>/<name>` and capture language
   - Audio/video → expect a transcript already exists in `material/transcripts/`

2. **Read the file head + tail + middle sample** (don't load the whole thing if huge). Identify:
   - Title or subject line
   - Approximate length (lines / pages / tokens)
   - Programming language(s) if code
   - Top-level structure (sections, lectures, chapters)

3. **Tag with topic(s).** Cross-reference with existing `topics/*/CONTEXT.md` source-materials sections. If no topic matches, ask the user: "which topic does this belong to, or should I run `/study-bound` to create a new one?"

4. **Append to `.study/ingestion-log.md`** — one row per file. Never delete rows; mark superseded with `~~strikethrough~~`.

5. **Update the topic's `CONTEXT.md`** Source materials section with the new file.

6. **Flag candidates for downstream skills:**
   - Concept-rich material → suggest `/extract-concepts`
   - Lecture transcript → suggest `/extract-concepts` + `/mental-model` for any new concept
   - Code samples → suggest `/worked-example` to wrap them with explanation
   - Worked-problem source → suggest `/worked-problem`

## Template — `.study/ingestion-log.md` row

```markdown
| Ingested | File | Format | Topic(s) | Length | Notes |
|---|---|---|---|---|---|
| 2026-05-04 | material/lectures/lec-04-paxos.txt | transcript | consensus-algorithms | ~6k words | dense; extract concepts |
| 2026-05-04 | material/code-samples/py/raft.py | code (Python) | consensus-algorithms | 312 LOC | runnable demo |
```

## Constraints

- **Do not transform the source.** Original lives untouched in `material/`. Derived artifacts go elsewhere.
- **One file = one ingestion row.** A multi-lecture playlist gets one row per lecture.
- **Never silently overwrite.** If a file already exists at the destination, ask.
- **Topic tagging is mandatory.** Untagged material can't be retrieved later.

## Anti-patterns

- Summarising the source during ingestion. Summaries belong in `notes/` or `concepts/`, written by `/extract-concepts` or by you.
- Skipping language detection on code. Downstream `/code-from-material` and `/compare-implementations` need it.
- Letting `material/` accumulate without ingestion. The corpus QA skill (`/scan-knowledge`) only sees indexed files.
