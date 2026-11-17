---
id: computing-software.cloud-infrastructure-engineering.netdata.streaming-parent-child-setup
name: streaming-parent-child-setup
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, stream-conf, parent-child, api-key]
level: practitioner
status: docs-checked
description: "Configure a Netdata Parent to accept streamed metrics and a Child to send them using a uuidgen API key in stream.conf, including the Docker route."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`stream.conf` holds API keys and IPs; treat it as sensitive. In it, `[stream]` configures the sender; every other section is an API key defining which senders the receiver accepts.

```
cd /etc/netdata 2>/dev/null || cd /opt/netdata/etc/netdata
sudo ./edit-config stream.conf
```

Parent:
1. Generate a key: `uuidgen`
2. Rename the `[API_KEY]` section header to the UUID and set:

```
[API_KEY]
    enabled = yes
```

3. Save the file and restart Netdata.

Child:

```
[stream]
    enabled = yes
    destination = PARENT_HOSTNAME_OR_IP:19999
    api key = API_KEY
```

Save and restart Netdata on the Child.

Docker: enter the container with `docker exec -it netdata bash`, then run `cd /etc/netdata && ./edit-config stream.conf` inside it.

For troubleshooting, see streaming-troubleshoot-logs.

## Checked

2026-11-04. Confirmed against the Netdata Configuring Metrics Centralization Points page: stream.conf sensitivity, the [stream] sender section versus API key receiver sections, the edit-config commands, uuidgen, the [API_KEY] rename with enabled = yes, the Child [stream] settings, restarts, and the Docker exec route. Removed the docker restart command, the volume list and the Cloud claiming claim, which the page does not state, and the Verify step.

Method: documentation only; no commands were run.
