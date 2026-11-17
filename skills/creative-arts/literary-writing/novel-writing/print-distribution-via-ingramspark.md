---
id: creative-arts.literary-writing.novel-writing.print-distribution-via-ingramspark
name: print-distribution-via-ingramspark
category: creative-arts
field: literary-writing
product: novel-writing
tags: [literary-writing, novel-writing, self-publishing, indie-publishing, ingramspark, print-on-demand, wholesale-discount, returns, bookstore-distribution, library-distribution, pdf-x]
level: practitioner
status: draft
description: "Distribute a self-published print book to bookstores and libraries via IngramSpark: your own ISBN, PDF/X files, wholesale discount and returns settings, and pairing with KDP."
sources: ["https://www.ingramspark.com/", "https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf", "https://www.myidentifiers.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print distribution via IngramSpark

**Goal:** make a print book orderable by bookstores and libraries worldwide through
Ingram's catalogue, priced so you still earn money. Fees and options change; check the
IngramSpark site and File Creation Guide before setup.

## Prerequisites
- **An ISBN you own** for each format (see `isbn-and-imprint-setup`). A KDP-assigned free
  ISBN cannot be used here.
- Interior PDF and cover PDF built to IngramSpark specs (trim, bleed, spine from their
  **cover template generator**, which needs ISBN, page count, paper and binding).

## File requirements (per the File Creation Guide)
- PDF/X-1a:2001 (or PDF/X-3/X-4 as the guide allows), fonts embedded, no transparency
  problems, images at 300 ppi.
- 0.125 in (3.175 mm) bleed where art runs off the page.
- Black-and-white interiors: text in 100% K (rich black text prints fuzzy).
- Cover uses the generated template with the barcode area the template specifies.

## Commercial settings
- **Wholesale discount:** what retailers buy at. Bookstores generally expect around
  40% or more to stock a book; lower discounts (minimum allowed is lower) earn more per
  copy but make bookstore orders unlikely.
- **Returns:** "No returns", "Yes - deliver" (books shipped back to you), or
  "Yes - destroy". Many stores will not order non-returnable books; returns can cost you
  the full wholesale price plus printing.
- Compensation = list price - discount - print cost. Use the publisher compensation
  calculator before committing.

## Pairing with KDP
Common approach: KDP for Amazon (better Amazon royalty and availability), IngramSpark
for everything else, with **KDP Expanded Distribution turned off** to avoid the two
channels competing for the same wholesale accounts. Use your own ISBN on both.

## Gotchas
- Uploading RGB images with rich-black text; check the generated proof (e-proof) carefully.
- Changing page count after generating the cover template — regenerate (spine width changes).
- Setting no returns and expecting bookstore stocking.
- Revision fees may apply after the initial period; finalise files before approval.

## Verify
- [ ] ISBN owned and registered to your imprint.
- [ ] E-proof approved; printed proof ordered and checked.
- [ ] Discount, returns and list price give positive compensation.
- [ ] KDP Expanded Distribution off if using IngramSpark for wide distribution.
