---
id: computing-software.cybersecurity-defensive.wazuh.sibling-decoders
name: sibling-decoders
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [sibling-decoders, parent-child, decoder-order, grandchildren]
level: advanced
status: docs-checked
description: "Use Wazuh sibling decoders: several small regexes each extract one field, coping with reordered, extra or missing fields."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/decoders/sibling-decoders.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sibling decoders are several decoders at the same level with no parent-child relationship between them. They operate in parallel and each extracts one piece of information.

Traditional decoding:
- Decoders without a parent are checked in sequence.
- Once one matches, the search stops there and only its children (if any) are checked.
- Overly generic matching conditions cause false positives, so keep them specific.
- Decoders have no grandchildren: a child cannot act as a parent.

Sibling approach:
- Siblings are decoders that are "parents" of each other, built on the simple parent-child matching logic.
- When one matches, the other siblings are checked too, each extracting one piece of information.
- Reordered, extra or missing fields no longer block extraction; the engine extracts as much as it can.
- Splitting one long regex into smaller ones improves readability.

Pattern from the docs (securityapp example): one base decoder that matches only the `program_name`, then several decoders with the same `name`, the same `<parent>`, and one small `<regex>` plus `<order>` each (for example `srcuser="(\.+)"` with order `srcuser`).

Gotchas:
- Each extracting sibling carries its own `<regex>` and `<order>`; the base decoder only anchors the match.
- A single long regex fails entirely when a field is missing or reordered; the sibling set still decodes the rest.
- Verify the combined extraction by running `/var/ossec/bin/wazuh-logtest` on messages with different field orders.

## Checked

2026-11-08: confirmed against the Wazuh docs page Sibling Decoders (read in full): parallel siblings, traditional matching stops at the first match, no grandchildren, parents-of-each-other logic, readability benefit, the securityapp example and the wazuh-logtest path. Removed the unsupported claim about OS_Regex and alternatives inside groups, and the unsupported "parent must match first" wording.
Method: documentation only; no commands were run.
