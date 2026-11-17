---
id: computing-software.cybersecurity-defensive.splunk.spl-rex-field-extraction
name: spl-rex-field-extraction
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, rex-command, regex, field-extraction, inline-extraction, sed-mode, investigation]
level: practitioner
status: draft
description: "Extract fields inline in SPL with rex during investigations: named groups, max_match, sed-mode masking, and promoting good regexes to props.conf."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Rex", "https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/AboutSplunkregularexpressions", "https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Createandmaintainsearch-timefieldextractionsthroughconfigurationfiles"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# rex and inline field extraction

**Goal:** pull a field out of raw events on the spot during an investigation, then make it
permanent if it is useful.

## Basics
```
index=web | rex field=_raw "user=(?<user>[^\s&]+)"
index=mail | rex field=subject "(?i)invoice\s+#?(?<inv>\d{5,})"
```
- Named capture groups `(?<name>...)` become fields. PCRE syntax.
- `field=` defaults to `_raw`; extracting from an existing field is faster and safer.
- `max_match=0` returns all matches as a multivalue field:
  `| rex max_match=0 "(?<ip>\d{1,3}(?:\.\d{1,3}){3})" | mvexpand ip`.

## Investigation patterns
URLs from a mail body:
```
| rex field=body max_match=0 "(?<url>https?://[^\s\"'<>]+)"
```
Command-line arguments:
```
index=edr process_name=powershell.exe
| rex field=process "(?i)-e(nc(odedcommand)?)?\s+(?<b64>[A-Za-z0-9+/=]{20,})"
| eval decoded=base64decode(b64)   ```(needs an app providing base64decode, or decode offline)```
```
Key=value pairs without writing a regex: `| extract pairdelim=";" kvdelim="="`.
JSON inside a field: `| spath input=message`.

## sed mode (masking and normalisation)
```
| rex field=card mode=sed "s/\d{12}(\d{4})/XXXXXXXXXXXX\1/g"
```
Same syntax in props.conf `SEDCMD-mask = s/.../.../g` masks at index time (data is changed
permanently before it is written).

## Promote to props.conf
When a rex is used in more than one saved search, define it once:
```
[myapp:log]
EXTRACT-user = user=(?<user>[^\s&]+)
```
Search-time, no reindex needed, and every analyst gets the same field name (pick CIM names).

## Gotchas
- Greedy `.*` across a long event is slow and grabs too much; use negated classes
  `[^"]+` or lazy `.*?`.
- Escape quotes inside the SPL string with `\"`; test the regex on regex101 in PCRE mode.
- rex on `_raw` runs on every event returned: filter first (`index=web "user="`).
- Extractions that produce nothing do not error; check `| stats count(user)`.

## Verify
`| stats count count(user) as extracted` shows the extraction rate; investigate events
where it failed with `| where isnull(user) | head 20`.
