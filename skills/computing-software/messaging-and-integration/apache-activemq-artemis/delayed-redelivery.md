---
id: computing-software.messaging-and-integration.apache-activemq-artemis.delayed-redelivery
name: delayed-redelivery
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,delayed-redelivery,redelivery-delay,redelivery-delay-multiplier,max-redelivery-delay,redelivery-collision-avoidance-factor,activemq-artemis]
level: advanced
status: docs-checked
description: "Back off redelivery of rolled-back messages with redelivery-delay, a multiplier, max-redelivery-delay and a random collision-avoidance factor."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/undelivered-messages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delayed redelivery

**Goal:** stop a failing consumer or rolled-back transaction from thrashing (deliver, rollback, redeliver immediately) and burning CPU and network.

## Configure (address-setting)
```xml
<address-setting match="exampleQueue">
   <redelivery-delay-multiplier>1.5</redelivery-delay-multiplier>
   <redelivery-delay>5000</redelivery-delay>
   <redelivery-collision-avoidance-factor>0.15</redelivery-collision-avoidance-factor>
   <max-redelivery-delay>50000</max-redelivery-delay>
</address-setting>
```
- `redelivery-delay`: wait before redelivering a cancelled message; default `0` (none). Other messages continue normally; only the cancelled one is sent back asynchronously after the delay.
- `redelivery-delay-multiplier` (default `1.0`): each delay is the previous delay times this.
- `max-redelivery-delay`: cap, defaulting to `redelivery-delay` * 10.
- `redelivery-collision-avoidance-factor` (default `0.0`, valid 0.0 to 1.0): a random adjustment up or down. The factor is randomly signed, multiplied by a random number between 0.0 and 1.0, then by the delay, and added to it, so a larger factor gives a larger variance.

Worked example from the manual: delay 5000, multiplier 2, max 15000 gives waits of 5000, 10000, then 15000 (capped).

## When to use the collision factor
Many consumers on one queue touching the same external system (for example a database) with overlapping data: one transaction succeeds and the rest fail, and if all are redelivered together the pattern repeats. Randomly padding the delay avoids those collisions.

## Journal cost
Two journal update records are written for each redelivery (delivery count, and a scheduled redelivery if used). With very short delays, keep `max-redelivery-records=1` to avoid unnecessary journal records.

## Checked
2026-11-03. Confirmed against the Artemis user manual page undelivered-messages, Delayed Redelivery section: settings, defaults, the 5000/2/15000 example, collision-avoidance algorithm and journal-record note. Removed: the Verify step.
Method: documentation only; no commands were run.
