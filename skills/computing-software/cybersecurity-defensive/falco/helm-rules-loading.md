---
id: computing-software.cybersecurity-defensive.falco.helm-rules-loading
name: helm-rules-loading
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [helm-chart, falcoctl, customrules, rules-files, configmap]
level: practitioner
status: docs-checked
description: "Control which Falco rules the Helm chart loads: automatic falcoctl updates, embedded image rules, customRules configmap, or only your own."
sources:
  - https://falco.org/docs/concepts/rules/default-custom/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Helm chart (version 3.0.0 or later) loads the latest compatible rules and keeps them updated through falcoctl.

Use the rules embedded in the image, with no download at runtime:

```
helm install falco \
    --set falcoctl.artifact.install.enabled=false \
    --set falcoctl.artifact.follow.enabled=false
```

Add custom rules by putting a `customRules` block in a values file (see the chart README) and passing `-f custom_rules.yaml`, with `helm upgrade -i` on an existing install. The docs examples combine this with the two falcoctl settings above. Verify loading with `kubectl logs -n falco daemonsets/falco`. The rules land in `/etc/falco/rules.d` and load in `rules_files` order, which by default is after `falco_rules.yaml`.

Use only your own rules, dropping the defaults and automatic updates, by removing the `falco_rules.yaml` and `falco_rules.local.yaml` entries:

```
helm install falco -f ./custom_rules.yaml \
    --set "falco.rules_files={/etc/falco/rules.d}" \
    --set falcoctl.artifact.install.enabled=false \
    --set falcoctl.artifact.follow.enabled=false
```

Outside Kubernetes use `falco -r /path/to/my/rules1.yaml -r /path/to/my/rules2.yaml`; `-r` takes a file or a directory and can repeat.

Gotcha: the image ships a snapshot of the official rules; only with both `falcoctl` settings false is nothing downloaded at runtime. Note `-r` on the command line makes Falco ignore `rules_files` in the config.

## Checked

2026-11-08. Read the Default and Local Rules page in full. Removed the claim that falcoctl may replace image rules; clarified the customRules example and that -r overrides rules_files.

Method: documentation only; no commands were run.
