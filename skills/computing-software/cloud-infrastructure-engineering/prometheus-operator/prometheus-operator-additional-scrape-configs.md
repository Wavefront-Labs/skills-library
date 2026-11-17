---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-additional-scrape-configs
name: prometheus-operator-additional-scrape-configs
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [additionalscrapeconfigs, extra-scrape-config, secret-scrape-config, scrape-config-secret]
level: advanced
status: docs-checked
description: "Append raw Prometheus scrape jobs from a Secret with additionalScrapeConfigs, and know the upgrade risk."
sources:
  - https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/additional-scrape-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.additionalScrapeConfigs` on a `Prometheus` points at a key of a Secret containing raw scrape job configuration, appended to what the operator generates. Jobs must have the form of the Prometheus `scrape_config` documentation.

## Steps
1. Write the jobs to `prometheus-additional.yaml`:
```yaml
- job_name: "prometheus"
  static_configs:
  - targets: ["localhost:9090"]
```
2. Build the Secret manifest and apply it:
```sh
kubectl create secret generic additional-scrape-configs --from-file=prometheus-additional.yaml --dry-run=client -oyaml > additional-scrape-configs.yaml
kubectl apply -f additional-scrape-configs.yaml -n monitoring
```
3. Reference it:
```yaml
spec:
  additionalScrapeConfigs:
    name: additional-scrape-configs
    key: prometheus-additional.yaml
```

## Cautions
Use only one Secret for all additional scrape configurations. Because the text is appended, you are responsible for its validity, and it can break upgrades of Prometheus; review Prometheus release notes for incompatible scrape settings before upgrading.

## Checked

2026-11-08. Read additional-scrape-config.md in full. Steps, Secret command, spec.additionalScrapeConfigs fields and the single-Secret rule match. Removed the unsourced advice to prefer the ScrapeConfig CRD.

Method: documentation only; no commands were run.
