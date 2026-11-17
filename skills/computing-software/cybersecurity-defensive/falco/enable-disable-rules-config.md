---
id: computing-software.cybersecurity-defensive.falco.enable-disable-rules-config
name: enable-disable-rules-config
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [rules-enable, rules-disable, falco-yaml-rules, tag-selection, wildcard]
level: practitioner
status: docs-checked
description: "Control which rules load with enable and disable entries in falco.yaml or -o options, evaluated in order with wildcard and tag patterns."
sources:
  - https://falco.org/docs/concepts/rules/controlling-rules/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Falco 0.38.0, the `rules` section of `falco.yaml` accepts ordered `enable` and `disable` entries by rule name pattern or tag. They are evaluated in order and override the `enabled` status from rule files and overrides.

```yaml
rules:
  - disable:
      rule: "*"
  - enable:
      rule: Netcat Remote Code Execution in Container
  - enable:
      rule: Delete or rename shell history
```

This disables every rule, then enables the two named ones. Entries take `rule: <wildcard pattern>` or `tag: <tag>`.

The same on the command line with `-o`:
`falco -o "rules[].enable.tag=network" -o "rules[].enable.rule=Directory traversal monitored file" -o "rules[].enable.rule=k8s_*" -o "rules[].disable.rule=k8s_noisy_rule"`
All rules tagged `network` are enabled, plus the named one and anything matching `k8s_*`, then `k8s_noisy_rule` is disabled. If both YAML configuration and `-o` options are given, the CLI options are applied last. With the official Helm chart pass these through `extraArgs`.

Other ways to silence a default rule:
- Override the `user_*` macro the rule ships, with `condition: (always_true)`; the last defined macro of that name wins.
- In a custom file loaded after the defaults, `- rule: User mgmt binaries` with `enabled: false`.

Gotcha: `enabled` as an override is deprecated and will be removed in Falco 1.0.0; use `override.enabled`. Writing `enabled: false` on a rule you define yourself is fine.

## Checked

2026-11-08. Read the cited controlling-rules page in full and corrected details to match it.

Method: documentation only; no commands were run.
