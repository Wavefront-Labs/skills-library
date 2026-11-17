---
id: computing-software.cybersecurity-defensive.splunk.spl-search-macros
name: spl-search-macros
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, search-macros, macros-conf, detection-engineering, knowledge-objects, escu]
level: practitioner
status: draft
description: "Write, parameterise and govern Splunk search macros (macros.conf, arguments, validation, permissions) and expand them with Ctrl+Shift+E when debugging detections."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Definesearchmacros", "https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Usesearchmacros", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Macrosconf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Search macros

Macros let one change (an index list, a tuning filter) apply to every detection that uses it.

## Define
Settings > Advanced search > Search macros, or `macros.conf`:
```
[edr_indexes]
definition = (index=crowdstrike OR index=defender)

[suspicious_parent(1)]
args = parent
definition = (parent_process_name="$parent$" AND process_name IN ("cmd.exe","powershell.exe"))
validation = isstr(parent)
errormsg = parent must be a string
iseval = 0
```
Use with backticks: `` `edr_indexes` `suspicious_parent("winword.exe")` ``. Macro names with arguments
include the arg count: `suspicious_parent(1)`; overloads by count are separate macros.

## Patterns that matter in security content
- **Index macros** (`` `wineventlog_security` ``): detections never hard-code indexes. ESCU ships these
  empty or default; set them during onboarding.
- **Filter macros** (`` `<detection_name>_filter` ``): ESCU appends one to every search; put tuning
  allowlists there so content updates do not overwrite your tuning.
- **eval macros** (`iseval = 1`): the definition is an eval expression returning the search string.
  Rarely needed; harder to read.

## Debugging
- In the search bar press **Ctrl+Shift+E** (Cmd+Shift+E) to expand all macros and see the real search.
- `| rest /servicesNS/-/-/admin/macros | search title=<name> | table title definition eai:acl.app eai:acl.sharing`
  finds which app's definition wins.
- Macro not found usually means it is private or app-shared in another app: set sharing to Global
  (export = system in `default.meta`) for macros used across apps.

## Gotchas
- Arguments are text substitution: quote values containing spaces, and beware `$` inside definitions.
- Changing a macro changes every saved search using it immediately; review like code.
- A trailing `|` or missing parentheses in an index macro silently changes boolean precedence.

## Verify
Expand the macro and run the expanded search; results must equal the macro version. List
consumers with `| rest /servicesNS/-/-/saved/searches | search search="*`edr_indexes`*" | table title`.
