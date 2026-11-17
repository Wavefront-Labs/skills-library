---
id: computing-software.game-programming.unity.profile-analyzer-frame-comparisons
name: profile-analyzer-frame-comparisons
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-profile-analyzer, profiler, performance, regression, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity Profile Analyzer to compare profiler captures: median marker times, frame ranges, Compare view deltas and the data files to keep."
sources: ["https://docs.unity3d.com/Packages/com.unity.performance.profile-analyzer@1.2/manual/index.html", "https://docs.unity3d.com/Packages/com.unity.performance.profile-analyzer@1.2/manual/compare-view.html", "https://docs.unity3d.com/Packages/com.unity.performance.profile-analyzer@1.2/manual/single-view.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profile Analyzer frame comparisons

**Goal:** prove an optimisation helped using statistics over many frames, not one spike.

## Capture and load
1. Install the Profile Analyzer package (`com.unity.performance.profile-analyzer`; version 1.2 documents
   compatibility with Unity Editor 2020.3 and later).
2. Record with the Unity Profiler, ideally with the same scene and a repeatable camera path for both runs.
3. In the Profile Analyzer, select **Pull Data** to bring in whatever is in the Profiler window, or **Load** a
   saved Profile Analyzer `.pdata` file. **Load** accepts only `.pdata`; a Profiler `.data` file must first be
   opened in the Profiler and then pulled in with **Pull Data**.
4. The `.pdata` file does not contain the original profile data. Store the Profiler `.data` file (or the `.raw`
   exported from a standalone player) alongside it.

## Single view
Describes one data set with min, max, median, mean and lower/upper quartile values for frames, threads and
markers. The Marker details list is sortable and each row aggregates every instance of that marker across all
filtered threads and all ranged frames. Useful columns: Median, Mean, SD, Min, Max, Range, Count, Count Frame
(average count per frame), Total, Threads. Column preset layouts (Time and count, Time, Totals, and others) and
a Custom layout are available from the Marker columns dropdown in the Filters pane.
Right-click commands include selecting the frames that contain a marker, adding it to the Include or Exclude
filter, and Set as Parent Marker Filter (limit analysis to that marker and those below it on the callstack).

## Compare view
Load two data sets: Left is the first loaded (blue), Right the second (orange). The Marker Comparison list adds
Diff (negative means the left set is bigger, positive means the right is bigger), Diff Percent (relative to the
first data set), Abs Diff, Count Delta and Total Delta columns. Check that the target marker moved and that no
other marker rose to absorb the cost.

## Gotchas
- Clicking a marker jumps to it in the Profiler only if the same data is loaded there and you have made a
  selection in the Profiler beforehand.
- Compare like with like: equal frame ranges and the same scenario; exclude loading frames from the range.

## Verify
- [ ] A perf change records the before and after medians for the target marker from the Compare view.

## Checked
Date 2026-11-09. Read in full as fetched text: package manual About page (v1.2), Single view and Compare view.
Confirmed: Pull Data and Load behaviour, `.pdata` limitation, compatibility with 2020.3 and later, column
meanings, Diff sign convention, context menu commands and the known marker-jump limitation.
Removed as unconfirmed: the menu path, Profiler default frame count, CSV export, histogram and box plot details,
frame-summary percentile feature, the "editor captures include overhead" and thermal-state notes and the
deep-profiling comparison warning.
Method: documentation only; no commands were run.
