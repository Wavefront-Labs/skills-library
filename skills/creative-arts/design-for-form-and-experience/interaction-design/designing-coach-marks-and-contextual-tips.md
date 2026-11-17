---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-coach-marks-and-contextual-tips
name: designing-coach-marks-and-contextual-tips
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [coach-marks, contextual-tips, product-tour, tooltips-tour, feature-discovery, hotspots, permission-priming]
level: practitioner
status: draft
description: "Design coach marks and permission priming: behaviour-triggered tips, one idea each, dismissible, and a pre-permission screen that explains value before the OS prompt."
sources:
  - "Nielsen Norman Group - Onboarding Tutorials vs. Contextual Help and Permission Requests (nngroup.com/articles/permission-requests)"
  - "Apple Human Interface Guidelines - Privacy and Requesting permission (developer.apple.com/design/human-interface-guidelines/privacy)"
  - "Android Developers - Request runtime permissions (developer.android.com/training/permissions/requesting)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Coach marks and permission priming

## Coach marks (contextual tips)
**Goal:** teach a feature at the moment it matters, not in a front-loaded tour.
1. **Trigger by context:** after the user reaches the relevant screen, or after completing prerequisite actions; not on first launch for everything.
2. **One idea per tip,** pointing at the element (arrow, spotlight), title and one sentence, a clear action ("Try it") and Dismiss. Limit tours to 3-5 steps; allow skip and replay from Help.
3. **Do not block the interface** unless the step requires interaction; never cover the element being explained; prefer interactive steps ("Click here") over passive reading.
4. **Persist state:** show once, do not repeat after dismissal; avoid tips for features the user already used.
5. **Accessibility:** focus moves into the tip, Esc dismisses, content announced; do not use only a colour highlight.
6. Measure feature adoption and dismissal rates; retire tips that nobody benefits from.

## Permission priming
**Goal:** raise the grant rate for system permissions (notifications, location, camera, tracking) without wasting the one-shot OS prompt.
- iOS shows the system alert once; a denial needs a trip to Settings. Android 11+ offers "only this time"; repeated denials block the dialog.
1. **Ask in context,** when the user takes an action that needs it (tap "Scan"), not at launch.
2. **Pre-permission screen (priming):** explain the benefit in their terms ("Get alerts when your parcel is arriving"), with "Continue" (then the OS prompt) and "Not now" (no OS prompt consumed).
3. **Provide a purpose string** (`NSLocationWhenInUseUsageDescription`, Info.plist) that is specific.
4. **Handle denial gracefully:** keep working with reduced function; explain how to enable in Settings, with a deep link.
5. **Request the minimum** (approximate location when enough).

## Verify
- [ ] Tips appear in context, are skippable, one idea each, and not repeated.
- [ ] Permissions requested in context with a priming screen; denial handled.
