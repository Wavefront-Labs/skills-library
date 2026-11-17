---
id: creative-arts.design-for-form-and-experience.figma.using-ready-for-dev-status-and-compare-changes
name: using-ready-for-dev-status-and-compare-changes
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [ready-for-dev, dev-mode-status, compare-changes, figma-dev-mode, section-status, design-handoff-status]
level: practitioner
status: docs-checked
description: "Use Dev Mode's Ready for dev and Completed statuses, the automatic Changed state, and Compare changes to review design diffs between versions."
sources:
  - https://help.figma.com/hc/en-us/articles/26781702258583-Dev-Mode-statuses-and-notifications
  - https://help.figma.com/hc/en-us/articles/15023193382935-Compare-changes-in-Dev-Mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ready for dev status and compare changes

Dev Mode lets designers mark what is ready to build and lets developers see what changed since they last looked. Dev Mode features need a Full or Dev seat.

## Statuses
1. Designers mark designs **Ready for dev** and can add a note to the status about updates or changes.
2. **Completed** is the second status; marking Completed and updating changed designs are limited to Education (K-12), Organization, Government and Enterprise plans.
3. **Changed** is set automatically when a design marked Ready for dev or Completed is modified; it cannot be set by hand. Edits to shared library instances, attached variables or styles, and temporary hover effects do not trigger it. Notes on a change also appear in version history and notifications.
4. Viewers with a Full or Dev seat are notified when designs are first marked Ready for dev; higher plans also get alerts for post-change updates and completions. File settings offer Status changes or Nothing.
5. Do not mark frames ready until specs, states and annotations are complete (`creative-arts.design-for-form-and-experience.interaction-design.writing-specs-and-redlines-for-developers`).

## Compare changes
Select a top-level frame or component and click **Compare changes** in the Inspect tab of the right sidebar. Views: **Version history** (pick a previous version; top-level frames only), **Side by side**, **Overlay** (with a transparency slider), **Compare code** and **Compare properties**. Layers are tagged **Edited**, **Added** or **Deleted**. It is available on Professional, Education, Organization, Government and Enterprise plans. From focus view, open the status indicator, choose Show in focus view, then Compare to latest version on a past version.

## Process
- Agree a convention: one section per feature, status set by the designer, a note after each change to ready work.

## Verify
- [ ] Only complete frames carry Ready for dev.
- [ ] Changes after handoff come with a note.

## Checked
2026-11-01. Confirmed against the Dev Mode statuses and notifications and Compare changes in Dev Mode Help Center articles: status names, Changed state rules, notes, notifications, plan limits, Compare changes views, layer tags and focus-view path. Removed (not on those pages): Ready-frames filtering, Jira and integration claims, "list of property changes" wording, change-note authoring in Compare changes.
Method: documentation only; no commands were run.
