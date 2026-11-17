---
id: media-communication.publishing.indexing.back-of-book-index-terms-cross-references-and-locators
name: back-of-book-index-terms-cross-references-and-locators
category: media-communication
field: publishing
product: indexing
tags: [indexing, indexer, back-of-book-index, book-index, index-entries, headings, subheadings, cross-references, see-also, locators, page-ranges, double-posting, alphabetisation, word-by-word, letter-by-letter, embedded-indexing, indesign-index, word-index-fields, cindex, sky-index, macrex, chicago-manual-of-style, iso-999, publishing, book-production]
level: practitioner
status: draft
description: "Write a usable back-of-book index: choose terms readers will look up, structure headings and subheadings, add see and see also references, keep locators accurate, and edit to length."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Back-of-book index: terms, cross-references and locators

**Goal:** a reader looking up anything the book substantially discusses finds it in one
or two steps, under the word they'd actually think of.

## 1. Before you start
- Confirm: **final pagination** (indexing on unstable pages wastes everything), **allowed
  length** (pages or lines — the designer or production editor sets it), style (Chicago
  and ISO 999 are common references; the house may have its own), alphabetisation (word-by-
  word vs letter-by-letter), and whether it's a **standalone** index (dedicated software
  like Cindex, Sky Index or Macrex) or **embedded** (tags placed in Word or InDesign that
  regenerate if pages move).
- Skim the whole book before marking anything; you need to know its main subjects.

## 2. Choose terms (analysis, not word-matching)
- Index **substantive discussion**, not passing mentions. A name in a list of examples
  usually doesn't qualify; a paragraph about that person does.
- Use the **reader's vocabulary** as headings; put the author's specialised terms as
  headings too if readers will learn them, and connect with cross-references.
- **Concepts discussed without being named** still get entries — a concordance tool can't
  find them; that's why indexing is human work.
- Prefer **nouns** and noun phrases as headings; keep subheadings concise and starting with
  the key word.

## 3. Structure
```
climate policy, 45–52
    carbon taxes, 47–49
    in the European Union, 50
    See also emissions trading
emissions trading, 53–60
carbon taxes. See under climate policy   (or double-post with locators)
```
- **Subheadings** when a heading would otherwise carry more than about 5-7 undifferentiated
  locators (a common rule of thumb). A string of 20 page numbers is useless.
- **Double-posting** (the same locators under two headings) is often better than a "See"
  reference when the entry is short.
- Keep to two levels of subheading at most in most trade and academic books.

## 4. Cross-references
- **See**: from a term not used to the term used ("cars. See automobiles"). The "See"
  heading has **no locators**.
- **See also**: to related headings that have additional information.
- Check every cross-reference **points to a heading that exists** and isn't itself a
  "See" (no blind or circular references).

## 5. Locators
- Page ranges for continuous discussion (45–52, with an en dash), not 45, 46, 47...
- Conventions for figures, tables and notes (e.g. 112f, 112t, 230n4) — follow house style.
- Embedded indexes: place range markers correctly so ranges survive repagination.

## 6. Alphabetisation gotchas
- Word-by-word puts "New York" before "Newark"; letter-by-letter reverses them.
  Choose one and apply throughout.
- Names: surname first; particles ("de", "van", "Mac") follow the person's own/national
  convention — check authoritative sources.
- Numbers and symbols: decide whether they file as spelled out or at the start.
- Ignore leading articles ("The", "A") in titles when sorting, per most styles.

## 7. Edit the index
Read it as a reader: merge synonymous headings, split overloaded ones, check consistency of
singular/plural and capitalisation, cut entries for trivial mentions to meet the length,
and spot-check a sample of locators against the pages (aim to check every one if time permits).

## Verify
- [ ] Indexed on final pages (or embedded tags tested after repagination).
- [ ] No heading has a long string of undifferentiated locators.
- [ ] Every See/See also target exists; no blind references.
- [ ] Alphabetisation rule consistent throughout.
- [ ] Spot-checked locators are correct; index fits the allotted space.
