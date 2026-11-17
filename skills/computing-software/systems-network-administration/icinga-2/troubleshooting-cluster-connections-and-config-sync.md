---
id: computing-software.systems-network-administration.icinga-2.troubleshooting-cluster-connections-and-config-sync
name: troubleshooting-cluster-connections-and-config-sync
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, troubleshooting, cluster, command-endpoint, config-sync, zones-stage, openssl-s-client, split-brain]
level: advanced
status: docs-checked
description: Troubleshoot Icinga 2 cluster problems - connection and TLS errors on port 5665, unauthenticated clients, command endpoint UNKNOWN results, missing zone, and config sync staging.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/15-troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting cluster connections and config sync
Check file permissions and packet filters first. Configure cluster health checks.

**Connection errors:** network configuration, packet loss, firewalls. Default port 5665; use `tcpdump -n port 5665 -i any`, `netstat -tulpen | grep icinga`, `nmap`.

**TLS errors:** check certificate file permissions and that every endpoint uses the same CA, issuer, CN and validity. Test manually with `openssl s_client -CAfile ca.crt -cert node.crt -key node.key -connect master:5665`.

**Unauthenticated clients:** log lines `New client connection for identity '...' (unauthenticated)` are normal during agent/satellite setup. If they persist, verify certificates.

**Split-brain:** if endpoints in an HA zone cannot reconnect, history may differ; the replay log resynchronises, but find the network cause.

**Command endpoint errors** show as `UNKNOWN` results: ApiListener does not accept commands; CheckCommand definition missing on the agent; plugin missing; unresolved macros. Check `check_source`, `icinga2.log`, the debug log, and event streams.

**Zone required:** a host with `command_endpoint` but no `zone` makes the config compiler error (fixed in 2.11). Move the objects from `conf.d` into `zones.d/master`.

**Config sync:** only one config master per zone may hold files in `zones.d`. It copies them to `/var/lib/icinga2/api/zones`, marks them `.authoritative`, and syncs only valid config. Nodes 2.11 and newer stage received config in `/var/lib/icinga2/api/zones-stage` first. Typical errors: `accept_config` not set, or the received zone is missing from `zones.conf`.

## Checked

2026-11-04. Confirmed against the Icinga 2 troubleshooting chapter: unauthenticated client log line, split-brain and replay behaviour, zones-stage staging from 2.11, .authoritative marker.

Method: documentation only; no commands were run.
