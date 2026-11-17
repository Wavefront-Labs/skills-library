---
id: computing-software.digital-privacy-hygiene.privacy-configuration.google-location-accuracy-setting
name: google-location-accuracy-setting
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, google-location-accuracy, android-location, wifi-scanning, location-services]
level: practitioner
status: docs-checked
description: "Decide whether to keep Android's Google Location Accuracy on, what Google says it collects, and how app permissions, Timeline and IP address also reveal location."
sources:
  - "https://policies.google.com/technologies/location-data"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Google Location Accuracy

**Goal:** understand the trade between a faster, more accurate location fix and Google collecting location signals from
your phone. Source: Google's "How Google uses location information" page. It does not give menu paths, so look in
your Android device's location settings for the Google Location Accuracy (GLA, also called Google Location Services)
switch; labels differ by maker and Android version.

## What it is
Android estimates location from GPS, sensors (accelerometer, gyroscope, magnetometer, barometer), mobile network
signals and Wi-Fi signals. Mobile and Wi-Fi signals help most where GPS is poor, such as dense urban areas or indoors.
When GLA is on, Google says it periodically collects location information from the device (GPS, Wi-Fi access point
information, mobile networks, sensors) using a temporary rotating device identifier not associated with a specific
person, to improve accuracy and to build crowdsourced maps of Wi-Fi access points and mobile network towers.

## Off vs on
| | On | Off |
|---|---|---|
| Method | GPS, sensors, plus mobile and Wi-Fi signals | Only GPS and device sensors |
| Data to Google | Periodic collection as described above | Not through GLA |
| Accuracy | Better where GPS is weak (cities, indoors) | Location still works, may be less accurate there |

You can turn GLA off at any time; Google states location keeps working without it.

## Other ways Google learns your location
- **IP address:** gives a general area to any site or service you use.
- **Saved activity:** with Web & App Activity or Search Services History on, activity can include the general area; manage
  it in My Activity.
- **Timeline:** off by default; when on, precise device locations are regularly saved to your account, even when
  Google apps are closed, and can be auto-deleted after 3, 18 or 36 months or kept until you delete them. Turning it
  off keeps past data until deleted and does not change other location-saving controls.
- **Saved home or work addresses:** used for directions and ads purposes; editable or deletable in your Google Account.
- **App permissions:** Android lets you choose precise or approximate location, and anytime, only while in use, ask
  every time, or never (availability depends on Android version). Some apps, such as Find My Device, need background
  location.

## Recommendation
Keep GLA on if accurate indoor and urban location matters more to you; turn it off if you prefer not to send these
signals to Google, then review app permissions either way.

## Checked
Checked 2026-11-08 against the full text of Google's location-data page. Removed what it does not state: the Settings
menu path, Wi-Fi and Bluetooth scanning switches, the Emergency Location Service advice, the Timeline-on-device note,
the GrapheneOS remark and the ride-hailing example. The support.google.com/android link is a stub and was dropped.
Method: documentation only; no commands were run.
