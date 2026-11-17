---
id: creative-arts.literary-writing.novel-writing.isbn-and-imprint-setup
name: isbn-and-imprint-setup
category: creative-arts
field: literary-writing
product: novel-writing
tags: [literary-writing, novel-writing, self-publishing, indie-publishing, isbn, imprint-setup, bowker, myidentifiers, nielsen, ean-13, barcode, publisher-of-record]
level: practitioner
status: draft
description: "Buy and assign ISBNs for a self-published book: national agencies (Bowker, Nielsen, free in Canada), one ISBN per format, imprint name as publisher of record."
sources: ["https://www.isbn-international.org/", "https://www.myidentifiers.com/", "https://www.bac-lac.gc.ca/eng/services/isbn-canada/Pages/isbn-canada.aspx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ISBNs and imprint setup

**Goal:** own your ISBNs so your imprint is the publisher of record everywhere the book
is sold, and assign them correctly per edition.

## Where ISBNs come from
ISBNs are issued by one national agency per country (International ISBN Agency):
- **US:** Bowker (myidentifiers.com). Bought singly or in blocks; blocks of 10 or more cost
  far less per ISBN, and most authors use several per book.
- **UK and Ireland:** Nielsen ISBN Agency.
- **Canada:** free through Library and Archives Canada (ISBN Canada).
- **Australia:** Thorpe-Bowker.
Buy from your national agency; resellers' ISBNs may list the reseller as publisher.

## One ISBN per format and edition
- Hardcover, paperback, large print, EPUB ebook and audiobook each need their own ISBN
  (ebooks sold only on Amazon can use the ASIN; audiobook distributors vary).
- A new edition (substantial content change) or new trim/binding = new ISBN.
  Correcting typos or a new cover does not need one.

## Imprint
- Choose an imprint (publisher) name; check it is not already used by a known publisher.
  It can be a trading name of you as an individual; local business registration rules vary.
- Enter the same imprint name in Bowker/Nielsen records, KDP, IngramSpark and the
  copyright page.

## Assign and register
1. In the agency portal, assign an ISBN to the title: title, contributor, format, trim,
   page count, price, publication date, BISAC subject.
2. Put the ISBN on the copyright page and the back cover barcode (print).
3. Barcode: EAN-13 encoding the ISBN-13, usually with a 5-digit price add-on (`90000`
   means no price). KDP and IngramSpark cover templates can generate it.

## Gotchas
- Reusing a paperback ISBN for the ebook.
- Using a platform-provided free ISBN and later wanting the same edition elsewhere.
- Not updating agency metadata, so library and bookstore systems show the wrong details.

## Verify
- [ ] ISBN list kept: which number = which format of which title.
- [ ] Imprint name identical across agency record, platforms and copyright page.
- [ ] Barcode scans to the right ISBN-13.
