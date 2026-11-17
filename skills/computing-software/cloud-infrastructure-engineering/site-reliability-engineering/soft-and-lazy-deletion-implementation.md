---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.soft-and-lazy-deletion-implementation
name: soft-and-lazy-deletion-implementation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [soft-deletion-implementation, lazy-deletion-pipeline, data-integrity, soft-delete, object-versioning]
level: practitioner
status: docs-checked
description: "The SRE Book's first layer of data defence: trash, soft deletion with a delay before destruction, and lazy deletion, plus how S3 Versioning delete markers relate."
sources: ["https://sre.google/sre-book/data-integrity/", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Soft and lazy deletion

Source: SRE Book "Data Integrity", "First Layer: Soft Deletion".

## Definitions
- **Trash**: lets users undelete; reduces but cannot eliminate the support burden of accidental deletion, especially when third-party add-ons can also delete data.
- **Soft deletion**: deleted data is immediately marked as such and unusable by all but the application's administrative code paths (legal discovery, hijacked account recovery, enterprise administration, user support, troubleshooting). Do it when a user empties their trash, and give authorised administrators a tool to undelete items.
- **Lazy deletion**: behind-the-scenes purging controlled by the storage system, whereas soft deletion is controlled by and expressed to the client application. Data deleted by a cloud application becomes inaccessible to the application but is kept by the provider for up to a few weeks before destruction.

## Design points from the book
- Soft-deleted data is destroyed after a reasonable delay, set by organisational policy and applicable law, storage resources and cost, and product pricing. Common choices are 15, 30, 45 or 60 days. The book reports that most account hijacking and data integrity issues are reported or detected within 60 days, so soft deleting for longer may not be justified. Gmail's trash lets users access messages deleted fewer than 30 days ago.
- The most devastating acute deletions come from developers unfamiliar with the code writing deletion code, especially batch pipelines. Design interfaces to hinder circumventing soft deletion, for example cloud offerings with built-in soft deletion and undeletion APIs, and make sure the feature is enabled.
- Lazy deletion is not advisable everywhere: a long period is costly with much short-lived data and impractical where destruction must be guaranteed within a reasonable time, such as systems offering privacy guarantees.
- Summary: trash is the primary defence against user error; soft deletion is the primary defence against developer error and secondary against user error; in developer offerings lazy deletion is the primary defence against internal developer error and secondary against external developer error.
- Revision history is a form of trash when users have it. At Google it helped with some corruption but not most accidental-deletion cases, since some implementations remove previous states on deletion; apply lazy and/or soft deletion principles to revision history too.

## Amazon S3 Versioning
Per the S3 User Guide: buckets are unversioned by default and versioning must be enabled. In a versioning-enabled bucket a delete inserts a delete marker that becomes the current version instead of removing the object permanently; an overwrite creates a new version and the previous version can be restored. A bucket that was versioned can never return to unversioned, only be suspended. Each version is stored as an entire object and normal rates apply to every version. If an unversioned bucket relied on an expiration lifecycle rule for permanent deletes, add a noncurrent expiration configuration to keep that behaviour. This is the S3 equivalent of keeping deleted data for a while, but the user guide does not describe it as the book's lazy deletion.

## Checked
- 2026-11-08: SRE Book points confirmed on the Data Integrity page; S3 points confirmed on the Versioning page.
- Removed: the SQL schema, view, undelete and purge job examples, the metric, rate-limit and pause-switch advice, the `NoncurrentVersionExpiration: 60 days` value, the GDPR 30-day and crypto-shredding advice, and the unique-constraint and cascade gotchas, none of which the cited pages state.
Method: docs-only read of cited pages, 2026-11-08
