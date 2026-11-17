---
id: computing-software.cloud-infrastructure-engineering.kubernetes.helm-values-precedence-and-merging
name: helm-values-precedence-and-merging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, helm, helm-values-precedence, set-vs-values, reuse-values, helm-upgrade]
level: practitioner
status: verified
description: "Predict the final Helm values: order of chart defaults, parent values, -f files and --set flags, list replacement, null deletion, and the --reuse-values upgrade trap."
sources: ["https://helm.sh/docs/chart_template_guide/values_files/", "https://helm.sh/docs/helm/helm_upgrade/", "https://helm.sh/docs/intro/using_helm/#customizing-the-chart-before-installing", "https://github.com/helm/helm/blob/main/pkg/cli/values/options.go"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Helm values precedence

## Order, lowest to highest
1. Chart's `values.yaml` (and for a subchart, its own `values.yaml`).
2. Parent chart's `values.yaml` section for the subchart (`<subchart-name>:` key).
3. `-f/--values` files, **in command-line order; later files win**.
4. `--set-json`, then `--set`, `--set-string`, `--set-file`, `--set-literal` (all override files).
```bash
helm upgrade --install api ./chart -f values.yaml -f values-prod.yaml --set image.tag=1.4.2
```

## Merge semantics
- Maps merge deeply.
- **Lists replace entirely**: `-f prod.yaml` with `tolerations: [x]` drops every default
  toleration. Charts that expect overrides use maps keyed by name (`extraEnv: {FOO: bar}`).
- `key: null` in a later file **deletes** a default key (e.g. remove a default `resources.limits`).
- `--set` type coercion: whole numbers become ints (`replicas=3`, `h=-2`), `true`/`false` become booleans
  and `null` becomes null. Decimals and zero-padded values stay strings (Helm 3.15: `tag=1.10` renders `"1.10"`,
  `e=007` renders `"007"`). The float trap is in values *files*, where an unquoted `tag: 1.10` loads as 1.1. Use
  `--set-string` for IDs that are plain digits (account numbers) and quote versions in YAML.
- `--set` escaping: `--set 'nodeSelector.kubernetes\.io/os=linux'`, lists `--set 'args={a,b}'`,
  index `--set 'env[0].name=X'` (replaces the whole list with a sparse one).

## Upgrades: the reuse trap
- Default `helm upgrade` (no reuse flags): values = chart defaults + what you pass **now**. Values passed at
  install but not repeated are dropped as soon as you pass any value. Only when you pass **no** values at all
  does Helm copy the previous release's user-supplied values (`reuseValues` in `pkg/action/upgrade.go`), so adding
  a single `--set` silently drops everything else.
- `--reuse-values`: merges new flags onto the **previous release's values** (old chart defaults plus the
  user-supplied values; the source swaps the new chart's defaults for the old ones), ignoring new chart defaults (new required keys stay unset, templates may break).
- `--reset-then-reuse-values` (Helm 3.14+): new chart defaults + previous user-supplied values + new flags. Usually what people meant.
- Best practice: always pass the full set of `-f` files from Git; never rely on reuse.

## Inspect what will be used
```bash
helm get values api                  # user-supplied values of the live release
helm get values api --all            # fully computed values
helm template api ./chart -f values.yaml -f values-prod.yaml --set image.tag=1.4.2 --debug | less
helm show values ./chart             # defaults
helm diff upgrade api ./chart -f ...  # helm-diff plugin: the real change before applying
```

## Globals
`global:` values are visible to the parent and every subchart as `.Values.global.*`;
subchart values cannot otherwise see the parent's.

## Verify
- [ ] `helm get values --all` after upgrade shows intended values; `helm diff` shows no
  surprise removals (lists, tolerations, env).
