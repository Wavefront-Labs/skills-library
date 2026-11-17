---
id: computing-software.cloud-infrastructure-engineering.docker.tuning-falco-false-positives-with-exceptions
name: tuning-falco-false-positives-with-exceptions
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, falco, falco-tuning, falco-exceptions, falco-macros, runtime-security, alert-fatigue]
level: advanced
status: docs-checked
description: "Cut Falco noise without blinding it: rule exceptions, override append/replace, list and macro extensions, disabling rules, priority thresholds, and testing changes before rollout."
sources: ["https://falco.org/docs/concepts/rules/exceptions/", "https://falco.org/docs/concepts/rules/overriding/", "https://falco.org/docs/concepts/rules/controlling-rules/", "https://github.com/falcosecurity/event-generator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuning Falco false positives with exceptions

Never edit `falco_rules.yaml` (upgrades overwrite it). Put tuning in a local file loaded after
it, e.g. `/etc/falco/rules.d/50-local.yaml` (the default `rules_files` order is `falco_rules.yaml`,
`falco_rules.local.yaml`, then `rules.d`; the order matters for overrides).

## Exceptions (preferred: structured, auditable)
```yaml
- rule: Write below etc
  exceptions:
    - name: config_renderers
      fields: [proc.name, fd.name]
      comps: [=, startswith]
      values:
        - [confd, /etc/nginx/]
        - [consul-template, /etc/haproxy/]
  override:
    exceptions: append
```
Each exception adds `and not (...)` terms built from `fields`, `comps` (one comparison operator per field) and `values`
(one tuple per entry); the `name` is only a label. It stays narrow when every field is listed. Prefer image or
container identifiers plus process name over broad paths.

## Appending conditions
```yaml
- macro: known_debug_images
  condition: (container.image.repository in (reg.example.com/tools/debug, nicolaka/netshoot))

- rule: Terminal shell in container
  condition: and not known_debug_images
  override:
    condition: append
```

## Extending lists and macros
```yaml
- list: allowed_k8s_users
  items: [ci-deployer]
  override:
    items: append
```
Many default rules include `user_*` macros (usually `(never_true)` or `(always_true)`) meant for exactly this;
override those macros instead of the rule when one exists.

## Disable or demote
```yaml
- rule: Contact K8S API Server From Container
  enabled: false
  override:
    enabled: replace
```
Falco 0.38.0 and later can also enable and disable rules from the `rules` section of `falco.yaml`
(for example `- disable: {rule: <name>}`, or `-o "rules[].disable.rule=<name>"` on the command line);
entries are evaluated in order. The `priority` setting in `falco.yaml` is the minimum priority of rules that are
loaded and run.

## Workflow
1. Collect a week of alerts; group by `rule` and `container.image.repository`.
2. For each noisy pair, confirm it is benign, then add the narrowest exception with a comment
   (owner, reason, date).
3. Validate syntax: `falco -V /etc/falco/falco_rules.yaml -V /etc/falco/rules.d/50-local.yaml`
   (`--validate` can be given several times).
4. Prove detection still works: run the falcosecurity/event-generator, which takes a regular
   expression of actions (`event-generator run <regexp>`, for example an action such as
   `syscall.ReadSensitiveFileUntrusted`), preferably in a container since some actions change the system, and
   check the expected rules still fire.

## Gotchas
- Use the `override:` section (`append` or `replace` per key, not both for the same key); using `enabled: true` as an
  override is deprecated and the `enabled` override style is slated for removal in Falco 1.0.0.
- An exception on `proc.name` alone lets any process with that name through; attackers can name
  binaries anything.

## Checked
Documentation release: falcosecurity/falco-website docs (rules overriding, exceptions and controlling-rules pages, master as of 2026-10-24), Falco 0.45.1 CLI options and falco.yaml, falcosecurity/event-generator README, checked 2026-10-26.
Confirmed: `exceptions` structure with `name`, `fields`, `comps`, `values` and `override: exceptions: append`; `override` keys per object type (append for list `items`, macro `condition`, rule `condition`/`output`/`desc`/`tags`/`exceptions`; replace also covers `enabled` and `priority`); `append` and `replace` cannot be combined; `enabled: false` with `override: enabled: replace`; `user_*` macros; `rules[].disable.rule` from Falco 0.38.0; `-V/--validate`; `rules_files` order; event-generator `run [regexp]`.
Corrected: removed the `--loop=false` event-generator flag, Falcosidekick `minimumpriority` routing, "exceptions match exactly as listed" wording and the claim that mixing `append: true` and `override` errors at load.
Method: documentation only; no commands were run.
