---
id: computing-software.general-digital-literacy.email-clients.inline-images-vs-attachments
name: inline-images-vs-attachments
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-attachments, inline-images, embedded-images, attachments]
level: intro
status: draft
description: "Choose whether to paste a picture into the email body or attach it, control size and quality, and fix images that arrive as attachments or don't show at all."
sources:
  - https://support.microsoft.com/en-us/outlook
  - https://support.google.com/mail
  - https://support.apple.com/guide/mail/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Inline images vs attachments

## Differences
- **Inline (embedded)**: appears in the body where you place it. Good for a screenshot with explanation. Recipient may get it downscaled; hard to save at full quality.
- **Attachment**: separate file, original quality and file name. Best for photos to print, documents, anything to be saved or forwarded.

## How
- **Outlook**: paste (Ctrl+V) or **Insert > Pictures** puts it inline (HTML format only). **Attach File** for attachments. Big pictures: File > Options > Mail > *Image size* or attach and choose *Resize large images* in the Attachments backstage.
- **Gmail**: **Insert photo** icon > *Inline* or *As attachment*. Pasting gives inline.
- **Apple Mail**: drag or paste puts it inline; **Image Size** drop-down in the header (Small/Medium/Large/Actual) resizes.
- Phones: share sheet from Photos inserts inline; Mail on iPhone offers sizes when sending large images.

## Fixing problems
- Inline image arrives as an attachment: the message was plain text, or the recipient's app/filters block HTML images. Send as HTML or attach.
- Recipient sees a blank box with a red X: their client blocks remote images; images *pasted* travel inside the message, images inserted by URL don't.
- Message too big (usually >20-25 MB): send a cloud link instead.

## Privacy
- Remote images in incoming mail can act as **tracking pixels**; keep "ask before downloading pictures" on (Outlook Trust Center, Gmail *Ask before displaying external images*, Apple *Protect Mail Activity*).
- Photo attachments can carry GPS location in EXIF; strip it if sharing with strangers.

## Verify
- [ ] Test email to yourself shows images in place and attachments open at full size.
