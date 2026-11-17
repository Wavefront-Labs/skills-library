---
id: computing-software.email-administration.dovecot.events-model-categories-and-fields
name: events-model-categories-and-fields
category: computing-software
field: email-administration
product: dovecot
tags: [events, event-categories, event-fields, event-hierarchy, duration-field, statistics]
level: advanced
status: docs-checked
description: "Understand Dovecot events: hierarchy, inherited categories and fields, forced debug flag, field types and why consistent names matter."
sources:
  - https://doc.dovecot.org/main/core/admin/events.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Events improve both logging and statistics. A logging call can attach to an event carrying more metadata than the message text, which will eventually allow machine-parsable (such as JSON) log lines. Events can also be captured and sent to statistics even if not logged. An event has:
- categories, such as `storage`, `mailbox` or `auth`;
- fields, such as `user=foo@example.com` or `service=imap`;
- a creation timestamp with microsecond precision;
- the source file and line where it was sent;
- optionally a human-readable name (important for statistics events);
- a forced debug flag, which turns on debug logging for that event regardless of global filters and is inherited by children.

Events are hierarchical. Children inherit all categories and fields from their parents, may replace a parent's field and may remove it. Ideally every event traces back to a top event for the user or session so statistics can attribute activity. An event's lifetime should match its object; an IMAP connection event is created at connect and destroyed at disconnect.

The automatic `duration` field runs from event creation to its last send, so reusing one long-lived event for many log lines makes duration meaningless.

Categories are hierarchical too: `mail` is a child of `mailbox`, which is a child of `storage`, so a filter on `category=storage` also matches `mail` and `mailbox`. A category is not a process name, although a `service:<name>` category exists, and the IMAP process has an `imap` category inherited by most of its child events.

There are 4 field types: strings, numbers (`intmax_t`, usually signed 64-bit), timestamps (`struct timeval`) and lists of strings. Fields serve filtering by `field_name=value`, counting in statistics (most commonly number fields), and internal metadata passing between plugins. Consistent names such as `ip`, `net_in_bytes` and `net_out_bytes` let statistics sum unrelated events (for example HTTP and IMAP network traffic).

A `category=imap` filter likely matches most imap process logging but not events whose parent is not the IMAP client event.

## Checked
2026-11-09. Read the whole Dovecot "Events Design" page (doc.dovecot.org/main/core/admin/events.html; the old main/admin/ URL is a script shell with no text, so the source was replaced). Corrected the field types (the page lists four, not including IPs) and added the filtering and category caveat from the page.

Method: documentation only; no commands were run.
