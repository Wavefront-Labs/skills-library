---
id: computing-software.systems-network-administration.dns-dhcp.stork-kea-monitoring
name: stork-kea-monitoring
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, stork, monitoring, prometheus, dashboard]
level: practitioner
status: verified
description: "Monitor Kea and BIND with ISC Stork: server and agent install, machine registration, pool utilisation, HA status, lease search and Prometheus export."
sources:
  - https://stork.readthedocs.io/en/latest/
  - https://www.isc.org/stork/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stork monitoring

Stork is ISC's dashboard for Kea (and BIND): pool utilisation, HA state, lease search, host
reservations, config review and events, plus Prometheus metrics.

## Components
- `isc-stork-server`: web UI and API, PostgreSQL database.
- `isc-stork-agent`: on every Kea/BIND host. It finds Kea daemons from their command lines (`-c`
  config path), reads the control socket and authentication settings from the config, and uses the
  first control socket it can connect to: the daemons' own HTTP control channel on Kea 3.0 and
  later, or the Control Agent for older Kea. It also exports Prometheus metrics (defaults: TCP
  9547 for Kea, 9119 for BIND 9; set with `STORK_AGENT_PROMETHEUS_KEA_EXPORTER_PORT` and
  `..._BIND9_EXPORTER_PORT`).

## Install (packages from cloudsmith.io/~isc)
```
apt install isc-stork-server postgresql
stork-tool db-create --db-name stork --db-user stork
systemctl enable isc-stork-server && systemctl start isc-stork-server    # UI on :8080 (STORK_REST_PORT)
# on each Kea host
apt install isc-stork-agent
su stork-agent -s /bin/sh -c 'stork-agent register -u http://stork.example.internal:8080'
systemctl enable isc-stork-agent && systemctl start isc-stork-agent
```
`--server-url` is the long form of `-u`. Registration can instead be done with an agent token, with
`STORK_AGENT_SERVER_URL` and `STORK_AGENT_HOST` set in `/etc/stork/agent.env`. A server administrator
must then approve the machine in the UI (Services > Machines > Unauthorized, compare the agent token with
`/var/lib/stork-agent/tokens/agent-token.txt`, then Action > Authorize). Registration stores a signed agent
certificate and the CA certificate on the agent (the registration output says so); the ARM's examples
use plain `http` for the registration URL but recommend `https` in production. The package repository is ISC's
Cloudsmith one (`cloudsmith.io/~isc/repos/stork`); the ARM also gives `dnf` commands for RPM distros.

## What to watch
- Subnet and shared-network utilisation (assigned vs total): the pool bar turns orange at 80 %
  (warning) and red at 90 % (critical).
- HA pairs: state (load-balancing/hot-standby/partner-down), last heartbeat.
- Config review: built-in checkers run on request, on config change, or when the host reservation
  database changes; list and toggle them under Configuration > Review Checkers (the list depends
  on your Stork version, so read it there rather than assuming specific checks).
- Lease search (DHCP > Lease Search) over IP, MAC, hostname and similar; it uses Kea control commands
  and needs the `lease_cmds` hook loaded on each Kea server.

## Prometheus
Scrape agents:
```yaml
- job_name: kea
  static_configs: [ { targets: ["kea1:9547", "kea2:9547"] } ]
```
Metrics use the `kea_` prefix, for example `kea_dhcp4_addresses_assigned_total` with
`kea_dhcp4_addresses_total` (their ratio is pool utilisation) and, for prefix delegation,
`kea_dhcp6_pd_assigned_total` with `kea_dhcp6_pd_total`. The `/metrics` endpoint needs no
authentication, so restrict it to the Prometheus host. Grafana templates (`kea-dhcp4.json`,
`kea-dhcp6.json`, `bind9-resolver.json`) are in the `grafana/` directory of the Stork source and are
imported into Grafana by hand.

## Verify
- [ ] Every Kea server shows as online in Stork with utilisation graphs, and Prometheus has non-empty Kea metrics.
