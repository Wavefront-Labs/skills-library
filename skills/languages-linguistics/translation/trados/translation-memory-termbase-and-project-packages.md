---
id: languages-linguistics.translation.trados.translation-memory-termbase-and-project-packages
name: translation-memory-termbase-and-project-packages
category: languages-linguistics
field: translation
product: trados
tags: [trados, trados-studio, sdl-trados, rws, cat-tool, computer-assisted-translation, translation-memory, tm, sdltm, termbase, multiterm, sdltb, project-package, sdlppx, sdlrpx, return-package, sdlxliff, batch-tasks, analyze-files, pre-translate, fuzzy-match, qa-checker, verify, alignment, tmx, translation]
level: practitioner
status: draft
description: "Work a Trados Studio project end to end: create it with TMs and a MultiTerm termbase, analyse and pre-translate, translate and confirm, run QA Checker, and exchange project/return packages."
sources: ["RWS Trados Studio online help (docs.rws.com)", "RWS Community Trados Studio forums"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trados Studio: translation memory, termbase and project packages

**Goal:** run a translation job in Trados Studio cleanly: the right resources attached,
matches leveraged, terminology enforced, QA clean, and packages returned so the client
or agency can import your work without problems.

*Written against recent Trados Studio releases (2022–2024 era). Menu names and the
licensing/cloud features shift between versions — confirm against your version's help.*

## 1. Key file types
| File | What it is |
|---|---|
| `.sdltm` | file-based translation memory |
| `.sdltb` | MultiTerm termbase |
| `.sdlxliff` | bilingual working file Studio creates from each source file |
| `.sdlproj` | project file |
| `.sdlppx` | **project package** (agency → translator) |
| `.sdlrpx` | **return package** (translator → agency) |
| `.tmx` / `.tbx` | standard exchange formats for TMs / termbases |

## 2. Receiving a package (most freelance work)
1. **File › Open Package**, select the `.sdlppx`. Studio creates the project with the
   files, TMs and termbases the agency included.
2. Check **Project Settings**: language pair, TMs (and whether you have update rights),
   termbase attached, any MT provider allowed.
3. Open files from the **Files** view; translate in the **Editor**.
4. When done: **Verify** (F8) → fix issues → **Batch Tasks › Update Main/Project TMs** if
   instructed → **File › Create Return Package** to make the `.sdlrpx`. Send that, not the
   loose sdlxliff, unless the agency asks otherwise.

## 3. Creating your own project
1. **New Project** wizard: name, location, source/target languages, source files.
2. Add or create a TM (*Create › New Translation Memory*), and a termbase (create in
   MultiTerm, then add under Project Settings › Language Pairs › Termbases).
3. Choose batch tasks: typically **Analyze Files** and **Pre-translate Files**.
4. The analysis report lists context/100%/fuzzy bands/new words — the basis for quoting.

## 4. Translating efficiently
- **Ctrl+Enter** confirms a segment and saves it to the TM (default shortcut; customisable).
- Match percentages appear per segment; check fuzzies carefully — differences are highlighted
  in the Translation Results window.
- **AutoSuggest** offers term and TM fragment completions as you type.
- Add terms on the fly (termbase must be writable) to keep consistency.
- Keep tags in place: use the tag shortcuts rather than retyping formatting.
- Lock or filter segments (display filter) to work only on new/fuzzy segments if the
  client says 100%/context matches are not to be touched.

## 5. QA
Project Settings › Verification: configure **QA Checker** (segments, inconsistencies,
punctuation, numbers, word list, regex), **Tag Verifier** and **Terminology Verifier**.
Run Verify; review messages in the Messages window. Tune noisy checks rather than ignoring
all warnings.

## 6. Alignment
To build a TM from old translations: **New › Align Documents** (alignment tool), load source
and target files, review the alignment links (especially at headings and lists), import into
a TM. Low-quality alignments pollute the TM — review before import.

## Gotchas
- Opening loose sdlxliff files outside a project loses TM/termbase settings.
- TM penalties and filter settings in packages may hide matches you'd expect.
- File-type settings (e.g. for XML, InDesign) must match what the agency used, or target
  files won't generate.
- "Generate target translations" fails if the source file changed or tags are broken —
  check Verify first.
- Back up TMs; corrupted `.sdltm` files are hard to recover. Export to TMX periodically.

## Verify
- [ ] Project settings show the correct language pair, TM(s) and termbase.
- [ ] Every segment is confirmed (status bar shows 100% translated/confirmed).
- [ ] Verify (F8) produces no unresolved errors.
- [ ] Target files generate and open correctly in their native application.
- [ ] Return package (`.sdlrpx`) or agreed deliverable sent; TM updated if required.

Related: `languages-linguistics.translation.memoq.livedocs-termbases-and-qa-workflow`,
`languages-linguistics.translation.technical-translation.terminology-consistency-and-controlled-language`.
