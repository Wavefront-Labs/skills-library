---
id: computing-software.cybersecurity-defensive.wazuh.sca-custom-policy-syntax
name: sca-custom-policy-syntax
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [sca-policy, yaml, checks, rule-types, regex-type, requirements]
level: advanced
status: docs-checked
description: "Write a custom Wazuh SCA policy YAML: policy, requirements, variables and checks sections, rule types f d p c r, operators, and the spacing traps."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/creating-custom-policies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A policy file has sections `policy` (required), `requirements` (optional), `variables` (optional) and `checks` (required).

- `policy`: `id`, `file`, `name`, `description` required; `references` optional; `regex_type` is `osregex` (default) or `pcre2`.
- `requirements`: `title`, `description`, `condition`, `rules`. If unmet, the scan for that file does not start.
- `variables`: names start with `$`, for example `$sshd_file`.
- `checks`: numeric `id`, `title`, `condition` (`all`, `any`, `none`) and `rules` required. Optional: `description`, `rationale`, `remediation`, `compliance`, `references`, `regex_type`. A check-level `regex_type` overrides the policy's.

`id` values under `policy` and `checks` must be unique across all policy files.

Rule types: `f` file, `d` directory, `p` process, `c` command, `r` Windows registry only.
Operators: literal by default; `r:` regex; `n:` numeric with a capture group and `compare` (`<`, `<=`, `==`, `!=`, `>=`, `>`). Prefix `not` negates a rule, `!` negates a content operator, ` && ` chains.

Traps:
- Spaces around `->`, `compare` and `&&` are mandatory.
- Process rules allow existence checks only; command rules allow content checks only.
- Content checks apply per line, and negated content operators pass on any non-matching line.
- A missing target yields Not applicable.

## Checked

2026-11-08. Read the whole Creating custom SCA policies page. Confirmed: section required flags, policy, requirements and checks field tables, regex_type values and override, variable syntax, unique ids, condition values, rule types, operators, compare operators, not and ! negation, && chaining, spacing rules, per-line content scope, process and command restrictions, Not applicable for a missing target. Nothing removed.
Method: documentation only; no commands were run.
