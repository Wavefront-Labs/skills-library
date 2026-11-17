---
id: computing-software.cloud-infrastructure-engineering.cilium.hubble-ui-standalone
name: hubble-ui-standalone
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, hubble-ui, standalone, service-map, relay-tls, helm]
level: practitioner
status: docs-checked
description: "Enable the Hubble UI service map with cilium hubble enable --ui or Helm, or deploy it standalone against existing Relay with mounted client certificates."
sources:
  - https://docs.cilium.io/en/stable/observability/hubble/hubble-ui/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hubble UI

Enable: `cilium hubble enable --ui`, or Helm upgrade with `--reuse-values --set hubble.relay.enabled=true --set hubble.ui.enabled=true`.

## Standalone install
When Cilium, Hubble and Relay are already installed, deploy only the UI with Helm values: `agent: false`, `operator.enabled: false`, `cni.install: false`, `hubble.enabled: false`, `hubble.relay.enabled: false`, `hubble.ui.enabled: true`, `hubble.ui.standalone.enabled: true`. If TLS is enabled on the Relay server set `hubble.relay.tls.server.enabled: true` and provide `hubble.ui.standalone.tls.certsVolume` (a projected volume, defaultMode 0400) from a secret such as `my-hubble-ui-client-certs` mapping `tls.crt` to `client.crt`, `tls.key` to `client.key`, `ca.crt` to `hubble-relay-ca.crt`.

The UI reads certs from `/var/lib/hubble-ui/certs/` via env `TLS_RELAY_CA_CERT_FILES` (hubble-relay-ca.crt), `TLS_RELAY_CLIENT_CERT_FILE` (client.crt) and `TLS_RELAY_CLIENT_KEY_FILE` (client.key), so the item paths must match those names.

Note: the page example shows a typo `hubble.ui.enabledd=true` in its --set line; use `hubble.ui.enabled=true`.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/observability/hubble/hubble-ui/. 

Method: documentation only; no commands were run.
