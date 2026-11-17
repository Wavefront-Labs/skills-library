---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-server-setup-and-upgrades
name: grafana-server-setup-and-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, grafana-config, grafana-ini, grafana-database, postgres, mysql, sqlite, grafana-ha, grafana-upgrade, grafana-migration, grafana-plugins, plugin-management, plugin-signing, data-sources, datasource-provisioning, environment-variables, root-url, reverse-proxy, image-renderer, feature-toggles, backup]
level: advanced
status: docs-checked
description: "Run Grafana as a service: grafana.ini/env config, Postgres for HA, data source and dashboard provisioning, plugin loading, image renderer, upgrades and backups."
sources: ["https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/", "https://grafana.com/docs/grafana/latest/setup-grafana/set-up-for-high-availability/", "https://grafana.com/docs/grafana/latest/upgrade-guide/", "https://grafana.com/docs/grafana/latest/administration/plugin-management/", "https://grafana.com/docs/grafana/latest/administration/provisioning/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Grafana server setup, configuration and upgrades

**Goal:** a Grafana deployment that is reproducible from config, survives a node loss,
and can be upgraded (and rolled back) without losing dashboards.

## 1. Configuration and the essentials
Defaults come from `conf/defaults.ini`; custom settings from `conf/custom.ini` or the file given with `--config`
(Deb and RPM packages use `/etc/grafana/grafana.ini`). An environment variable `GF_<SECTION NAME>_<KEY>` overrides an
existing option: uppercase, periods and dashes become underscores. Use env vars to override options, not to add new
ones. Values can use `$__env{VAR}` (or `${VAR}`) and `$__file{/path}` (file contents, whitespace trimmed).
```ini
[server]
root_url = https://grafana.example.com/    # full browser URL; needed for OAuth callbacks and sub-path proxies
serve_from_sub_path = false                 # true if root_url has a sub-path such as /grafana
http_port = 3000
[database]
type = postgres                              # mysql, postgres or sqlite3; sqlite3 is not recommended for production
host = pg.example.com:5432
name = grafana
user = grafana
password = $__file{/etc/grafana/secrets/db}
ssl_mode = require                           # Postgres: any valid libpq sslmode
max_open_conn = 50
[security]
admin_password = $__file{/etc/grafana/secrets/admin}    # only applied on first run
secret_key = $__file{/etc/grafana/secrets/secret_key}   # signs data source secrets (AES-256 CFB); changing it needs data source settings re-encoded
cookie_secure = true                         # when Grafana is served over HTTPS
[users]
default_theme = system                       # dark (default), light or system
[unified_alerting]
ha_peers = grafana-0.grafana-headless:9094,grafana-1.grafana-headless:9094
[dashboards]
versions_to_keep = 20                        # per dashboard; default 20
min_refresh_interval = 10s                   # default 5s; stops users setting faster refresh
[analytics]
reporting_enabled = false
[log]
mode = console
level = info
[feature_toggles]
# one `<name> = true|false` entry per toggle; the `enable = a b` list form is deprecated
```
Behind a reverse proxy, set `root_url` (add the sub-path to it if you serve from one).

## 2. HA
- Run two or more active-active servers behind a load balancer, all using one shared **MySQL or Postgres** database;
  the default embedded sqlite3 cannot be shared.
- The shared database tracks session information (auth tokens), so the load balancer needs no session affinity.
- Alerting HA: `[unified_alerting] ha_peers` (comma-separated `<HOST>:<PORT>`; enables HA mode; `ha_listen_address`
  defaults to `0.0.0.0:9094`, used for TCP and UDP) or the `ha_redis_*` settings (`ha_redis_address`). All alerts run
  on every server and notifications are sent once; load distribution between servers is not supported.
- Grafana Live works with limitations in HA; `[live] ha_engine` is experimental and the only value is `redis`.
- Image renderer as a separate service: `[rendering] server_url` (remote renderer URL) and `callback_url` (URL where
  Grafana is reachable, when the renderer runs on another server).
- Grafana Enterprise HA: license token in the name of the cluster's shared hostname and `root_url` set to it.

## 3. Provisioning (file-based, applied at start)
Environment variables work in provisioning YAML as `$NAME` or `${NAME}`; write `$$` for a literal `$`. Use them for
values only, not keys, and not inside dashboard JSON files.
```yaml
# provisioning/datasources/prometheus.yaml
apiVersion: 1
prune: true                     # delete provisioned data sources removed from the file
datasources:
  - name: Prometheus
    uid: prom-prod              # stable uid: dashboards reference it
    type: prometheus
    access: proxy
    url: http://mimir-query-frontend/prometheus
    isDefault: true             # one default per organization
    jsonData: { httpMethod: POST, timeInterval: "30s", prometheusType: Mimir, httpHeaderName1: X-Scope-OrgID }
    secureJsonData: { httpHeaderValue1: team-payments }
    editable: false
# provisioning/dashboards/teams.yaml
apiVersion: 1
providers:
  - name: teams
    type: file
    disableDeletion: false
    allowUiUpdates: false
    updateIntervalSeconds: 30
    options: { path: /var/lib/grafana/dashboards, foldersFromFilesStructure: true }
```
- Data sources: `deleteDatasources` entries are removed before others are added or updated. With several Grafana
  instances, give each data source a `version` and raise it on change; Grafana only updates data sources with the same
  or lower version.
- Dashboards: a JSON `uid` keeps URLs stable across instances; `id` is null. With `updateIntervalSeconds` of 10 or
  less Grafana watches the filesystem (events may not arrive over Docker bind mounts or network filesystems), above 10
  it polls. `foldersFromFilesStructure` requires `folder` and `folderUid` to be unset; nesting is supported to 4 levels.
- With `allowUiUpdates: false` a UI save shows "Cannot save provisioned dashboard". With `true`, a UI save persists to
  the database but the provisioning file overwrites it on the next change, ignoring `version`.
- `provisioning/plugins` configures already-installed app plugins (it does not install them). Alerting provisioning is
  documented separately (Provision Grafana Alerting resources).

## 4. Plugins
- Installing, updating and uninstalling needs the Server Admin role; Org Admins can configure app plugins but not
  install them. `[plugins] plugin_admin_enabled` defaults to true; false hides the install controls.
- `[plugins] preinstall` takes a comma-separated list installed at startup from the catalog (asynchronously;
  `preinstall_sync` installs before start). Pin with `plugin_id@version`; unpinned entries update to the latest
  version on startup unless `preinstall_auto_update = false`. Env form: `GF_PLUGINS_PREINSTALL`.
- Grafana checks plugin signatures on load. `allow_loading_unsigned_plugins` (comma-separated ids) loads unsigned
  plugins and is not recommended; plugins with modified signatures never load.
- `disable_plugins` lists plugin ids that are not loaded, core plugins included.

## 5. Upgrade procedure
1. Read the upgrade guide for the target version (guides exist per major version: v11, v12, v13; v10.4 and earlier
   are archived). Grafana states upgrades are backward compatible; you can upgrade to any supported release from any
   supported release.
2. Back up the database (`pg_dump` for Postgres, or copy the sqlite file with Grafana stopped), the provisioning files
   and the `secret_key`; note plugin versions.
3. Rehearse on a staging copy of the database; rollback means restoring the backup and the old version.
4. Roll out, then verify SSO login, a Prometheus panel, an alert evaluation and a notification test.
5. Keep `versions_to_keep` high enough that dashboard edits stay recoverable per dashboard.

## 6. Backups and DR
- The database holds dashboards, users, alert rules and data sources with encrypted secrets; back it up before
  upgrades and on a schedule, together with the `secret_key`.
- Provisioning files and Terraform state are the second copy for the reproducible parts.
- Test restore into a scratch instance: dashboards render, data sources connect.

## Gotchas
- `secret_key` cannot be changed without updating data source settings to re-encode them; back up first.
- sqlite cannot be shared between replicas: HA needs a shared MySQL or Postgres database.
- MySQL: set `max_open_conn` on both Grafana and the database, and keep `conn_max_lifetime` shorter than `wait_timeout`.

## Verify
- [ ] A fresh instance built from provisioning plus a database restore shows the same dashboards and working data sources.
- [ ] Data sources test OK on every replica.
- [ ] Upgrade rehearsal on staging passed: login, panels, alert evaluation, notification test.
- [ ] Plugin list in prod matches the pinned list in config.

## Checked
Checked 2026-11-08 against the five Grafana docs pages in sources (configuration, high availability, upgrade guide,
plugin management, provisioning), read in full for the HA, upgrade, plugin and provisioning pages and by section for
the configuration reference. Removed as not stated there: grafana cli commands and admin data-migration notes, the
plugin signing and `grafanaDependency` details, Helm chart and grafana-operator notes, the websocket path, the
`/api/health` check, exemplar and derived-field jsonData examples, the access-control and alerting provisioning
folders, and the claim that migrations are irreversible.
Method: documentation only; no commands were run.
