---
id: computing-software.cybersecurity-defensive.falco.custom-ruleset-placement
name: custom-ruleset-placement
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [custom-rules, rules-d, rules-files, customrules, helm-values]
level: practitioner
status: docs-checked
description: "Place custom Falco rules in /etc/falco/rules.d or Helm customRules, with the required rule keys and the error Falco raises for missing ones."
sources:
  - https://falco.org/docs/concepts/rules/custom-ruleset/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Falco loads the default rules first, then custom rules in `/etc/falco/rules.d`, as set by `rules_files` in `/etc/falco/falco.yaml`:

```yaml
rules_files:
  - /etc/falco/falco_rules.yaml
  - /etc/falco/falco_rules.local.yaml
  - /etc/falco/rules.d
```

Syscall rules are grouped per `evt.type` for faster matching and then processed in order, so by default two rules do not fire together on the same `evt.type` event. Put specific rules before general ones, or the general rule captures events meant for the specific one. The `rules_files` list can be adjusted to reorder, include other files or add directories. The default file holds reusable lists and macros, so think before delaying or disabling it.

With Helm, replace `customRules: {}` in `values.yaml`:

```yaml
customRules:
  custom-rules.yaml: |-
    - rule: Example rule
      desc: ...
```

Each key becomes a file under `/etc/falco/rules.d` in the Falco pods.

Every rule needs `rule`, `desc`, `condition`, `output` and `priority`; `tags` is optional but recommended. A rule name that already exists overwrites the earlier one. A missing key fails loading, for example:
`LOAD_ERR_YAML_VALIDATE (Error validating internal structure of YAML file): Item has no mapping for key 'desc'`

Keeping the upstream ruleset is not mandatory; you may reorganise or rewrite it. An existing rule can be changed in `rules.d` by rewriting it or using `append`.

## Checked

2026-11-08. Read the Custom Ruleset page in full. Removed an unsupported falco -V claim; added placement ordering, rules_files adjustment and append notes.

Method: documentation only; no commands were run.
