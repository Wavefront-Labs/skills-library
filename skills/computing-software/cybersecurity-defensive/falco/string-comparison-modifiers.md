---
id: computing-software.cybersecurity-defensive.falco.string-comparison-modifiers
name: string-comparison-modifiers
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [anyof, allof, oneof, string-modifiers, falco-0-44]
level: advanced
status: docs-checked
description: "Compare one Falco field against several values with anyof, allof and oneof, and avoid the not-equal trap with allof."
sources:
  - https://falco.org/docs/concepts/rules/conditions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Falco 0.44, a string comparison operator can be followed by `anyof`, `allof` or `oneof`:

```
proc.cmdline contains anyof (curl, wget)
proc.cmdline contains allof (curl, --upload-file)
proc.cmdline contains oneof (curl, wget)
```

Meaning: `anyof` is true when at least one right-hand value matches, `allof` when every one matches, `oneof` when exactly one matches. A command line containing both `curl` and `wget` matches the `anyof` example but not the `oneof` example. Repeated list entries count separately for `oneof`.

Syntax rules: put a space before and after the modifier and the values in parentheses. A Falco list can sit inside the parentheses, for example `fd.name contains anyof (suspicious_paths)`. They work with `=`, `==`, `!=`, `contains`, `icontains`, `bcontains`, `startswith`, `bstartswith`, `endswith`, `glob`, `iglob` and `regex`, subject to the field's supported operators. They do not apply to `in`, `intersects`, `pmatch`, `exists` or numeric ordering operators such as `>`.

They compare a single field value with the list. For list-valued fields keep using `in` or `intersects`. An empty right-hand list makes all three modifiers false.

Not-equal trap: with `!=` each individual comparison tests inequality. To exclude both `bash` and `sh` write `proc.name != allof (bash, sh)`. Writing `!= anyof (bash, sh)` also matches `bash`, since it differs from `sh`.

Only use these modifiers on Falco 0.44 or later.

## Checked

2026-11-08. Read the cited conditions page in full. Added the regex full-match note and removed claims the page does not make.

Method: documentation only; no commands were run.
