---
id: computing-software.cybersecurity-defensive.splunk.spl-eval-functions
name: spl-eval-functions
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, eval-functions, eval, case-function, coalesce, strptime, relative-time, investigation]
level: practitioner
status: draft
description: "Use SPL eval for security analysis: case/if logic, coalesce for messy fields, time math with strptime and relative_time, string and IP functions, null handling."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Eval", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/CommonEvalFunctions", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/DateandTimeFunctions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# eval functions for investigations

## Conditional logic
```
| eval risk=case(
    match(process,"(?i)-enc(odedcommand)?\s"), 80,
    like(process,"%DownloadString%"), 70,
    true(), 0)
| eval is_admin=if(isnotnull(mvfind(groups,"(?i)domain admins")), 1, 0)
```
- `case()` returns NULL when nothing matches, so always end with `true(), <default>`.
- `match()` is regex, `like()` uses `%` and `_` wildcards; `searchmatch("x=y")` reuses search syntax.

## Messy field names across sources
```
| eval user=coalesce(user, src_user, TargetUserName, Account_Name)
| eval user=lower(mvindex(split(user,"\\"),-1))      ``` strip DOMAIN\ ```
```

## Time math
```
| eval created=strptime(pwdLastSet,"%Y-%m-%dT%H:%M:%S")
| eval age_days=round((now()-created)/86400,1)
| where _time > relative_time(now(),"-24h@h")
| eval hour=strftime(_time,"%H"), off_hours=if(hour<7 OR hour>19,1,0)
```
- `strptime` returns epoch seconds; NULL if the format does not match exactly (check timezone `%z`).
- `relative_time(now(),"-7d@d")` snaps to midnight seven days ago.

## Strings, numbers, network
- `len()`, `substr(x,1,10)`, `replace(x,"regex","new")`, `upper/lower`, `trim`.
- `urldecode(url)`, `tostring(bytes,"commas")`, `tonumber(hex,16)`.
- `cidrmatch("10.0.0.0/8", src)` returns true/false; use inside `if()` to tag internal traffic.
- Shannon entropy is not built in; use the URL Toolbox app (`ut_shannon`) for DGA-style checks.

## Multiple assignments
`| eval a=1, b=a*2` evaluates left to right in one command, so later expressions can use earlier ones.

## Null handling
- Arithmetic with NULL yields NULL: `| eval total=coalesce(in,0)+coalesce(out,0)`.
- `isnull()` / `isnotnull()`; `fillnull value=0 field1 field2` before stats.
- Comparisons against NULL are false in both directions, so `where x!="a"` drops events with no x.

## Gotchas
- Field names with dots or dashes need single quotes in eval: `'Processes.process_name'`.
- Double quotes are string literals; single quotes are field references.
- `eval` on every event before filtering is slow; put `where`/search terms first.

## Verify
`| table` the inputs next to the computed field on 20 events, including ones where inputs are
missing, before using the field in a detection.
