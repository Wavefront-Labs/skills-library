---
id: computing-software.digital-privacy-hygiene.privacy-configuration.ios-system-services-location
name: ios-system-services-location
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, system-services-location, location-services, significant-locations]
level: practitioner
status: docs-checked
description: "Review iPhone Location Services and System Services: significant locations, iPhone Analytics, suggestions, the status bar arrow, and what to keep for Find My and emergencies."
sources:
  - "https://support.apple.com/en-us/102515"
  - "https://support.apple.com/guide/iphone/control-the-location-information-you-share-iph3dd5f9be/ios"
  - "https://www.apple.com/legal/privacy/data/en/device-analytics/"
  - "https://www.apple.com/legal/privacy/data/en/ask-siri-dictation/"
  - "https://ssd.eff.org/module/how-to-get-to-know-iphone-privacy-and-security-settings"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# iOS System Services location

**Goal:** Apple's own background location use matches what you want, not just third-party apps. Apple's pages do not
describe every System Services entry, so this skill lists only what the cited pages state; read each toggle's own
description on the device.

## Where
Settings > Privacy & Security > Location Services > scroll to the bottom > **System Services**. There you can see each
service's status, turn each on or off, and choose to **show in the status bar** when enabled system services use your
location (Apple's iPhone guide). Per Apple 102515, a black or white arrow in the status bar or Control Center shows an app is using
Location Services.

## What the sources say about specific services
| Service | What is documented |
|---|---|
| Find My iPhone | EFF: needed for specific services such as finding or wiping a lost phone; keep on if you want that |
| Significant Locations | EFF: stores the locations you go to most often; consider turning it off. Stolen Device Protection's "Away from Familiar Locations" option stops working if it is off |
| iPhone Analytics | Apple: turn it off to stop analytics location data (location of calls ending, signal strength) being sent |
| Suggestions & Search | EFF: may not be critical; Apple's Siri page also lists it as the control for suggestions location |

Per-app choices: Apple (102515) describes While In Use and Allow Once; EFF lists Never, Ask Next Time or When I Share,
While Using and Always, and says turning Precise Location off gives an app only your general location.

## Other facts worth knowing
- With an app set to While In Use, background use shows a blue pill in the status bar, and iOS reminds you from time to
  time about apps using location in the background.
- Emergency calls: Apple says location may be used when you place an emergency call whether or not Location Services
  is on.
- Wi-Fi hotspot owners can opt an access point out of Apple's crowd-sourced database by ending the network name with
  "_nomap" (not effective on hidden networks).
- Settings > General > Transfer or Reset [device] > Reset > **Reset Location & Privacy** returns all location and
  privacy settings to defaults; apps stop using location until you grant it again.
- Turning Location Services off limits the performance of many Apple and third-party apps.

## Checked
Checked 2026-11-08 against the full text of Apple Support 102515 ("About privacy and Location Services"), the iPhone
User Guide page "Control the location information you share", Apple's "Device Analytics & Privacy" and "Siri,
Dictation & Privacy" pages, and the EFF iPhone settings guide. Removed the recommendation table: no cited page names
Location-Based Alerts, Location-Based Apple Ads, Routing & Traffic, Improve Maps, Popular Near Me, Networking &
Wireless or Setting time zone, nor the Significant Locations encryption claim, so those rows and the "Product
Improvement" section are gone. The Personal Safety guide link redirected to a contents page and was dropped.
Method: documentation only; no commands were run.
