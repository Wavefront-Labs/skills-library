---
id: computing-software.firmware-embedded-development.low-power-design.thread-zigbee-sleepy-end-device
name: thread-zigbee-sleepy-end-device
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [sleepy-end-device, thread-sed, ssed, csl, poll-period, zigbee-end-device, openthread, low-power, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Configure Thread sleepy end devices in OpenThread: poll period vs latency, SSED with CSL, child timeouts, and measuring average current."
sources:
  - https://github.com/openthread/openthread/blob/main/include/openthread/link.h
  - https://github.com/openthread/openthread/blob/main/include/openthread/thread.h
  - https://github.com/openthread/openthread/blob/main/src/cli/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sleepy end devices (Thread)

A sleepy end device (SED) turns its radio off and relies on a parent router to buffer frames for
it. The power knob is how often it wakes to listen.

## Thread SED (poll-based)
- Child sends a MAC Data Request to its parent every **poll period**; parent replies with buffered
  frames. Average current scales with 1/poll period.
- OpenThread: `otLinkSetPollPeriod(instance, 30000)` (ms) or CLI `pollperiod 30000`.
  Mode: `otThreadSetLinkMode` with `mRxOnWhenIdle = false`. The CLI `pollperiod` command is documented as
  for certification tests; production code should use the API.
- Downlink latency = up to one poll period. A 30 s poll is fine for a sensor; a lock or light needs
  faster response.
- Child timeout (`otThreadSetChildTimeout`, CLI `childtimeout`; the build-time default
  `OPENTHREAD_CONFIG_MLE_CHILD_TIMEOUT_DEFAULT` is 240 s) must exceed the poll period by a margin
  or the parent drops the child.

## Thread SSED with CSL
- Coordinated Sampled Listening: the child wakes on a schedule (the CSL period) for a short receive
  window and the parent sends then, instead of the child polling.
- `otLinkSetCslPeriod(instance, period_us)` takes the period in **microseconds**, which must be a
  multiple of 160 us (`OT_LINK_CSL_PERIOD_TEN_SYMBOLS_UNIT_IN_USEC`), else `OT_ERROR_INVALID_ARGS`; `0`
  disables CSL. CLI: `csl period 500000` (500 ms), `csl channel <channel>`; also `csl accuracy` and
  `csl uncertainty`. Needs `OPENTHREAD_CONFIG_MAC_CSL_RECEIVER_ENABLE` in the build.

## Zigbee
Zigbee end devices also poll a parent; the stack names and timings differ per vendor SDK, so take the
poll interval and end-device timeout settings from your SDK's documentation.

## Measuring
Profile with a current analyser: idle current between polls (the sleep floor), energy per poll, and
periodic attach/maintenance traffic. Compare with your vendor's power profiler.

## Verify
- [ ] Device stays attached over 48 h with the chosen poll/CSL settings.
- [ ] Downlink command latency measured and within product requirement.

## Checked
2026-11-01. Confirmed in OpenThread sources (link.h, thread.h, mle.h config, src/cli/README.md): `otLinkSetPollPeriod`,
`otThreadSetLinkMode` with `mRxOnWhenIdle`, `otThreadSetChildTimeout`, default child timeout 240,
`otLinkSetCslPeriod` in microseconds and 160 us multiple, CLI `csl period/channel/accuracy/uncertainty`,
`pollperiod` described as certification-test only. Removed: fast-poll behaviour, clock crystal advice, current
figures, and all Zigbee stack function names, timeouts and buffering times (unconfirmed).
Method: documentation only; no commands were run.

