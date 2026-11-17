---
id: computing-software.cybersecurity-defensive.nessus.nessus-proxy-and-plugin-update-settings
name: nessus-proxy-and-plugin-update-settings
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-proxy-settings, plugin-updates, proxy, nessuscli, tls-inspection, nessus-deployment]
level: practitioner
status: draft
description: "Configure Nessus proxy, plugin feed update schedule and custom update hosts, and troubleshoot failed plugin updates behind proxies with TLS inspection."
sources: ["https://docs.tenable.com/nessus/Content/ProxyServer.htm", "https://docs.tenable.com/nessus/Content/SoftwareUpdate.htm", "https://docs.tenable.com/nessus/Content/NessusCLIFix.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Nessus proxy and plugin update settings

## Proxy
UI: Settings > Proxy Server: host, port, username, password, auth method (Auto-detect, None, Basic,
Digest, NTLMv1/v2), custom user-agent. CLI equivalents:
```
nessuscli fix --set proxy=proxy.example.internal
nessuscli fix --set proxy_port=3128
nessuscli fix --set proxy_username=<user> ; nessuscli fix --secure --set proxy_password=<PASSWORD>
nessuscli fix --set proxy_auth=basic
```
Allow outbound HTTPS to `plugins.nessus.org`, `downloads.nessus.org`, `sensor.cloud.tenable.com`
(linked to Tenable VM) and `cloud.tenable.com`.

## Updates
- Settings > Software Update: automatic updates of plugins and/or software (all components,
  plugins only, or disabled), frequency daily/weekly/monthly. Nessus Professional default: daily.
- Manual: `nessuscli update --all` or `--plugins-only`; offline: `nessuscli update <plugins.tar.gz>`.
- Custom update host (Nessus Manager / air-gapped mirror): `nessuscli fix --set custom_host=<host>`.
- Pin software version on change-controlled scanners: update plugins automatically, software manually
  after testing.

## Troubleshooting
- `nessuscli update --plugins-only` prints the error. Common:
  - TLS inspection proxy re-signs certs -> update fails certificate checks; bypass inspection for Tenable
    domains, or add the proxy CA where supported.
  - Proxy requires auth but `proxy_auth` wrong -> 407 responses.
  - Expired or invalid activation code -> "not registered".
- After update, plugin compilation runs (high CPU for minutes); scans wait until it finishes.
- Logs: `/opt/nessus/var/nessus/logs/backend.log` (Linux), `nessusd.messages`.

## Gotchas
- Stale plugins mean missed CVEs: alert if plugin set age > 3 days (Settings > About shows
  plugin set date; API `GET /server/properties`).

## Verify
After configuration, Settings > About > Last Updated is today and `nessuscli update --plugins-only`
reports success through the proxy.
