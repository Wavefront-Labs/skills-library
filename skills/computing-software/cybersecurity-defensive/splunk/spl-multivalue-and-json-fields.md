---
id: computing-software.cybersecurity-defensive.splunk.spl-multivalue-and-json-fields
name: spl-multivalue-and-json-fields
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, multivalue-fields, spath, mvexpand, mvzip, json-parsing, cloud-logs, investigation]
level: practitioner
status: draft
description: "Handle JSON cloud logs and multivalue fields in SPL: spath paths and arrays, mvexpand memory limits, mvzip to keep pairs aligned, mvfilter and mvcount."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Spath", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Mvexpand", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/MultivalueEvalFunctions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multivalue fields and JSON

Cloud audit logs (CloudTrail, Entra, Okta, GCP) are nested JSON with arrays. Getting them flat
and correctly paired is most of the work.

## spath
```
index=aws sourcetype=aws:cloudtrail
| spath path=requestParameters.policyDocument output=policy
| spath input=policy path=Statement{}.Action output=actions
```
- `{}` addresses array elements; `Statement{0}.Effect` is the first element.
- `KV_MODE=json` (or `INDEXED_EXTRACTIONS=json`) in props.conf already extracts top-level paths,
  so you often only need spath for embedded JSON strings.
- Embedded JSON inside a string field needs `spath input=<field>`.
- Truncated events (default `TRUNCATE=10000`) break spath silently; raise TRUNCATE for that sourcetype.

## Keep parallel arrays aligned
Entra `ModifiedProperties` holds names and values in separate arrays:
```
| spath path=modifiedProperties{}.displayName output=prop
| spath path=modifiedProperties{}.newValue output=newval
| eval pair=mvzip(prop,newval,"=")
| mvexpand pair
| rex field=pair "(?<prop>[^=]+)=(?<newval>.*)"
```
Expanding each field separately creates a cross product and wrong pairings.

## Multivalue eval
- `mvcount(f)`, `mvindex(f,0)`, `mvindex(f,-1)`, `mvjoin(f,";")`, `mvdedup(f)`, `mvsort(f)`.
- `mvfilter(match(actions,"^iam:"))` keeps matching values only (one field per call).
- `mvfind(f,"regex")` returns the index or NULL; useful in `if()`.
- `mvappend(a,b)` merges fields (NULL-safe).
- `makemv delim="," field` splits a delimited string; `nomv` collapses.

## mvexpand limits
`mvexpand` is bounded by `max_mem_usage_mb` in limits.conf and silently truncates results
when it hits the limit (a warning appears in the job). Reduce fields with `fields` first:
```
| fields _time user actions | mvexpand actions
```

## stats with multivalue
`stats count by actions` counts each value separately (implicit expand). `values()` returns a
sorted deduplicated multivalue; `list()` keeps order and duplicates (capped at 100 values).

## Verify
After mvexpand, check `| stats dc(_cd)` versus the event count before expansion and confirm a
few pairs against the raw JSON in the event viewer.
