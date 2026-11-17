---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-plugins-smtp-rendering-and-feature-toggles
name: grafana-plugins-smtp-rendering-and-feature-toggles
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, grafana-plugins, plugin-install, plugin-catalog, unsigned-plugins, smtp-config, image-renderer-setup, feature-toggles-config, feature-flags-grafana]
level: practitioner
status: docs-checked
description: "Install Grafana plugins (catalog, grafana cli, GF_PLUGINS_PREINSTALL, unsigned allowlist), configure SMTP and the image renderer service, and manage feature toggles."
sources: ["https://grafana.com/docs/grafana/latest/administration/plugin-management/", "https://grafana.com/docs/grafana/latest/administration/cli/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-docker/", "https://grafana.com/docs/grafana/latest/setup-grafana/image-rendering/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/feature-toggles/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugins, SMTP, image rendering and feature toggles

## Plugins
```bash
grafana cli plugins install grafana-polystat-panel <VERSION>    # pin versions
grafana cli plugins ls ; grafana cli plugins update-all
```
- Containers and config: `[plugins] preinstall` (env `GF_PLUGINS_PREINSTALL`) takes a comma-separated list of plugin IDs,
  pinned with `plugin_id@version` or from a custom URL with `plugin_id@version@url`. Preinstall runs asynchronously
  (`preinstall_sync` installs before start); unpinned preinstalled plugins are updated to the latest version on startup
  (`preinstall_auto_update`), so pin versions. Preinstalled plugins cannot be uninstalled in the UI. `GF_INSTALL_PLUGINS` is a
  build argument of Grafana's custom Dockerfile (`plugin version` pairs, or `url;folder` for private plugins).
- Catalog UI install needs `[plugins] plugin_admin_enabled = true` (default is true) and server admin.
- Unsigned (private) plugins: `[plugins] allow_loading_unsigned_plugins = my-org-panel` (comma-separated IDs; Grafana
  does not recommend it, and plugins with modified signatures are never loaded). Prefer signing private plugins.

## SMTP
```ini
[smtp]
enabled = true
host = smtp.example.com:587
user = <SMTP_USER>
password = $__file{/etc/grafana/secrets/smtp}
from_address = grafana@example.com
from_name = Grafana
startTLS_policy = MandatoryStartTLS
```
`host` defaults to `localhost:25` (use port 465 for implicit TLS); `startTLS_policy` is one of `OpportunisticStartTLS`,
`MandatoryStartTLS`, `NoStartTLS` or empty. Send a test notification from an email contact point to verify.

## Image renderer
Renders panels and dashboards as PNG, PDF or CSV and is required for images in alert notifications.
```yaml
# separate service
image: grafana/grafana-image-renderer:<VERSION>   # a latest tag exists; pin a version in production
env: [{name: AUTH_TOKEN, value: "<shared>"}]
```
```ini
[rendering]
server_url = http://grafana-image-renderer:8081/render
callback_url = http://grafana:3000/
renderer_token = <shared>
[unified_alerting.screenshots]
capture = true
```
The renderer needs a lot of memory and CPU in spiky bursts: the docs recommend at least 16 GiB of memory and 4 CPU cores,
and `GOMEMLIMIT` set below the container limit (about 1 GiB per 8 GiB of limit). Grafana's
`concurrent_render_request_limit` (default 30) caps concurrent render requests. `AUTH_TOKEN` on the service must match
`[rendering] renderer_token`.

## Feature toggles
```ini
[feature_toggles]
exploreMixedDatasource = false     # <NAME> = <value>, e.g. disable an on-by-default toggle
```
The `enable = a b c` list form is deprecated; use one `NAME = value` entry per toggle. The feature toggles page lists
general availability and public preview toggles; experimental toggles are documented only with their feature and need
app mode `development` in some cases. Re-check toggles after each upgrade.

## Verify
- [ ] `grafana cli plugins ls` matches the declared list after a pod restart.
- [ ] Alert email includes a rendered panel image.

## Checked
Date: 2026-10-28. Confirmed against the Grafana configure-grafana reference (`[plugins]` options, `[smtp]` options and defaults, `[rendering]`, `[unified_alerting.screenshots] capture`, `[feature_toggles]` and the deprecated `enable` list), the Grafana CLI page (`plugins install|ls|update-all`), the Docker configuration page (`GF_PLUGINS_PREINSTALL`, `GF_INSTALL_PLUGINS` build arg), the image-rendering page (PNG/PDF/CSV, memory and CPU recommendation, `GOMEMLIMIT`, `AUTH_TOKEN`, `renderer_token`, latest-tag advice) and the feature toggles page. Fixed: the renderer memory and concurrency advice (old Node renderer variables) and the deprecated `enable` toggle form. Removed unconfirmed claims: Helm `plugins:` key, `@grafana/sign-plugin`, air-gapped unpack steps, `/api/featuremgmt`, UI test menu paths, the specific SMTP vendor host and the two example toggle names.
Method: documentation only; no commands were run.
