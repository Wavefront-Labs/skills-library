---
id: languages-linguistics.translation.memoq.livedocs-termbases-and-qa-workflow
name: livedocs-termbases-and-qa-workflow
category: languages-linguistics
field: translation
product: memoq
tags: [memoq, memoq-tms, memoq-server, cat-tool, computer-assisted-translation, livedocs, corpora, alignment, translation-memory, tm, term-base, terminology, mqxliff, handoff-package, mqout, mqback, return-package, file-filters, filter-configuration, regex-tagger, cascading-filters, qa, lqa, muses, fragment-assembly, translation]
level: practitioner
status: draft
description: "Translate in memoQ: set up TMs, term bases and LiveDocs corpora, pick the right filter (incl. cascading/regex tagging), work server projects or handoff packages, and run QA before delivery."
sources: ["memoQ documentation (docs.memoq.com)", "memoQ help on LiveDocs, filters and handoff packages"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# memoQ: LiveDocs, term bases and the QA workflow

**Goal:** use memoQ's resources properly — not just a TM — so you leverage old work
without a formal alignment, keep terminology consistent, import tricky formats cleanly,
and deliver files that pass QA and re-export.

*Based on memoQ 9.x–11.x desktop. Menu names, ribbon layout and shortcuts vary between
versions; check the in-app help for yours.*

## 1. Resources
- **Translation memory (TM)**: segment pairs; memoQ shows matches with percentages and
  differences highlighted.
- **Term base (TB)**: concept-oriented terms with forms, usage, forbidden variants. Mark
  terms as forbidden so QA flags them. Import/export via CSV, Excel or TBX.
- **LiveDocs corpora**: collections of documents (monolingual references, bilingual files,
  or *aligned* source/target pairs) memoQ queries like a TM. Drop old translations into
  LiveDocs and memoQ aligns them **automatically** on the fly; you only fix alignment
  where a match looks wrong. Much less effort than full manual alignment up front.
- **Muses / fragment assembly / auto-translatables**: predictive typing and auto-assembled
  fragments (numbers, dates, terms). Configure auto-translatable rules for things like
  product codes so they're carried over correctly.

## 2. Creating a project
1. Project › New Project (or from a template — templates save TM/TB/QA/filter settings).
2. Add documents. Choose **Import with options** for anything non-trivial to select the
   filter and its configuration.
3. Attach TMs (one marked **working**, others reference), TBs, LiveDocs corpora, MT if allowed.
4. Run **Statistics/Analysis** for quoting and **Pre-translate** with the agreed thresholds.

## 3. Filters
- Each format has a filter (Word, Excel, XML, JSON, InDesign IDML, etc.).
- **Cascading filters**: e.g. an Excel file whose cells contain HTML — Excel filter then an
  HTML filter on top.
- **Regex tagger**: turn placeholders (`{0}`, `%s`, `[name]`) into protected inline tags so
  they can't be mistyped. Test the regex on a sample first.
- Save working filter configurations as resources for reuse.

## 4. Server and handoff
- **memoQ server/TMS projects**: check out the project from the server; resources live online;
  deliver from the project (Deliver/Return). Don't leave segments unconfirmed or the
  workflow won't advance.
- **Handoff packages** (`.mqout` from the PM) — import, translate, then create the **delivery
  package** (`.mqback`) to send back.
- Bilingual exchange: memoQ XLIFF (`.mqxliff`) or two-column RTF for reviewers without memoQ.

## 5. QA before delivery
- Configure QA settings (numbers, tags, terminology including forbidden terms, consistency,
  punctuation, length limits). Run QA on the whole project.
- Resolve or ignore with reason in the Resolve errors and warnings view.
- Check that all segments are **Confirmed** and tags are complete, then **Export** target
  files and open them to inspect.
- Run linguistic QA/spell check with the right language dictionaries installed.

## Gotchas
- Wrong filter on import = mangled tags; re-import with the right configuration rather than
  fixing tags by hand.
- Term base language codes (en vs en-GB) must match the project's or terms won't show.
- LiveDocs auto-alignment is approximate; confirm before trusting a high match from it.
- Working TM not writable (read-only from client) — your confirmations won't be stored; ask.
- Version mismatch between your desktop and the client's server can block check-out.

## Verify
- [ ] Project has the correct working TM, reference TMs, TB and LiveDocs attached.
- [ ] Placeholders and codes appear as protected tags, not plain text.
- [ ] QA run shows no unresolved errors; forbidden terms absent.
- [ ] All segments confirmed; exported targets open correctly.
- [ ] Delivery package or server delivery completed and acknowledged.

Related: `languages-linguistics.translation.trados.translation-memory-termbase-and-project-packages`,
`languages-linguistics.translation.translation-revision.bilingual-revision-and-mqm-error-typology`.
