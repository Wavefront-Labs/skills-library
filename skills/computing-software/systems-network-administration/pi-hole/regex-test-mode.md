---
id: computing-software.systems-network-administration.pi-hole.regex-test-mode
name: regex-test-mode
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [regex-test, pihole-ftl-regex-test, regex-debug-script]
level: practitioner
status: docs-checked
description: "Test domains against regexes with pihole-FTL regex-test, including exit codes useful in scripts."
sources: ["https://docs.pi-hole.net/regex/testmode/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Regex test mode

`pihole-FTL regex-test` checks a domain against regexes without waiting for live traffic.

```bash
pihole-FTL regex-test doubleclick.net
```

tests the domain against all regexes in the gravity database.

```bash
pihole-FTL regex-test doubleclick.net "(^|\.)double"
```

tests it against the regex you pass on the command line. You do not need `sudo`; any user can run it.

**Exit codes** for scripting:

| Code | Meaning |
| --- | --- |
| 0 | Match |
| 1 | Error |
| 2 | No match |

Output shows the compile time and check time, and finishes with `MATCH` or `NO MATCH`, for example:

```text
Step 1: Compiling regex filter...
Step 2: Checking domain...
MATCH
```

Comments and back-references work in test mode too.

**Pair with debug logging.** Test mode checks a pattern; `pihole-FTL --config debug.regex true` logs real matches to `/var/log/pihole/FTL.log`, including the `domainlist` row ID.

**Checklist**

1. Save the regex to the domain list.
2. Run `pihole reloadlists`; the Regex Blocking page prefers it to SIGHUP or a restart because the DNS cache stays intact.

## Checked

2026-11-03. Read the Regex Test mode page (both commands, no sudo needed, exit codes 0 match, 1 error, 2 no match), the Regex Blocking page (`pihole-FTL --config debug.regex true`, FTL.log, DB ID matching the `domainlist` row, `pihole reloadlists`) and the Pi-hole regex extensions page (test output format, comments, back-references). Removed the checklist advice that the pages do not state.

Method: documentation only; no commands were run.
