---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-alertmanager-configuration-methods
name: prometheus-operator-alertmanager-configuration-methods
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [alertmanager-config, alertmanagerconfig-crd, configsecret, alertmanagerconfiguration, global-config, templates]
level: practitioner
status: docs-checked
description: "Choose how to configure Alertmanager: a native config Secret, selected AlertmanagerConfig resources, or a global AlertmanagerConfig."
sources:
  - https://prometheus-operator.dev/docs/developer/alerting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three ways to supply Alertmanager configuration.

## 1. Native configuration in a Secret
Create a Secret named `alertmanager-{ALERTMANAGER_NAME}` whose key is `alertmanager.yaml`:
```bash
kubectl create secret generic alertmanager-example --from-file=alertmanager.yaml
```
For an Alertmanager named `example` the Secret must be `alertmanager-example`. To use another name set `spec.configSecret`. Templates and password files can be stored as extra keys in the same Secret; they appear under `/etc/alertmanager/config`, so reference them as `templates: ['/etc/alertmanager/config/*.tmpl']`.

## 2. AlertmanagerConfig resources
Namespaced objects holding routes, receivers and inhibition rules. The operator merges the selected objects into the main Alertmanager configuration, so the `Alertmanager` must select them with `spec.alertmanagerConfigSelector` (and optionally `alertmanagerConfigNamespaceSelector`), for example matching the label `alertmanagerConfig: example`.

## 3. Global AlertmanagerConfig
Set `spec.alertmanagerConfiguration` to the `name` of one AlertmanagerConfig in the same namespace; it is used for the Alertmanager configuration instead of the `alertmanager-<name>` Secret. When the operator generates configuration from this global resource, the namespace label is not enforced for routes and inhibition rules.

Choose the Secret for full native control, AlertmanagerConfig for team-owned routing.

## Checked

2026-11-08. Read the developer alerting guide in full. Corrected the global AlertmanagerConfig description (name in the same namespace, not name and namespace) and removed an unsourced claim about namespace scoping of selected configs.

Method: documentation only; no commands were run.
