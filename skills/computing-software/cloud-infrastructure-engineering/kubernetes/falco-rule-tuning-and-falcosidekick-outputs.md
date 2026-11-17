---
id: computing-software.cloud-infrastructure-engineering.kubernetes.falco-rule-tuning-and-falcosidekick-outputs
name: falco-rule-tuning-and-falcosidekick-outputs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, falco, falco-rule-tuning, falcosidekick, runtime-security, alerting, cks]
level: advanced
status: docs-checked
description: "Cut Falco noise without blinding it: override rules with exceptions and appended macros, set priorities, and route alerts by severity through Falcosidekick to chat, SIEM and responders."
sources: ["https://falco.org/docs/setup/kubernetes/", "https://falco.org/docs/concepts/event-sources/kernel/", "https://falco.org/docs/concepts/rules/overriding/", "https://falco.org/docs/concepts/rules/exceptions/", "https://github.com/falcosecurity/charts/tree/master/charts/falco", "https://github.com/falcosecurity/falcosidekick"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Falco rule tuning and Falcosidekick outputs

## Measure the noise first
```bash
kubectl -n falco logs ds/falco -c falco --since=24h
```
(with `json_output: true`, each line carries a `rule` field you can count). Tune the noisiest rules first.

## Tune with overrides, never by editing upstream files
Put local rules in Helm `customRules`. Use the `override:` section; the older `append` key is deprecated
and will be removed in Falco 1.0.0, and `enabled: true` is deprecated too. Rules files load in order, so an
override must come after the definition it changes:
```yaml
customRules:
  tuning.yaml: |-
    # exception: our backup job legitimately reads sensitive files
    - rule: Read sensitive file untrusted
      exceptions:
      - name: backup_agent
        fields: [k8s.ns.name, proc.name]
        values: [[backup, restic]]
      override:
        exceptions: append

    # widen a macro used by many rules
    - macro: user_known_read_sensitive_files_activities
      condition: (k8s.ns.name = "ci-runners")
      override:
        condition: replace

    # silence a rule entirely (record why)
    - rule: Contact K8S API Server From Container
      enabled: false
      override:
        enabled: replace
```
Prefer **exceptions scoped by namespace + image/process** over disabling rules. Avoid
excepting on `container.id` or pod names (they change).

## Priority and volume controls
- The `priority` setting in `falco.yaml` (chart: `falco.priority`, default `debug`) sets the minimum priority of rules that load.
- Raise priority of rules you actually page on (`override: priority: replace`).
- `outputs_queue` buffers output; Falco also detects dropped syscall events and takes the configured
  actions (see the dropped-events docs), which means blind spots.

## Falcosidekick
```bash
helm upgrade --install falco falcosecurity/falco -n falco --create-namespace \
  --set falcosidekick.enabled=true --set falcosidekick.webui.enabled=true \
  --set falco.json_output=true --set falco.http_output.enabled=true \
  --set falcosidekick.config.slack.webhookurl=https://hooks.slack.com/... \
  --set falcosidekick.config.slack.minimumpriority=error \
  --set falcosidekick.config.loki.hostport=http://loki-gateway.monitoring \
  --set falcosidekick.config.loki.minimumpriority=notice
```
Route by severity: everything to the SIEM/log store, `error`+ to chat, `critical` to the
pager. Each output has its own `minimumpriority` (order: emergency, alert, critical, error, warning,
notice, informational, debug). Falcosidekick can forward to Falco Talon for automatic response; start with labelling, not killing.

## Gotchas
- Driver: `modern_ebpf` needs kernel BTF (usually 5.8+).
- Validate rule changes in CI: `falco -V rules.yaml` (reads the rules file, validates it and exits) and
  `falco --dry-run` (runs without processing events to check configuration and rules).

## Verify
```bash
kubectl exec -it deploy/test -- cat /etc/shadow          # should still alert (Critical/Warning)
kubectl -n falco logs deploy/falco-falcosidekick
```

## Checked

Checked on 2026-10-26 against `falcosecurity/falco-website` docs (`concepts/rules/overriding`, `exceptions`, `concepts/event-sources/kernel/dropped-events`), the Falco source (`falco.yaml`, `userspace/falco/app/options.cpp`), the Helm chart values, `falcosecurity/rules` (`falco_rules.yaml`) and `falcosidekick` `config_example.yaml`.
Confirmed: `override` section with `append` and `replace` and the per-type fields (rule `exceptions` append, `enabled` and `priority` replace, macro `condition` replace); `append` deprecated and removal in 1.0.0; `enabled: true` deprecation; rules `Read sensitive file untrusted` and `Contact K8S API Server From Container`; macro `user_known_read_sensitive_files_activities`; `falco -V` and `--dry-run`; `falco.yaml` `priority`, `json_output`, `outputs_queue`; Falcosidekick `slack.webhookurl`, `minimumpriority` ordering and `loki.hostport`; Falco Talon as an output.
Wrong in the draft: macro `user_known_package_manager_in_container` is not in the default rules (replaced with an existing macro). Removed as unconfirmed: the "since Falco 0.37" version for `override`, the `/etc/falco/rules.d` mount path, the drop-metric name, rate limiting, and the 90 percent volume figure.

Method: documentation only; no commands were run.
