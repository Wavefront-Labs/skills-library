---
id: computing-software.digital-privacy-hygiene.privacy-configuration.office-document-inspector
name: office-document-inspector
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, document-inspector, metadata, microsoft-office, redaction]
level: practitioner
status: docs-checked
description: "Use Microsoft Office Document Inspector to remove comments, tracked changes, hidden text and author metadata before sharing Word, Excel or PowerPoint files."
sources:
  - "https://support.microsoft.com/en-us/office/remove-hidden-data-and-personal-information-by-inspecting-documents-presentations-or-workbooks-356b7b5d-77af-44fe-a07f-9aa4d085966f"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Office Document Inspector

**Goal:** the file you send contains only what you see on the page. Source: Microsoft Support, "Remove hidden data and
personal information by inspecting documents, presentations, or workbooks".

## Run it (Word, Excel, PowerPoint)
1. Work on a copy: File > Save As with a new name. Microsoft highly recommends this because removed data often cannot
   be restored, and Undo may not bring it back.
2. In the copy: File > Info > Check for Issues > Inspect Document.
3. Tick the inspectors you want, select **Inspect**, review results, then **Remove All** beside each type to delete.
4. Select Reinspect or Close.
- For .odt, .ods or .odp files, run the inspector every time you save in that format.

## What each app's inspectors cover
- **Word:** Comments, Revisions, Versions and Annotations (comments, tracked-change marks, version information, ink);
  Document Properties and Personal Information (properties, email headers, routing slips, send-for-review info, server
  properties, user name, template name); Headers, Footers and Watermarks; Hidden Text; Custom XML Data; Invisible
  Content.
- **Excel:** Comments and Annotations; Document Properties and Personal Information (also document location, printer
  path, scenario comments, inactive external data connections); Headers and Footers; Hidden Rows and Columns; Hidden
  Worksheets; Custom XML Data; Invisible Content.
- **PowerPoint:** Comments and Annotations; Document Properties and Personal Information; Revision Tracking Data;
  Invisible On-Slide Content; Off-Slide Content; Presentation Notes; Custom XML Data.
- **Visio:** use File > Info > Check for Issues > Remove Personal Information, then tick "Remove these items from the
  document".

## Limits Microsoft documents
- Hidden Text finds only text formatted as hidden, not white-on-white text. Invisible Content does not detect objects
  covered by other objects.
- Word and Excel: hidden-row and hidden-column removal can change formula results. Unhide and review them first. The
  inspector does not detect shapes, charts or pictures inside hidden columns, and hidden rows or columns in a table
  header, list header or PivotTable are unhidden rather than removed.
- Found but not removed (Excel): external links, embedded files or objects, macros and VBA, cached PivotTable, slicer
  and Cube data, Excel Surveys, Scenario Manager scenarios, filters and hidden names. Inspect each by hand or replace it
  with a static picture.
- PowerPoint: it cannot remove pictures in Notes or off-slide objects with animation effects, and finds but cannot
  remove embedded objects and macros. An older PowerPoint version cannot detect or remove revision-tracking data added
  by a newer Microsoft 365 version.
- Excel shared workbooks (Review > Share Workbook): the Comments, Document Properties and Headers inspectors cannot be
  used. Copy the workbook and unshare it first.
- After removal, PowerPoint keeps removing personal information on later saves; the "Change setting" button on the
  notification stops that if you need coauthor names kept on comments.
- Microsoft says it has no access to your document content unless you send it.

## Printing without comments
File > Print > Print All Pages > clear **Print Markup**.

## Checked
Checked 2026-11-08 against the full text of the cited Microsoft Support page. The generic Office root and Learn index
sources were dropped. Removed what the page does not state: the Mac Word preferences path, the Trust Center option,
PDF export properties advice, and the EXIF and named-range gotchas.
Method: documentation only; no commands were run.
