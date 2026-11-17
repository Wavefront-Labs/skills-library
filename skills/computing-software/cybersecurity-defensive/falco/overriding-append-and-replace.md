---
id: computing-software.cybersecurity-defensive.falco.overriding-append-and-replace
name: overriding-append-and-replace
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [override, append, replace, rules-local-yaml, rules-files]
level: practitioner
status: docs-checked
description: "Modify default Falco lists, macros and rules with the override section, knowing which keys each action allows and load order."
sources:
  - https://falco.org/docs/concepts/rules/overriding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Override existing objects from a later rules file, for example `/etc/falco/falco_rules.local.yaml` loaded after `falco_rules.yaml`, or later in the same file. Order is set with repeated `-r` parameters, `rules_files` in `falco.yaml`, or the Helm value `falco.rules_files`. Add an `override` section naming the key and action. `append` and `replace` cannot be used together; trying to apply both is an error. Different keys in one `override` can use different actions, as the `condition: append` plus `output: replace` example shows.

Overridable keys:
- Lists, append or replace: `items`.
- Macros, append or replace: `condition`.
- Rules, append: `condition`, `output`, `desc`, `tags`, `exceptions`.
- Rules, replace: `condition`, `output`, `desc`, `priority`, `tags`, `exceptions`, `enabled`, `warn_evttypes`, `skip-if-unknown-filter`.

```yaml
- list: my_programs
  items: [cp]
  override:
    items: append
- macro: access_file
  condition: or evt.type=openat
  override:
    condition: append
- rule: program_accesses_file
  condition: and not user.name=root
  output: A file (user=%user.name command=%proc.cmdline file=%fd.name) was opened by a monitored program
  override:
    condition: append
    output: replace
```

Appending to a condition simply adds the text to the original condition, so start it with `and` or `or`. In the example, the rule then excludes root and uses the new output. If the original condition mixes `and`/`or` without parentheses, the appended `or` may bind in an unintended way, so scope the original condition with parentheses or avoid appending conditions.

Gotcha: if the local file loads before the default file, the override has nothing to modify. Re-enabling a rule with `enabled: true` as an override is deprecated (warning since Falco 0.37.0); use `override: enabled: replace` instead.

## Checked

2026-11-08. Read the cited overriding page in full and corrected append and replace semantics to match it.

Method: documentation only; no commands were run.
