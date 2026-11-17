---
id: computing-software.systems-network-administration.dns-dhcp.kea-logging-and-statistics
name: kea-logging-and-statistics
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, dhcp-troubleshooting, kea-logging, kea-statistics, loggers, debuglevel, statistic-get-all, kea-dhcp4, pool-utilisation, kea-exporter, prometheus, dhcp4-packets]
level: practitioner
status: verified
description: "Troubleshoot and monitor Kea: configuring loggers and debug levels per component, reading key log messages, statistics commands for pool usage, and Prometheus export."
sources:
  - https://kea.readthedocs.io/en/latest/arm/logging.html
  - https://kea.readthedocs.io/en/latest/arm/stats.html
  - https://github.com/mweinelt/kea-exporter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea logging and statistics

## Loggers
```json
"loggers": [
  {"name": "kea-dhcp4",
   "output-options": [{"output": "/var/log/kea/kea-dhcp4.log", "maxsize": 10485760, "maxver": 8}],
   "severity": "INFO"},
  {"name": "kea-dhcp4.packets",
   "output-options": [{"output": "/var/log/kea/kea-dhcp4-packets.log"}],
   "severity": "DEBUG", "debuglevel": 50}
]
```
- Severity: FATAL, ERROR, WARN, INFO, DEBUG, or NONE to silence a logger; a logger emits its
  severity and everything above it. `debuglevel` (0 to 99) only applies to DEBUG. Documented
  levels: 0 startup/shutdown messages, 10 API commands, 15 reasons a packet was dropped, 40 tracing
  and expression results, 45 adds details such as the selected subnet, 50 hook status, lease and
  packet processing, 55 everything including full packet contents.
- Since Kea 2.7.9 a log file must be in the build-time log directory (`var/log/kea` under the
  install prefix) or the one named by `KEA_LOG_FILE_DIR`; any other path in `output` is refused,
  so give a bare file name to use the default directory. `maxsize` default is 10240000 bytes
  (rotation is off below 204800) and `maxver` (default 1) is how many rotated files are kept.
- Child loggers narrow scope: `kea-dhcp4.packets` (packet details), `kea-dhcp4.leases` (allocation
  decisions), `kea-dhcp4.dhcpsrv`, `kea-dhcp4.ddns`, `kea-dhcp4.hosts`, `kea-dhcp4.ha-hooks`.
- `output` can be `stdout`, `stderr`, `syslog`, `syslog:name` (the name used in syslog, not the
  facility), or a file. Changing loggers requires `config-reload` or `config-set`.

## Messages to know
| Message ID | Meaning |
|---|---|
| `DHCP4_LEASE_ALLOC` | lease granted in response to a DHCPREQUEST (sent in the DHCPACK) |
| `DHCP4_LEASE_OFFER` | address will be offered (DHCPDISCOVER) |
| `DHCP4_PACKET_NAK_0001` | failed to select a subnet for the incoming packet (0002: invalid address requested by INIT-REBOOT; 0003/0004: failed to advertise/grant a lease) |
| `ALLOC_ENGINE_V4_ALLOC_FAIL` | allocation failed after N attempts: pool exhausted. Not logged when N is 0 because no pool was usable for the client (more detailed messages precede it) |
| `DHCP4_SUBNET_SELECTION_FAILED` | debug level 50: failed to select a subnet for the client |
| `DHCP4_PACKET_DROP_0002` | no suitable subnet configured for a direct client on that interface |
| `DHCP4_PACKET_DROP_0001` | packet could not be parsed (debug level 15) |
| `DHCP4_PACKET_DROP_0003` | dropped: it contains a foreign server identifier |
| `HA_STATE_TRANSITION` | HA server moved between states; other `HA_*` messages cover partner communication |
Search by client MAC: the client label looks like `[hwtype=1 00:11:22:33:44:55], cid=[...], tid=0x...`.

## Statistics
Via the unix socket or an HTTP control socket (add `"service":["dhcp4"]` through a Control Agent):
```
curl -s -X POST http://127.0.0.1:8000/ -H 'Content-Type: application/json' \
  -d '{"command":"statistic-get-all"}' | python -c "import json,sys; a=json.load(sys.stdin)[0]['arguments']; print({k:v[0][0] for k,v in a.items() if k.startswith('subnet[10].')})"
```
Each statistic is a list of `[value, timestamp]` pairs, newest first in the ARM sample reply; the filter keeps the newest
value of every `subnet[10].*` statistic (tested on a sample reply; use `jq` if you have it).
Key stats: `subnet[N].total-addresses`, `subnet[N].assigned-addresses`, `subnet[N].declined-addresses`
(N is the subnet id), `pkt4-discover-received`, `pkt4-offer-sent`, `pkt4-nak-sent`,
`pkt4-receive-drop`, `v4-allocation-fail` (with `-no-pools`, `-classes`, `-subnet` and
`-shared-network` variants). Utilisation = assigned / total. Declined addresses accumulate when
clients send DHCPDECLINE after detecting a conflict (for example static devices inside pools).

## Prometheus
The Stork agent on the Kea host is a Prometheus exporter (default TCP port 9547 for Kea). Metrics use
the `kea_` prefix, for example `kea_dhcp4_addresses_assigned_total` and `kea_dhcp4_addresses_total`;
utilisation is their ratio, and Stork's own utilisation bars turn warning at 80 % and critical at
90 %. The stats are not protected: restrict the endpoint to the Prometheus host. See the Stork
monitoring skill. Alert on utilisation approaching 100 %, allocation failures, and NAK spikes.

## Verify
- [ ] Packet logger can be switched on for an incident and off again without restart issues.
- [ ] Per-subnet utilisation graphed with an exhaustion alert.
