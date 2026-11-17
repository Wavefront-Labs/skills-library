---
id: computing-software.systems-network-administration.frigate.frigate-object-filters-and-stationary-objects
name: frigate-object-filters-and-stationary-objects
category: computing-software
field: systems-network-administration
product: frigate
tags: [object-filters, min-score, threshold, min-area, max-area, stationary-objects, false-positives]
level: advanced
status: docs-checked
description: "Cut false positives with Frigate score thresholds, area and ratio limits, and tune how stationary objects are re-checked."
sources: ["https://docs.frigate.video/configuration/object_filters/", "https://docs.frigate.video/configuration/stationary_objects/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Object filters and stationary objects

Scores: a single detection below `min_score` is ignored. `threshold` applies to the computed score, the median of the tracked object's score history (padded to at least three values). In the docs' example a frame at 0.55 below `min_score` becomes 0.0, and the object is only reported once the median crosses the threshold (0.875 on the fourth frame). The top score is the highest computed score reached in the object's lifetime.

Size filters: `min_area` and `max_area` bound the bounding-box area (the example uses 5000 and 100000) to reject a leaf detected as a dog or a tree as a person. `min_ratio` and `max_ratio` bound width divided by height: 1 is square, 0.5 tall and thin, 2 wide and flat.

Stationary objects: an object is stationary when it stays in a very similar position for `detect.stationary.threshold` frames (default 50). Detection is then not run continuously on it; it is re-verified every `detect.stationary.interval` frames (default 50). This saves resources and lets Frigate keep tracking, for example, a parked car without re-detecting it.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/object_filters, docs.frigate.video/configuration/stationary_objects (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
