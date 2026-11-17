---
id: computing-software.devops-ci-cd.argo-rollouts.metric-provider-and-step-plugins
name: metric-provider-and-step-plugins
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [plugin, metric-provider, stepplugins, metricproviderplugins, argo-rollouts-config, analysis, argo-rollouts]
level: sme
status: docs-checked
description: "Extend Argo Rollouts with metric provider plugins and canary step plugins configured in the argo-rollouts-config ConfigMap."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/analysis/plugins/
  - https://argo-rollouts.readthedocs.io/en/stable/features/canary/plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Plugins support metric providers and canary steps that are not built in. They are configured in the `argo-rollouts-config` ConfigMap, the same one used for traffic router plugins. Metric provider plugins are beta (since 1.5.0); step plugins are alpha (since 1.8.0).

**Metric provider plugins** use the key `metricProviderPlugins`:

```yaml
data:
  metricProviderPlugins: |-
    - name: "argoproj-labs/sample-prometheus"
      location: "file://./my-custom-plugin"
```

Install options match traffic router plugins: mount the executable (init container, shared volume, or built into the image) with a `file://` location, or host it over HTTP(S) with an optional `sha256`. The plugin name must match what the plugin expects.

**Canary step plugins** use the key `stepPlugins`, and a plugin is invoked as a canary step:

```yaml
steps:
  - plugin:
      name: example
      config:
        key: value
```

The step plugin's `name` references the plugin configured in the ConfigMap; for the available `config`, see that plugin's own documentation. A step plugin can also be disabled globally with `disabled: true` in its ConfigMap entry, which skips it in every Rollout.

Operational caution: the controller will not start if it cannot download or find the plugin executable, so choose the install method with outage risk in mind (HA mode helps a little because each pod downloads the plugin at startup).

Verify controller logs at startup, then run a test AnalysisRun using the plugin.

## Checked
2026-11-08. Confirmed against the Argo Rollouts Metric Plugins, Canary Step Plugins and Traffic Router Plugins pages: `metricProviderPlugins` and `stepPlugins` keys, the `argo-rollouts-config` ConfigMap, `file://` and HTTP(S) locations with optional `sha256`, the install options, the plugin step syntax, the `disabled` flag, the startup caution and the beta and alpha statuses. Removed the claims that the core accepts no new metric integrations and about AnalysisTemplate provider selection, which are not on these pages.
Method: documentation only; no commands were run.
