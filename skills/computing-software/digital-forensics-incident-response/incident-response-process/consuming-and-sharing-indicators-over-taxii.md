---
id: computing-software.digital-forensics-incident-response.incident-response-process.consuming-and-sharing-indicators-over-taxii
name: consuming-and-sharing-indicators-over-taxii
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [taxii-feeds, stix, threat-intelligence, misp, dfir]
level: advanced
status: docs-checked
description: "Consume and publish STIX 2.1 indicators over TAXII 2.1: discovery, collections, polling with added_after, filtering, and pushing incident IOCs to partners."
sources: ["https://docs.oasis-open.org/cti/taxii/v2.1/os/taxii-v2.1-os.html", "https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html", "https://github.com/oasis-open/cti-taxii-client"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consuming and sharing indicators over TAXII

**Goal:** pull machine-readable intel into the incident (and push your findings to an ISAC or
partner) using the TAXII 2.1 API rather than emailed spreadsheets.

## TAXII 2.1 model
- **Discovery** is `GET /taxii2/` on the server; it lists API roots (logical groupings of
  collections). **Collections:** `GET {api-root}/collections/`.
- Objects: `GET {api-root}/collections/{id}/objects/` with filters `added_after` (a timestamp),
  `limit`, `next` and `match[type]`, e.g. `match[type]=indicator`.
- Paging: the response envelope carries `more` and `next`; pass the server-provided `next` value
  back (it is opaque to clients).
- Headers: `Accept: application/taxii+json;version=2.1`; a POST also needs
  `Content-Type: application/taxii+json;version=2.1`.
- Write: `POST {api-root}/collections/{id}/objects/` with STIX objects inside a TAXII envelope
  (`{"objects": [...]}`), only if the collection's `can_write` is true. The server answers 202 with
  a status resource (`id`, `status`, `total_count`, `success_count`, `failure_count`,
  `pending_count`); poll it until complete. Re-publishing an identical object is not an error.

## Python client (oasis-open/cti-taxii-client)
```python
from taxii2client.v21 import Server, as_pages
server = Server("https://taxii.example.org/taxii2/", user="u", password="p")
collection = server.api_roots[0].collections[0]
for envelope in as_pages(collection.get_objects, per_request=500):
    for obj in envelope.get("objects", []):
        print(obj["id"], obj.get("pattern"), obj.get("valid_until"))
```
The client README says extra arguments to `get_objects` carry filter information as keyword
arguments; check its documentation for the `added_after` and type filter names before use.
To poll incrementally, store the `X-TAXII-Date-Added-Last` response header (the `date_added` of the
last object returned) and use it as the next `added_after`.

## Using the indicators
- An Indicator has a required `pattern`, `pattern_type` and `valid_from`, and an optional
  `valid_until` that must be later than `valid_from`; if omitted, the indicator has no expiry.
  `confidence` is a number from 0 to 100. A STIX pattern looks like
  `[file:hashes.'SHA-256' = '<hash>']`. Convert patterns to SIEM queries or EDR IOC lists and
  respect `valid_until` and `confidence`.

## Publishing incident IOCs
- Build `indicator` objects and link them to a `malware` object with a relationship of type
  `indicates`; apply data markings through `object_marking_refs` (marking-definition objects).
- Strip victim-identifying data (internal hostnames, employee emails) before sharing.

## Gotchas
- TAXII 2.0 and 2.1 differ: the discovery URL changed from `/taxii/` to `/taxii2/`, and item-based
  pagination was removed in 2.1. Check the server version.
- Ingesting unvetted feeds creates alert floods; set confidence thresholds and expiry.

## Verify
Indicators arrive incrementally, map to working detections, and shared objects were accepted
(status resource shows success).

## Checked
Date: 2026-11-08. Confirmed from the TAXII 2.1 spec (read in two parts; the final 49,000 characters of
the page and the sections on filtering formats were not read): discovery and collections paths,
filters, `more` and `next`, media type, Add Objects envelope, 202 status resource, `can_write`,
`X-TAXII-Date-Added-Last`, 2.0 differences. From the STIX 2.1 spec (about 200,000 of 240,000
characters read): indicator properties, confidence range, file-hash pattern example, `indicates`.
From the client README: Server, api_roots, collections, as_pages, per_request, keyword filters.
Removed as unconfirmed: the domain-name pattern example, specific TLP marking-definition ids,
`intrusion-set` link, MISP import and the STIX validator note.
Method: documentation only; no commands were run.
