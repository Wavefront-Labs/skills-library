---
id: computing-software.cloud-infrastructure-engineering.netdata.troubleshoot-missing-stock-alerts
name: troubleshoot-missing-stock-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, missing-alerts, file-shadowing, dyncfg-override]
level: practitioner
status: docs-checked
description: "Find why stock Netdata alerts are missing: health disabled, stock config disabled, user file shadowing a stock file or dynamic configuration overrides."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Check in order:

1. `[health] enabled = no` disables all alerting. No output from this grep means the default (enabled):

```
grep 'enabled' /etc/netdata/netdata.conf
```

2. `enable stock health configuration = no` disables stock alerts while custom ones still run:

```
grep 'enable stock health configuration' /etc/netdata/netdata.conf
```

Restart after changing either (`sudo systemctl restart netdata`); `reload-health` does not reload `netdata.conf`.

3. File shadowing: a user file with the same filename as a stock file hides it. Find overlaps:

```
comm -12 <(ls /etc/netdata/health.d/ | sort) <(ls /usr/lib/netdata/conf.d/health.d/ | sort)
```

Remove the shadowing copy and reload:

```
sudo rm /etc/netdata/health.d/<filename>.conf
sudo netdatacli reload-health
```

4. Dynamic config overrides: UI or API edits replace file definitions and persist. Use Reset to default in the UI, or remove the dynamic config through the API.

Verify: a healthy Agent has hundreds of stock alerts.

```
curl -s "http://localhost:19999/api/v1/alarms?all" | jq '.alarms | to_entries[].value.name' | sort -u | wc -l
```

Also: if all lookup values are NULL, `$this` becomes NaN and the alert is UNDEFINED.

## Checked

2026-11-04. Confirmed against the Netdata Health README troubleshooting section: the [health] enabled and enable stock health configuration settings with their grep checks, the reload-health caveat, file shadowing and the comm overlap command, the reload step, DynCfg overrides and Reset to default, the hundreds-of-stock-alerts count command, and the all-NULL gives NaN note. Nothing removed.

Method: documentation only; no commands were run.
