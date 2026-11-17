---
id: creative-arts.comics-and-sequential-art.webcomics.isbn-and-barcode-for-a-comic-collection
name: isbn-and-barcode-for-a-comic-collection
category: creative-arts
field: comics-and-sequential-art
product: webcomics
tags: [webcomics, webcomic-print-collection, isbn-barcode, isbn, ean-13, bookland, metadata]
level: practitioner
status: draft
description: "Get ISBNs and barcodes for a self-published comic collection: national agencies, one ISBN per format, EAN-13 with price add-on, barcode placement and metadata."
sources:
  - https://www.isbn.org/faqs_general_questions
  - https://www.isbn-international.org/
  - https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ISBN and barcode for a collection

## ISBN basics
- An ISBN identifies one edition in one format. Paperback, hardcover and ebook each need their own.
- Buy from your country's agency: Bowker (US), Nielsen (UK/Ireland), the national library or agency
  elsewhere (some countries, e.g. Canada, issue them free). Buying in blocks of 10 is far cheaper than 1.
- A free ISBN from KDP/IngramSpark lists that platform as publisher and usually can't be used elsewhere.
- Periodical single issues may use an ISSN plus a UPC instead (direct-market comics use UPC with an
  issue add-on); collected editions use ISBN.

## Barcode
- Retail barcode for books = **EAN-13** derived from the ISBN-13 (starting 978/979, "Bookland").
- Add a 5-digit **price add-on** (e.g. `51999` = US $19.99, `90000` = no price) if selling in US stores.
- Generate as vector (EPS/PDF) at 100% size (about 1.5 x 1 in minimum), black on white, from a reputable
  generator; IngramSpark generates one for its covers.
- Place on the back cover, usually bottom right, inside the safe area, not over busy art.

## Metadata
- Register title, contributors, format, trim, page count, price, BISAC subject (e.g. `CGN004000 Comics &
  Graphic Novels / Manga / General`), description and cover image with the agency/distributor.
- Assign the ISBN to the exact edition before printing; changes (new trim, new edition) need a new ISBN.
- Legal deposit: many countries require sending copies to the national library.

## Gotchas
- Scaling the barcode down or printing it in colour causes scan failures.
- Reusing one ISBN for hardcover and paperback breaks retailer systems.

## Verify
- [ ] Scan the proof's barcode with a phone app; it returns the right ISBN.
- [ ] Metadata live in the distributor catalogue.
