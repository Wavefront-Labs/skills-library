---
id: computing-software.cybersecurity-defensive.wazuh.docker-listener-wodle
name: docker-listener-wodle
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [docker-listener, container-security, wodle, pip3, python]
level: practitioner
status: docs-checked
description: "Enable the Wazuh docker-listener wodle on an agent: Python and pip dependencies, disabled, attempts and scheduling options, the PEP 668 gotcha."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/container-security/monitoring-docker.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Docker listener runs on an agent installed on the Docker host and forwards Docker events to the Wazuh server.

Requirements: Python 3, compatible with 3.8 to 3.13 (later versions should work but are not assured). Install with pip3: `docker==7.1.0`, `urllib3==1.26.20`, `requests==2.32.2`; the docs also show the same command with `--break-system-packages` for an externally managed Python. The manager already includes these dependencies; install them only when configuring an agent.

Enable in `/var/ossec/etc/ossec.conf`:

```xml
<wodle name="docker-listener">
  <disabled>no</disabled>
</wodle>
```

Restart with `systemctl restart wazuh-agent`.

Options and defaults:
- `disabled`: `no`
- `attempts`: `5` (positive number); the number of attempts to execute the listener if it fails
- `run_on_start`: `yes`; runs the listener when the agent starts
- `interval`: `1m`; waiting time to rerun the listener if it fails (suffixes s, m, h, d, M)
- `day`: day of month 1 to 31; interval must be a multiple of months (default one month)
- `wday`: day of week (sunday/sun ... saturday/sat), not compatible with `day`; interval a multiple of weeks (default one week)
- `time`: `hh:mm`; with only `time` set, interval must be a multiple of days or weeks (default one day)

Gotcha: with `--break-system-packages`, pip3 modifies the default externally managed Python environment (PEP 668). To avoid that, use a virtual environment and update the shebang of `/var/ossec/wodles/docker/DockerListener` to the virtual environment's interpreter.

## Checked

2026-11-08: confirmed against the Wazuh docs page Using Wazuh to monitor Docker (read in full): Python 3.8 to 3.13 compatibility, docker 7.1.0 / urllib3 / requests pins, the break-system-packages variant and PEP 668 note, the virtual environment shebang advice, the wodle block and restart, and every option default and allowed value. Removed the unsupported Python 3.11 to 3.12 version range.
Method: documentation only; no commands were run.
