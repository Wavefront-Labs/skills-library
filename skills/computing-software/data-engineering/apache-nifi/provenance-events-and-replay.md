---
id: computing-software.data-engineering.apache-nifi.provenance-events-and-replay
name: provenance-events-and-replay
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, data-provenance, replay, lineage, event-types]
level: practitioner
status: docs-checked
description: "Using NiFi data provenance: the 17 event types, search with wildcards, event details tabs, replay last event, lineage graph, and required policies."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data provenance

Event types: ADDINFO, ATTRIBUTES_MODIFIED, CLONE, CONTENT_MODIFIED, CREATE, DOWNLOAD, DROP, EXPIRE, FETCH, FORK, JOIN, RECEIVE, REMOTE_INVOCATION, REPLAY, ROUTE, SEND, UNKNOWN.

- Search: Search button upper right; `*` is a wildcard; "Exclude from search results" inverts a term.
- View Details has Details, Attributes ("Only show modified") and Content tabs; Content offers Download and Submit (Submit replays from that point).
- Replay: right-click a processor > "Replay last event", from Primary Node only or all nodes.
- Lineage: Show Lineage icon; selected event is red; right-click for "Find parents" and "Expand"; the slider shows earlier states.
- Policies: global "query provenance", component "view provenance" and "view the data" for attributes and content.

Verify: a query returns events and Submit sends the FlowFile to the connection feeding the component that produced the event.

## Checked

Confirmed against the NiFi user guide (Data Provenance: event types table, Searching for Events, Details of an Event, Replaying a FlowFile, Viewing FlowFile Lineage, Find Parents, Expanding an Event).

Method: docs-only read of cited pages, 2026-11-08
