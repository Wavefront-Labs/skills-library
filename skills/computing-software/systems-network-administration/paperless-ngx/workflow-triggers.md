---
id: computing-software.systems-network-administration.paperless-ngx.workflow-triggers
name: workflow-triggers
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, workflows, workflow-triggers, consumption-started, scheduled-trigger, document-added]
level: practitioner
status: docs-checked
description: "Choose between the four workflow trigger types and apply source, filename, path, tag, correspondent and custom field filters."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow triggers

Workflows have multiple triggers (events with optional filtering rules) and sequential actions. Workflows and their actions apply in sort order. For assignment actions, later assignments override earlier ones, except assignments that accept multiple items (tags, custom fields, permissions), which are merged.

## Trigger types
1. Consumption Started: before a document is consumed. Filters: source (mail, consumption folder or API), file path, file name, mail rule.
2. Document Added: after a document is added. File path and source are no longer available, but content has been extracted and metadata such as document type and tags have been set, so these can be used for filtering.
3. Document Updated: when a document is updated. Like Added, it can filter by content matching, tags, document type, correspondent or storage path.
4. Scheduled: runs workflows at a specific time. The date used is the document's added, created or updated date, or a date custom field, with a day offset (positive after the date, negative before). The scheduled check runs hourly at 5 minutes past the hour by default; `PAPERLESS_WORKFLOW_SCHEDULED_TASK_CRON` configures it (default `5 */1 * * *`, and `disable` stops scheduled workflows).

## Filters
- Source: consume folder, API (and the web UI), or mail fetch.
- File name, including wildcards such as `*.pdf`.
- File path, including wildcards. With `PAPERLESS_CONSUMER_RECURSIVE` enabled you can, for example, assign documents to different owners based on the upload directory.
- Mail rule. Choosing it forces mail fetch to be the workflow source.
- Content matching (Added, Updated and Scheduled triggers only).
- Advanced filters for Added, Updated and Scheduled: any tags, all tags, no tags, document type, not document types, correspondent, not correspondents, storage path, not storage paths, and a custom field query (the same as used for the document list filters).

## Permissions
Workflows intentionally have no owner or permissions: all users with application permission to edit workflows see the same set. Because workflows can change the permissions of existing documents, you may want to restrict access to them. On migration, existing installs grant workflow access to users who can add documents (superusers can always access everything).

## Checked
Date: 2026-11-07
Pages read in full: none in full. I read the whole Workflows section of usage (introduction, triggers, filters, actions, placeholders, permissions) and the PAPERLESS_WORKFLOW_SCHEDULED_TASK_CRON entry in configuration.
Corrections: removed "Tags and content are not available yet" for Consumption Started (not stated); reworded the permission advice to the page's "may want to restrict"; attributed the hourly :05 schedule to the page and added the configuration default and `disable`; added the migration permission note.
Method: documentation only; no commands were run.
