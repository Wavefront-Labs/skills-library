---
id: computing-software.systems-network-administration.paperless-ngx.workflow-actions
name: workflow-actions
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, workflow-actions, password-removal, move-to-trash, email-action, assignment]
level: practitioner
status: docs-checked
description: "Use workflow actions: assignment, removal, email, webhook, move to trash, password removal, remote OCR and AI suggestions, with their ordering rules."
sources:
  - "https://docs.paperless-ngx.com/usage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow actions

Actions apply sequentially in sort order.

- Assignment: can assign title (see workflow placeholders, Jinja templates), tags, correspondent, document type, storage path, document owner, view and/or edit permissions for users or groups, and custom fields optionally with a value. A custom field without a value is only added and any existing value is left untouched; with a value it overwrites an existing value.
- Removal: removes all of, or specific sets of, tags, correspondents, document types, storage paths, document owner, view and/or edit permissions, and custom fields.
- Email: requires a mail server to be configured. You specify the recipient address(es) separated by commas, the subject and body (which can include placeholders), and whether to attach the document.
- Webhook: sends a POST request to a URL, with a body as text or key-value pairs, JSON or form-data encoding, and headers. See the workflow-webhooks-placeholders skill.
- Move to Trash: moves the document to the trash; it can be restored until the trash is emptied (after the configured delay or manually). It always executes at the end of the workflow run regardless of its position, no other workflow executes on the document afterwards, and in a consume pipeline it aborts the consumption and deletes the file.
- Password Removal: tries the listed passwords (separated by commas or new lines) in order until one unlocks the PDF. It never modifies a file in place: the decrypted content is consumed as a new document version and the encrypted original stays in version history. With Consumption Started, the first version is typically stored with no extracted text because OCR cannot process an encrypted PDF; the decrypted file is then re-consumed as a second version with normal text extraction. With Added, Updated and Scheduled, the decrypted content is queued as a new version right away. Passwords are a simple list without descriptions, so create separate workflows for different PDF types.
- Remote OCR: only works with a Consumption Started trigger; takes no options. See the remote-ocr-azure skill.
- Apply AI Suggestions: requires AI features to be enabled and works with every trigger except Consumption Started. You choose which suggestions to apply (title, tags, correspondent, document type, storage path, created date), whether to create missing items (storage paths are never created) and whether to overwrite existing values (by default a field is only filled if empty; suggested tags are always added and never replace existing tags). Documents with empty or whitespace-only processed text are skipped. The action is queued and runs in the background. Each matching document queries the AI service, which may incur costs and have privacy implications, and a workflow matching many documents can occupy the task queue and delay consumption; consider narrowing the trigger filters, running in small batches and/or increasing workers.

## Checked
Date: 2026-11-07
Pages read in full: none in full. I read the whole Workflows section of usage (triggers, each action type, placeholders, permissions).
Corrections: removed "Test a workflow on one document before widening its filters" (not on the page); replaced "needs SMTP configured" with the page's "mail server configured"; made the webhook and remote OCR cross-references name the existing skills; replaced "narrow the filters" with the page's fuller advice; added Removal and Assignment details and the Move to Trash restore window.
Method: documentation only; no commands were run.
