---
id: computing-software.digital-privacy-hygiene.device-hardening.reading-the-ios-app-privacy-report
name: reading-the-ios-app-privacy-report
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, app-privacy-report, app-permissions, ios, tracking-domains, app-tracking-transparency]
level: practitioner
status: draft
description: "Turn on and read the iPhone App Privacy Report to see which apps used sensors and data and which tracking domains they contacted, then cut access."
sources:
  - "https://support.apple.com/guide/iphone/welcome/ios"
  - "https://developer.apple.com/documentation/network/inspecting_app_activity_data"
  - "https://ssd.eff.org/module/how-to-get-to-know-iphone-privacy-and-security-settings"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading the iOS App Privacy Report

**Goal:** see what apps actually do, not what their privacy label claims.

## Turn it on
Settings > Privacy & Security > **App Privacy Report** > Turn On App Privacy Report (iOS 15.2+). It records
7 days of activity; come back after normal use. Turning it off deletes the history.

## Sections
- **Data & Sensor Access**: which apps touched Location, Photos, Camera, Microphone, Contacts, and when.
  Look for access at times you were not using the app.
- **App Network Activity**: domains each app contacted. Third-party analytics/ad domains show up here
  (for example Firebase `app-measurement.com`, `graph.facebook.com`, ad exchanges).
- **Website Network Activity**: domains contacted by sites loaded in apps and in-app browsers.
- **Most Contacted Domains**: overall tracker heavy hitters.

## Export for analysis
Tap the share icon (top right) > **Save App Activity**: an NDJSON file. Each line has `type` (`access` or
`networkActivity`), `bundleID`, `domain`, `timeStamp`. Quick count with Python:
```python
import json, collections
c = collections.Counter(json.loads(l).get("domain") for l in open("App_Privacy_Report.ndjson"))
print(c.most_common(30))
```

## Act on it
- Revoke permissions per app (Settings > app name) or switch Location to **While Using** and Precise Location off.
- Settings > Privacy & Security > Tracking > **Allow Apps to Request to Track** off (blanket ATT denial).
- Delete apps contacting many ad/analytics domains if an alternative exists; browsers with blockers cut website
  tracking.

## Gotchas
- A domain listed is not proof of data theft; many are CDNs or crash reporting. Judge by pattern and vendor.
- It does not cover traffic through system services or VPN apps' own tunnels in detail.

## Verify
- [ ] Report enabled for a week, reviewed, and at least the sensor anomalies resolved.
