---
id: creative-arts.photography-fine-art.adobe-lightroom.publish-services
name: publish-services
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, publish-services, lightroom-export, hard-drive-publish, republish, lightroom-classic]
level: practitioner
status: draft
description: "Use Lightroom Classic Publish Services (Hard Drive, Flickr, Adobe Portfolio via plugins) to keep exported folders in sync, republish edits and track what is out."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Publish photos online; Publish services)", "https://helpx.adobe.com/lightroom-classic/desktop/export-photos/exporting-photos-basic-workflow.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Publish services

A publish service is an export target that remembers what was exported. When you edit a published photo, it moves to **Modified Photos to Re-Publish**; one click updates the destination.

## Hard Drive publish (built in) - the most useful
1. Publish Services panel (Library, left) > Hard Drive > **Set Up...**
2. Settings as in Export: location (e.g. `Published/Website`), naming, format, size, sharpening, metadata, watermark.
3. Create **published collections** inside it: `Website - Coastline`, `Gallery - Available prints`, `Phone portfolio`.
4. Drag photos in, click **Publish**. Edit later > collection shows "Modified" > Publish again overwrites files.
- Use for a portfolio folder synced to a website builder, a tablet portfolio, or a gallery's shared Dropbox folder.

## Online services
- Flickr ships built in; others (Adobe Portfolio, SmugMug, Zenfolio, Instagram via plugins such as LR/Instagram) come as plugins: File > Plug-in Manager > Add.
- Removing a photo from a published collection deletes it from the service on next Publish (choose carefully).

## Smart published collections
- Hard Drive services support smart published collections: e.g. "Rating 5 and keyword `portfolio`" auto-feeds the portfolio folder.

## Gotchas
- Changing the service's settings marks every photo for republish.
- Renaming files in the destination breaks tracking.

## Verify
- [ ] After editing one published photo, it appears under "Modified Photos to Re-Publish" and the file on disk updates after Publish.
