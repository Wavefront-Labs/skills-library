---
id: computing-software.database-administration.influxdb.troubleshoot-write-errors
name: troubleshoot-write-errors
category: computing-software
field: database-administration
product: influxdb
tags: [writes, http-status, rejected-points, troubleshooting, retry-after]
level: practitioner
status: docs-checked
description: "Map InfluxDB v2 write API status codes to causes and diagnose rejected points from the 422 response body."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/troubleshoot/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Writes are synchronous: the response status is the final status and everything ingested is queryable. Wait for a response before sending the next request if write order matters.

Status codes the write API returns:

- 204: all data ingested.
- 400: bad request; the body names the first malformed line and all request data was rejected.
- 401: `Authorization: Token` header missing or malformed, token value missing, or the token lacks write permission on the organization and bucket.
- 404: a requested resource such as the organization or bucket was not found; the body names the resource type and name.
- 413: request entity too large; all data rejected. OSS returns it only if the Go `ioutil.ReadAll()` call raises an error.
- 422: well-formed request but some or all points were rejected for semantic errors (schema conflicts, retention policy violations). Points not rejected are still ingested.
- 500: internal server error, the default error status.
- 503: server temporarily unavailable to accept writes; the `Retry-After` header says when to retry.

The `message` property of the body carries detail; `partial write` means some points were rejected. A 422 body has `code` of `unprocessable entity` and a `message` that can name the retention policy bound that was violated.

Points are rejected for: a line protocol parsing error, an invalid timestamp, a schema conflict (the same series already has a field of a different value type, in the same batch or in the bucket), or a retention policy violation (timestamp outside the bucket retention).

When data is missing: check the status code, read `message`, verify every line is valid line protocol or CSV, verify timestamps match the request precision parameter, and reduce payload size by optimizing writes.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 "Troubleshoot issues writing data" page, read in full as downloaded text.

Removed: the 429 quota code, the `_monitoring` `rejected_points` lookup and its 7-day retention, none of which appear on the current page.
