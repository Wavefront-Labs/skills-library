---
id: humanities.oral-history-and-tradition-keeping.transcription-and-archiving.transcribing-indexing-and-depositing-interviews
name: transcribing-indexing-and-depositing-interviews
category: humanities
field: oral-history-and-tradition-keeping
product: transcription-and-archiving
tags: [transcription-and-archiving, oral-history, transcription, verbatim-transcription, transcription-style-guide, baylor-style-guide, audit-checking, audit-edit, timestamps, time-coded-index, interview-summary, ohms, oral-history-metadata-synchronizer, keywords, subject-headings, speech-to-text, whisper, asr, wav, bwf, file-naming, checksums, metadata, dublin-core, archival-deposit, digital-preservation]
level: practitioner
status: draft
description: "Make interviews usable and durable: verbatim transcription to a style guide, audit-checking against audio, time-coded indexes (e.g. OHMS), sound file and metadata practice, and archival deposit."
sources:
  - "Baylor University Institute for Oral History. Style Guide (transcription)"
  - "OHMS (Oral History Metadata Synchronizer), University of Kentucky Libraries"
  - "Oral History Association. Principles and Best Practices (2018)"
  - "Digital Preservation Coalition. Digital Preservation Handbook"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transcribing, indexing and depositing interviews

**Goal:** turn a raw recording into an archive-ready package — preserved audio, accurate
transcript and/or time-coded index, complete metadata and paperwork — that researchers can
find and use decades later.

## 1. Look after the master first
- Keep the original **WAV** (or BWF) as the **preservation master**; never edit it. Make
  derived access copies (MP3/AAC) for listening.
- **File naming**: consistent, no spaces, sortable, e.g.
  `<PROJECT>_<NNN>_<NarratorSurname>_<YYYYMMDD>_part01.wav`.
- Generate **checksums** (MD5/SHA-256) on ingest so you can detect corruption later.
- Keep **3 copies, 2 media, 1 off-site** until deposit.

## 2. Transcribe or index? Decide per project
- **Full transcript**: best for searchability and publication; time-consuming (often quoted
  as 4–8+ hours per recorded hour by hand; less when correcting automatic speech
  recognition). *Unconfirmed:* actual rates vary with audio quality and accent.
- **Time-coded index/summary**: segment-by-segment summaries with keywords, linked to
  audio — faster, keeps the voice primary. Tools like **OHMS** sync indexes and transcripts
  to audio online.
Many projects do both: an index for all interviews, transcripts for some.

## 3. Transcription standards
Use a **style guide** (e.g. Baylor's) and keep a project-specific supplement of names and
terms. Typical conventions:
- **Verbatim, lightly cleaned**: keep the narrator's words, grammar and dialect; drop most
  "um/uh" and false starts *unless* meaningful. State your policy.
- Don't "correct" dialect into standard spelling or render it as stereotyped phonetic
  spelling; use standard spelling for standard words.
- Mark **[inaudible 00:23:15]**, **[laughs]**, **[pause]**, **[crosstalk]** sparingly and
  consistently; time-stamp uncertain passages.
- Speaker labels (initials) consistently; time-stamps every few minutes or at paragraph breaks.
- Header: project, narrator, interviewer, date, place, duration, file names, transcriber.

**Speech-to-text (e.g. Whisper-class models)**: good first drafts, but errors cluster on
names, places, dialect and overlapping speech, and they sometimes **hallucinate** fluent
text over silence or noise. Always audit. Check your consent covers sending audio to any
cloud service; prefer local processing for sensitive material.

## 4. Audit-check
A second person listens to the whole recording against the transcript, correcting errors
and flagging queries. Then, if your protocol allows, the **narrator reviews** for spellings
and factual slips — but the transcript should still reflect what was said; record any
narrator corrections as such (e.g. bracketed notes), not silent rewrites.

## 5. Indexing and summary
- **Summary**: 200–500 words on the interview's content and significance.
- **Segment index**: every ~5 min or topic change: time code, segment title, short synopsis,
  keywords, names, places.
- **Keywords**: use controlled vocabulary where possible (Library of Congress Subject
  Headings, your archive's thesaurus) plus local terms the community uses.

## 6. Deposit
Agree the receiving archive *before* interviewing, and use their specs. Package:
- preservation masters + checksums, access copies;
- transcript/index (searchable PDF and editable format, e.g. DOCX/TXT/XML);
- signed release and any **restrictions** (time-coded), consent notes;
- metadata (Dublin Core or the archive's schema): narrator, interviewer, date, place,
  language, duration, rights, subjects;
- photographs and documents lent or donated (with their own permissions);
- project documentation: aims, interview guide, style guide, interviewer notes.

## Gotchas
- Editing the master to "clean" noise — always work on copies.
- Restrictions on paper that never reach the catalogue.
- Proprietary or obsolete formats (old recorder formats, CD-R only).
- Transcribers guessing at names instead of flagging.

## Verify
- [ ] Untouched WAV masters with checksums exist in three copies.
- [ ] A style guide and names list were used; dialect respected.
- [ ] Every transcript was fully audit-checked against audio, including any ASR draft.
- [ ] A summary and time-coded index with controlled keywords exist.
- [ ] Deposit package includes masters, text, release, restrictions and metadata, to the archive's spec.
