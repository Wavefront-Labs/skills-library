---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-plugin-and-app-provisioning
name: grafana-plugin-and-app-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [plugin-provisioning, app-provisioning, grafana-plugins, provisioning, grafana-helm-chart]
level: practitioner
status: gated
description: "Install Grafana plugins reproducibly (preinstall env, CLI, Helm) and provision app plugin settings with provisioning/plugins YAML including secure fields."
sources: ["https://grafana.com/docs/grafana/latest/administration/provisioning/#plugins", "https://grafana.com/docs/grafana/latest/administration/plugin-management/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#plugins"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin and app provisioning

Two steps: install the plugin binary, then provision its settings (app plugins) or data sources (data source plugins).

## Install
- Grafana 12+: `GF_PLUGINS_PREINSTALL=grafana-clock-panel,grafana-oncall-app@1.9.0` (installed in the background at startup; also `[plugins] preinstall` in grafana.ini; `preinstall_sync` installs before startup, `preinstall_disabled` turns it off, `preinstall_auto_update` defaults to true for unpinned entries: all four keys are in the 13.2.4 `defaults.ini`). Run here: `GF_PLUGINS_PREINSTALL_SYNC="grafana-clock-panel@2.1.8,grafana-piechart-panel@1.6.4"` installed both into the plugins dir and `GET /api/plugins?embedded=0` then listed `grafana-clock-panel` at `2.1.8` with a valid signature. The `GF_INSTALL_PLUGINS` deprecation was not run (gated: unconfirmed, source is paywalled or blocked).
- CLI in an image build: `grafana cli plugins install grafana-clock-panel 2.1.8` (ran with `--pluginsDir`; it printed `Downloaded and extracted grafana-clock-panel v2.1.8 zip successfully`; bake into a custom image for air-gapped installs). Do not use `grafana-piechart-panel`: it is an Angular plugin and Grafana 13.2.4 logged `Refusing to initialize plugin because it's using Angular, which has been disabled` / `angular plugins are not supported`, so it never loads (use the built-in Pie chart).
- Helm chart: `plugins: [grafana-clock-panel]` (not run: no Kubernetes) (gated: unconfirmed, source is paywalled or blocked).
- Unsigned/private plugins: `allow_loading_unsigned_plugins = my-org-panel` in `[plugins]` (the key exists, empty by default, in `defaults.ini`) and copy into the plugins dir (the unsigned load itself was not run) (gated: unconfirmed, source is paywalled or blocked).

## Provision app plugin settings
```yaml
# /etc/grafana/provisioning/plugins/apps.yaml
apiVersion: 1
apps:
  - type: grafana-oncall-app
    org_id: 1
    disabled: false
    jsonData:
      stackId: 5
      onCallApiUrl: https://oncall.example.com
    secureJsonData:
      onCallApiToken: $ONCALL_TOKEN        # env var expansion (not run: the OnCall app was not installed)
```
Run with an installed app (`type: grafana-lokiexplore-app`, `org_id: 1`, `disabled: false`, `jsonData: {stackId: 5}`): `POST /api/admin/provisioning/plugins/reload` returned `Plugins config reloaded` and `GET /api/plugins/grafana-lokiexplore-app/settings` showed `jsonData` `{stackId: 5}`, `enabled: true`, `pinned: true`. The `secureJsonData` part is gated (gated: unconfirmed, source is paywalled or blocked).
Data source plugins are configured in `provisioning/datasources/*.yaml` like built-in ones (`type: <plugin id>`).

## Pinning
Pin versions (`plugin@version`); unpinned installs change behaviour on pod restart.

## Gotchas
- Plugins installed at runtime need outbound internet to grafana.com (the installs above downloaded from it); in restricted networks use a custom image or plugin mirror.
- Provisioned app settings overwrite UI changes at restart (not run) (gated: unconfirmed, source is paywalled or blocked).
- Angular-based plugins do not load in Grafana 13.2.4 (confirmed above; the Grafana Angular deprecation page plans complete removal in 12); check plugin compatibility before upgrading.

## Verify
- [ ] `GET /api/plugins?embedded=0` lists the plugin with the pinned version after a fresh pod start.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 (two local instances, scratch plugin dirs), internet access to grafana.com for downloads.
- Ran `grafana cli plugins install` for clock panel 2.1.8 and piechart panel 1.6.4, a second Grafana with `GF_PLUGINS_PREINSTALL_SYNC` and the pinned `id@version` syntax, app settings provisioning with reload, and the settings API. Read the preinstall keys from `defaults.ini`. Angular statement checked against the log lines and the Grafana angular-deprecation docs page.
- Several lines are gated, so the skill is `gated`.
