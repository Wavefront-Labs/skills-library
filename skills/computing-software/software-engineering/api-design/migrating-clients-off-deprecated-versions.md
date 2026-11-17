---
id: computing-software.software-engineering.api-design.migrating-clients-off-deprecated-versions
name: migrating-clients-off-deprecated-versions
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-client-migration, api-deprecation, sunset-header, deprecation-header, api-versioning]
level: advanced
status: draft
description: "Get real consumers off a deprecated API version: usage telemetry, Deprecation/Sunset headers, outreach, brownouts, and a safe final shutdown."
sources: ["https://www.rfc-editor.org/rfc/rfc8594", "https://www.rfc-editor.org/rfc/rfc9745", "https://github.blog/changelog/2021-08-10-brownout-notice-api-authentication-via-query-parameters-for-48-hours/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrating clients off a deprecated version

## 1. Measure who is still on it
Log per request: API version, endpoint, client id/key, User-Agent/SDK version. Build a dashboard of
**distinct callers per week** on the old version, not request volume; one cron job matters as much as
a busy client.

## 2. Signal in-band
```
Deprecation: @1767225600            (RFC 9745, date it became deprecated)
Sunset: Wed, 30 Jun 2027 00:00:00 GMT   (RFC 8594, removal date)
Link: <https://docs.example.com/migrate/v2>; rel="deprecation"
```
SDKs should log a warning once per process when they see `Deprecation`.

## 3. Make migration cheap
- Migration guide with field-by-field mapping and code diffs per SDK language.
- Compatibility period where both versions run; translation layer from v1 to v2 internally so
  you maintain one implementation.
- Where possible, let clients opt in per request (version header) so they can migrate gradually.

## 4. Outreach on a timeline
T-6 months announce; T-3 email the remaining callers by name; T-1 direct contact for top callers.

## 5. Brownouts before shutdown
Scheduled windows (e.g. 1 hour, then 24 hours) where the old version returns the final error
(410 Gone or 400 with a migration link). Announce them. Brownouts surface the forgotten integrations
owners never read email for. Watch support tickets and the caller list during each.

## 6. Shutdown
Return **410 Gone** with a problem+json body linking the guide, not 404. Keep the error response for
months. Have a rollback flag for a key strategic customer, time-boxed.

## Verify
Caller count on the old version trends to zero before the sunset date; anything left is a named
account with an owner and a plan.
