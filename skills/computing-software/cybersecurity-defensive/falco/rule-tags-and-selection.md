---
id: computing-software.cybersecurity-defensive.falco.rule-tags-and-selection
name: rule-tags-and-selection
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [rule-tags, tag-filter, cis, filesystem, falco-t-option]
level: intro
status: docs-checked
description: "Tag Falco rules and run only or skip tagged subsets with -t and -T, using the default ruleset tag meanings and the -A flag."
sources:
  - https://falco.org/docs/concepts/rules/controlling-rules/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Give a rule a `tags` list, for example `tags: [container, cis]`. Without the key, or with an empty list, the rule has no tags.

Command-line selection:
- `falco -T filesystem -T cis ...` disables rules with those tags. `-T` can be repeated and cannot be combined with `-t`.
- `falco -t filesystem -t cis ...` runs only rules with those tags. `-t` can be repeated and cannot be combined with `-T` or `-D <pattern>` (disable rules by rule name regex).

Tags used in the default ruleset (every default rule has at least one):
- `filesystem`: reading or writing files
- `software_mgmt`: package tools such as rpm and dpkg
- `process`: starting or changing a process
- `database`: databases
- `host`: the rule only works outside containers
- `shell`: starting shells
- `container`: the rule only works inside containers
- `cis`: CIS Docker benchmark
- `users`: user management or identity changes
- `network`: network activity

For performance, some syscalls are discarded before Falco processes them. List them with `falco -i`. To run against all events, including those, use the `-A` flag.

The `rules` section of `falco.yaml` can also select by tag with `enable: tag:` and `disable: tag:`, evaluated in order.

## Checked

2026-11-08. Read the cited controlling-rules page in full and corrected details to match it.

Method: documentation only; no commands were run.
