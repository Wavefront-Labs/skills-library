---
id: computing-software.firmware-embedded-development.bootloader-development.staged-fleet-rollout
name: staged-fleet-rollout
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [staged-rollout, ab-update, canary-release, ota-campaign, fleet-health-metrics, firmware-embedded-development]
level: advanced
status: draft
description: "Roll firmware out to a fleet in stages: canary cohorts, health metrics that gate progression, automatic halt and rollback, and the device behaviour that makes it safe."
sources:
  - https://docs.memfault.com/docs/platform/ota
  - https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html
  - https://docs.mender.io/overview/deployment
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Staged fleet rollout

A bug that slipped through testing should hit 50 devices, not 50,000. Staged rollouts are how
firmware teams contain that risk.

## Stages (example)
| Stage | Cohort | Soak time | Gate |
|---|---|---|---|
| 0 | internal devices / test rack | 1-3 days | no crashes, all features pass HIL |
| 1 | 1% of fleet, mixed hardware revisions and regions | 2-3 days | metrics within thresholds |
| 2 | 10% | 3 days | same |
| 3 | 50% | 2 days | same |
| 4 | 100% | | |
Cohorts are chosen randomly but stratified: every hardware revision, battery type and
connectivity type must be represented early.

## Health metrics that gate progression
Compare updated cohort vs a control cohort on the old version over the same period:
- Crash/reset rate per device-day (by reset reason: watchdog, HardFault, brown-out).
- Update success rate, rollback (unconfirmed image reverted) rate, time-to-confirm.
- Connectivity: reconnect count, time online.
- Battery drain rate (mAh/day) and sensor data gaps.
- Key business events (measurements uploaded per day).
Define thresholds before the rollout ("no more than +10% resets per device-day"); automate the halt.

## Device-side requirements
- **Self-test + confirm**: the new image marks itself confirmed only after passing health checks
  (connected to the server, sensors read OK); otherwise the bootloader reverts on the next reset.
- **Telemetry carries the firmware version and build ID** in every report and crash dump.
- **Randomised update windows** (jitter) so a cohort doesn't all reboot at once (support load,
  networks of devices that depend on each other).
- **Server-controlled targeting** (device group, version constraints) rather than "latest for all".
- Respect user/operational constraints: don't update during active operation, low battery,
  or metered connections if configured.

## Halt and rollback
- Halt: stop assigning the release to new devices (devices mid-download finish or abort per policy).
- Rollback: publish the previous version as a new release (with a higher build number if
  anti-rollback requires) or use a "downgrade allowed" flag, only above the security counter floor.

## Verify
- [ ] A deliberately broken canary build (crash after 10 minutes) halts at stage 1 automatically.
- [ ] Dashboards show per-version metrics; every device reports its version within 24 h of update.
