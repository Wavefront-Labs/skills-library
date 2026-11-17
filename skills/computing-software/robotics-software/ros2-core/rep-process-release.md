---
id: computing-software.robotics-software.ros2-core.rep-process-release
name: rep-process-release
category: computing-software
field: robotics-software
product: ros2-core
tags: [rep-index, rep-2000, rep-2004, package-quality, rep-2005, rep-149]
level: advanced
status: docs-checked
description: "Find the REP governing a convention (2000 releases, 2004 quality levels, 149 package.xml) and cite it correctly."
sources:
  - https://www.ros.org/reps/rep-2000.html
  - https://www.ros.org/reps/rep-2004.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# REP lookup
**Goal:** know which standard answers a question.

- Index: ros.org/reps (`rep-0000`). Key ones: REP 103 standard units and coordinate conventions, 105 coordinate frames for mobile platforms, 2000 ROS 2 releases and target platforms, 2004 package quality categories.
- REP 2004 defines Quality Levels 1 to 5 with requirements such as version policy, public API, feature documentation, a quality declaration, and feature testing and code coverage; check a dependency's quality declaration.
- Read the REP header for its status before relying on it.

## Gotchas
- Quoting an old REP revision; check the latest.

## Self-check
You can name the REP and section that justifies a design choice in a code review.

## Checked
2026-11-03. Confirmed in REP 103, 105, 2000 and 2004 (titles, Quality Levels 1-5, version policy, public API, feature documentation, quality declaration, testing and coverage). Removed: REP 149, 2005 and 144 numbers and package-naming rules, QUALITY_DECLARATION.md filename, Draft/Active/Final status and wiki claims (REP index and those REPs not read).
Method: documentation only; no commands were run.
