---
id: computing-software.software-engineering.api-design.field-naming-and-timestamps
name: field-naming-and-timestamps
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, field-naming, rfc-3339, aip-140, aip-142, timestamps, json-conventions]
level: practitioner
status: docs-checked
description: "Name and type API fields consistently, following Google AIP-140 (field names) and AIP-142 (time and duration): casing, plurals, booleans, _time and _date suffixes, unit suffixes."
sources: ["https://google.aip.dev/140", "https://google.aip.dev/142", "https://www.rfc-editor.org/rfc/rfc3339"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Field naming, types and timestamps

## Naming (AIP-140)
- Protobuf field names are `lower_snake_case`; AIP-140 says they map to the appropriate convention in JSON
  and generated code. No word may begin with a number; no leading, trailing or adjacent underscores.
- Correct American English; the same name for the same concept across APIs.
- Repeated fields are plural (`books`), non-repeated singular (`book`).
- No prepositions (`error_reason`, not `reason_for_error`); the exception is "per" in units.
- Well-known abbreviations are used: `config`, `id`, `info`, `spec`, `stats`; unit abbreviations too
  (`distance_km`, `width_px`).
- Adjective before noun: `collected_items`, not `items_collected`.
- Fields are nouns, never verbs (`disabled`, not `disable`).
- Booleans omit the `is` prefix (`disabled`, `required`), except where the bare word is a reserved word (`is_new`).
- URIs: `uri` for arbitrary URIs, `url` for fields that can only be a URL (`image_url`).
- Avoid names that clash with language keywords (`new`, `class`, `import`) and do not name a field after its
  enclosing message.
- Human-readable label: `display_name` (no uniqueness requirement); `title` for an official formal name.
- Use `bytes` for binary content (base64 on the wire in JSON) rather than asking users to base64 a string.

## Time and duration (AIP-142)
| Concept | Field name | Type |
|---|---|---|
| Absolute instant | ends in `_time` (`create_time`, `update_time`; `_times` if repeated) | `google.protobuf.Timestamp` |
| Span between instants | e.g. `flight_duration` | `google.protobuf.Duration` |
| Offset within a stream | ends in `_offset`, comment says what it is relative to | `google.protobuf.Duration` |
| Civil date | ends in `_date` | `google.type.Date` |
| Wall-clock time | ends in `_time` | `google.type.TimeOfDay` |
| Civil date and time, optional zone | ends in `_time` | `google.type.DateTime` |
- Name activity timestamps with the imperative form (`publish_time`), not past tense (`published_time`,
  `created_time`, `last_updated_time`).
- `Date` and `TimeOfDay` are timezone-naive; use `DateTime` when a zone is needed.
- When a legacy spec forces other types: integers carry meaning plus unit as the final suffix (`seconds`, `millis`,
  `micros`, `nanos`, e.g. `send_time_millis`); strings carry the meaning but no unit suffix. Document the format
  and the reason.
- If you emit text timestamps, RFC 3339 is the Internet profile of ISO 8601 date-time with an explicit offset
  or `Z`.

## Checked
Date: 2026-11-01. Confirmed against AIP-140 and AIP-142 (google.aip.dev): casing, plural, preposition,
abbreviation, adjective, verb, boolean, URI, display name rules; `_time`, `_date`, `_offset` suffixes, imperative
naming, compatibility suffix rules. Removed: framework and linter claims (Spectral, api-linter), vendor styles,
money and int64-id guidance, enum and field-behaviour notes, which the cited pages do not state.
Method: documentation only; no commands were run.
