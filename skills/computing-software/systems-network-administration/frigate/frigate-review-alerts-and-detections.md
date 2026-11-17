---
id: computing-software.systems-network-administration.frigate.frigate-review-alerts-and-detections
name: frigate-review-alerts-and-detections
category: computing-software
field: systems-network-administration
product: frigate
tags: [review-items, alerts, detections, alert-labels, tracked-objects, objects-track]
level: practitioner
status: docs-checked
description: "How Frigate groups activity into review items, which objects become alerts or detections and how to restrict alert labels."
sources: ["https://docs.frigate.video/configuration/review/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Review items, alerts and detections

Since 0.14 the UI shows review items, periods where any number of tracked objects were active, instead of one event per object. For two people and a car passing together, 0.13 showed four events; 0.14 and later bundle them into a single review item. Review items for one camera cannot overlap, and watched periods are marked reviewed.

Review items are classed as alerts (higher priority) or detections. Both depend on the object detector first finding the objects, and by default only `person` is tracked. Add labels under `objects: track:` (for example `person`, `car`). By default a review item becomes an alert only if a person or car is detected; the alert labels can be changed to any object or audio label in Settings, Global configuration, Review.

Review previews are bandwidth-optimised low frame-rate clips on a vertical timeline, filterable by date, object type and camera.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/review (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
