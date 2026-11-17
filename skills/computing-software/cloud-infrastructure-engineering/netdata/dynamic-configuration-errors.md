---
id: computing-software.cloud-infrastructure-engineering.netdata.dynamic-configuration-errors
name: dynamic-configuration-errors
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, http-412, http-403, disable-alert]
level: advanced
status: docs-checked
description: "Troubleshoot Dynamic Configuration failures: HTTP 412 missing bearer token, HTTP 403 roles, disabled alerts that still fire, and No items to enable."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configuration/dynamic-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HTTP 412: in Netdata it means a bearer token was required but missing, not a schema error. Causes: bearer token protection enabled, lost Cloud connection, token older than 24 hours, missing browser auth state.
1. Open `http://IP:19999/api/v3/info`; `cloud.status` should be `online`, otherwise read `cloud.reason`.
2. Log out of and back into Netdata Cloud.
3. Check the bearer token protection setting in `netdata.conf`.
4. If it turns into 403, confirm you are Admin or Manager.

HTTP 403: only Admin and Manager can do more than list. Troubleshooter, Observer, Billing and Community-plan users get List All only. Check Space Settings, Users.

Disabled alert still appears: disabling is per node. Target every node (use Multi-Node Deployment). Manual route in `netdata.conf`:

```
[health]
    enabled alarms = !10min_cpu_usage *
```

then restart the Agent (`netdatacli reload-health` does not reload `netdata.conf`). Or comment the alert out in a `health.d/*.conf` file and run `netdatacli reload-health`.

No items to enable: alerts have an alert-level switch plus per-rule switches. Turn the alert on first; rules cannot run while it is off. To run only some rules: Edit, enable wanted rules (at least one), Submit, then Enable the alert.

## Checked

2026-11-04: the HTTP 412 meaning, causes and resolution steps, the HTTP 403 roles and plan limits, the per-node disable fix with its manual route, and the No items to enable steps confirmed against the Netdata Dynamic Configuration Manager troubleshooting section.

Method: documentation only; no commands were run.
