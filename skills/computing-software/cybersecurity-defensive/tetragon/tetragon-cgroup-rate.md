---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-cgroup-rate
name: tetragon-cgroup-rate
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [cgroup-rate]
level: practitioner
status: docs-checked
description: "Throttle Tetragon base sensor events per cgroup with the --cgroup-rate option and read THROTTLE_START and THROTTLE_STOP events."
sources:
  - "https://tetragon.io/docs/concepts/cgroup-rate/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cgroup rate limiting

Goal: stop a noisy cgroup from flooding Tetragon with events. Tetragon monitors the event rate per cgroup and throttles it (stops posting its events) when it crosses the configured threshold. When the cgroup's traffic is stable under the limit again, throttling stops and events resume.

## Behaviour

- A `THROTTLE` start event is sent when the cgroup rate limit is crossed.
- A `THROTTLE` stop event is sent when the rate has been below the limit, stable, for 5 seconds.
- The threshold is monitored per CPU: events spread over several CPUs are throttled per CPU only if they cross the threshold on that CPU.
- Only base sensor events are monitored and limited: `PROCESS_EXEC` and `PROCESS_EXIT`.

## Setup

The option is `--cgroup-rate <events,interval>` and is disabled by default.

- `--cgroup-rate=10,1s`: 10 events per second
- `--cgroup-rate=1000,1s`: 1000 events per second
- `--cgroup-rate=100,1m`: 100 events per minute
- `--cgroup-rate=10000,10m`: 10000 events per 10 minutes

## Event format

```json
{
  "process_throttle": {
    "type": "THROTTLE_START",
    "cgroup": "session-429.scope"
  },
  "node_name": "ubuntu-22",
  "time": "2024-07-26T13:07:43.178407128Z"
}
```

The stop event is the same with `"type": "THROTTLE_STOP"`.

## Try it

```shell
tetragon --bpf-lib ./bpf/objs/ --cgroup-rate=10,1s
```

The log shows `Cgroup rate started (10/1s)`. In another terminal generate more than 10 events per second, and watch with `tetra getevents -o compact`:

```shell
while :; do sleep 0.001s; done
```

The output shows `throttle START session-429.scope`. After you stop the loop, `throttle STOP` appears after 5 seconds.

## Checked

Date: 2026-11-07

Cited page read in full; every claim matched to page text.

Method: documentation only; no commands were run.
