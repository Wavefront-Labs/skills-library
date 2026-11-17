---
id: computing-software.systems-network-administration.paperless-ngx.remote-ocr-azure
name: remote-ocr-azure
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, remote-ocr, azure, document-intelligence, paperless-remote-ocr-mode, workflow-only]
level: advanced
status: docs-checked
description: "Send documents to Azure Document Intelligence for OCR, either always or selectively through a Remote OCR workflow action."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote OCR with Azure AI

This feature is disabled by default and will always remain strictly opt-in. At the moment it is limited to Microsoft's Azure Document Intelligence service, a paid service (with a free tier) that requires an Azure account and subscription. Consider costs and any file size or page limitations, for example with a free tier.

## Settings
```bash
PAPERLESS_REMOTE_OCR_ENGINE=azureai
PAPERLESS_REMOTE_OCR_API_KEY=<API_KEY>
PAPERLESS_REMOTE_OCR_ENDPOINT=<ENDPOINT_URL>
```
The engine defaults to None, which disables remote OCR. The endpoint is required for Azure AI. The settings can be supplied as environment variables or via Application Configuration.

## Which documents go remote
`PAPERLESS_REMOTE_OCR_MODE` (default `always`):
- `always`: every document of a supported file type is sent to the remote engine, bypassing the local OCR engine.
- `workflow_only`: documents are processed locally unless a workflow explicitly enables remote OCR for them. This mode also allows the Reprocess actions to use remote OCR selectively for individual documents.

## Remote OCR workflow action
Add it to a workflow that matches only the documents you want sent. The action takes no options; its presence enables remote OCR for a matching document. It only works with a Consumption Started trigger. If the engine is not configured or does not support the file type, the document is processed locally and a warning is written to the log.

## Archive interaction
With the remote parser, `PAPERLESS_ARCHIVE_FILE_GENERATION` is honoured as for the local engine: when no archive is requested (`never`, or `auto` with a born-digital PDF), the remote engine is skipped entirely and locally extracted text is used.

## Network safety
`PAPERLESS_REMOTE_OCR_ALLOW_INTERNAL_ENDPOINTS` defaults to true. If set to false, Paperless blocks remote OCR endpoint URLs that resolve to non-public addresses (for example localhost).

Documents are sent to Azure for OCR processing when this is enabled.

## Checked
Date: 2026-11-07
Pages read in full: none in full. I read the Remote OCR section of usage (including the Remote OCR workflow action), the Remote OCR settings in configuration, and the Remote OCR parser note in migration-v3.
Corrections: added the missing default (true) for ALLOW_INTERNAL_ENDPOINTS, which the draft implied was false; replaced "check cost, file size and page limits" and the privacy advice with the page's wording; added the engine default and the Reprocess behaviour; added migration-v3 as a source for the archive interaction.
Method: documentation only; no commands were run.
