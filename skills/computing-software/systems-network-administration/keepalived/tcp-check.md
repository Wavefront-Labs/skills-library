---
id: computing-software.systems-network-administration.keepalived.tcp-check
name: tcp-check
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, tcp-check, health-checking, real-server, connect-timeout, connect-port]
level: practitioner
status: docs-checked
description: "TCP_CHECK health checker: succeeds if a TCP connection opens in time; keywords connect_port and connect_timeout, with the case-study value 3."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP_CHECK

Layer-4 check: only verifies that a TCP connection can be established within the timeout.

```
real_server 192.168.100.4 25 {
    weight 1
    TCP_CHECK {
        connect_timeout 3
    }
}
```
- `connect_port`: TCP port to test (numeric); omitted in the case study.
- `connect_timeout`: timeout (numeric), 3 in all case-study examples.

Checks run every `delay_loop` seconds of the virtual_server. The checker uses nonblocking, timed-out connections.

Verify: closing the service port removes the real server from the IPVS table.

## Checked

2026-11-04. Confirmed the TCP_CHECK keywords on the configuration synopsis page, the value 3 in the case-study examples and the nonblocking timed-out connection on the Software Design page. Removed the claim about which port is checked when connect_port is omitted and the timing claim, which the pages do not state.

Method: documentation only; no commands were run.
