---
id: computing-software.cybersecurity-defensive.zeek.capture-loss-and-reporter-logs
name: capture-loss-and-reporter-logs
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, capture-loss, reporter-log, sensor-health, packet-loss]
level: practitioner
status: docs-checked
description: "Check sensor health with capture_loss.log (percentage reading, 0.41 means 0.41 percent) and reporter.log messages for warnings, errors and signals."
sources: ["https://docs.zeek.org/en/current/reference/logs/capture-loss-and-reporter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# capture loss and reporter logs

These logs show how a deployment is performing; formats are `CaptureLoss::Info` and `Reporter::Info`.

**capture_loss.log**: reports analysis of missing traffic, based on gaps in TCP sequence numbers. The value is a percentage: `0.412308930008045` means 0.4123 percent, not 41.23 percent. In the page's example, loss never exceeded 1 percent, so the sensor captured its link well; a small amount of loss is tolerable. Keep watching this log to hold performance at an acceptable level.

**reporter.log**: messages from Zeek itself with a level (the page shows `Reporter::INFO`), message text and location. Examples in the page include Zeek receiving a termination signal and Zeek setting a file for configuring Berkeley Packet Filters.

Workflow: check capture loss regularly, and consult `reporter.log` when Zeek reports internal warnings or errors.

## Checked

2026-11-08. Read the capture_loss.log and reporter.log page in full; removed the Reporter::WARNING level example and the missing-field input example, which the page does not show.

Method: documentation only; no commands were run.
