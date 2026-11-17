---
id: computing-software.digital-privacy-hygiene.device-hardening.windows-app-permissions
name: windows-app-permissions
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, windows-app-permissions, app-permissions, windows-privacy]
level: practitioner
status: docs-checked
description: "Control which Windows apps can use your camera, microphone and location, including the separate toggle for desktop apps and where to see recent location use."
sources:
  - "https://support.microsoft.com/windows/windows-camera-microphone-and-privacy-a83257bc-e990-d54a-d212-b5e41beba857"
  - "https://support.microsoft.com/windows/windows-location-service-and-privacy-3a8eee0a-5b0b-dc07-eede-2a5ca1c49088"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows app permissions

**Goal:** only the apps you expect can use your camera, microphone and location on Windows.

## Camera and microphone
Settings > Privacy & security > **Camera** (or **Microphone**). Turn on or off:
- Camera access / Microphone access, and **Let apps access your camera / microphone**.
- The individual toggle for each Microsoft Store app.
- **Let desktop apps access your camera / microphone**: desktop apps cannot be toggled individually; this one switch
  controls them all.

## Location
Settings > Privacy & security > **Location**.
- **Location services** (administrators only) controls whether the location service can be used on the device.
- **Let apps access your location** controls it for just your user account; it cannot be turned on while Location services
  is off.
- Under Let apps access your location you can see the date and time location was last used by each app.
- Desktop apps do not ask for separate location permission and do not appear in the app list; control them with the
  desktop apps toggle on that page.
- If Location services is on and you are signed in with a Microsoft account, your location may be periodically saved in
  the cloud.

## Hardening
- Allow camera and microphone only for conferencing apps and the browser; turn off for the rest.
- Browsers have their own per-site permissions on top; review them too.

## Gotchas
- Turning off the desktop apps toggle blocks every classic app, including video-call apps, until re-enabled.
- These toggles are a privacy control, not a security boundary against software running with admin rights.

## Checked
2026-10-28. Confirmed on Microsoft Support (camera, microphone and privacy; location service and privacy): paths,
toggle names, desktop app behaviour, last-used timestamps, cloud-saved location. Removed (not confirmed): the "7 days"
recent activity view, the other App permissions categories list, taskbar indicator claims, Wi-Fi location side effect.
Method: documentation only; no commands were run.
