---
id: computing-software.digital-privacy-hygiene.privacy-configuration.turning-off-smart-tv-acr-tracking
name: turning-off-smart-tv-acr-tracking
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, smart-tv-acr, ad-tracking-controls, automatic-content-recognition, samsung-viewing-information, lg-live-plus, roku-privacy, vizio-viewing-data, google-tv, smart-home]
level: intro
status: docs-checked
description: "Disable automatic content recognition (ACR) and ad tracking on Samsung, LG, Roku, Vizio, Sony, Google TV and Fire TV, per Consumer Reports' 2025 guide."
sources:
  - "https://www.consumerreports.org/electronics/privacy/how-to-turn-off-smart-tv-snooping-features-a4840102036/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Turning off smart TV ACR tracking

**Goal:** automatic content recognition (ACR) tries to identify every show you watch, including programmes from cable,
over-the-air broadcasts, streaming services and Blu-ray discs. The data can be used for recommendations, for targeting
ads to you and your family and for other purposes, and it is not always easy to review or delete later. Consumer
Reports says you cannot stop all data collection, but turning off ACR reduces it. Vizio came under federal and state
regulator scrutiny in 2017 for collecting such data without users' knowledge or consent.

## Menus (names change by year and model; check your own set)
| Platform | Where and what to turn off |
|---|---|
| Samsung (Tizen), 2025 | Home > Menu > Settings > All Settings > General & Privacy > Terms & Privacy: untick **Viewing Information Services** (Samsung's ACR) and Interest-Based Advertisements. Privacy Choices has a Do Not Sell or Share My Personal Information option. Voice is under Settings > All Settings > Advanced Features > Voice and may be greyed out until the microphone switch under the TV is on |
| LG (webOS), new sets | Settings > All Settings > Support > Privacy & Terms: User Agreements > **Viewing Information** (powers Live Plus ACR; LG says ACR applies only if the TV has Live Plus), plus Voice Information, Interest-Based Cross-Device Advertising and "Who. Where. What?". There is also a Do Not Sell My Personal Information toggle. These agreements were off by default during setup |
| Roku TV | Settings > Privacy: Smart TV Experience > untick **Use Info from TV Inputs** (disables ACR; also switches off Enable Auto Notifications). Advertising > untick Personalize Ads to reset the advertising ID. Privacy Choices lets you opt out of sale or sharing |
| Vizio (SmartCast) | Settings > All Settings > Admin & Privacy: **Viewing Data** is Vizio's ACR. Activity Data is separate and stays on when Viewing Data is off. Older sets use System > Reset & Admin, or Smart Interactivity |
| Google TV | Settings > Privacy > Ads: reset or delete the advertising ID. Google says the platform itself does not use ACR, but individual TV brands may, with their own agreements. Google's privacy policy cannot be declined if you want smart features |
| Amazon Fire TV Edition | Settings > Preferences > Privacy Settings: Device Usage Data, Collect App and Over-the-Air Usage, Interest-Based Ads (all on by default), plus a reset for the advertising ID and, new for 2025, Manage Sharing From Apps. Amazon says it does not use ACR on non-Amazon devices connected to the TV. Older sets may use Applications instead of Preferences |
| Sony (Google TV) | Settings > All Settings, just below Privacy: **Samba Interactive TV** toggle (Samba TV supplies Sony's ACR). The setup Bravia policy options (Provide Sony Smart TV Features, Provide Program Recommendations, Perform Product Improvements, Share TV Data) are off by default |

TCL Google TVs also carry the brand's own Terms & Privacy agreements: you can opt out of the User Experience
Improvement Program and diagnostic collection, and withdraw consent under Settings > Privacy > User Agreements.

## Other limits to know
- Turning off Fire TV usage collection does not affect data about your use of Amazon services such as Prime Video.
- Turning off Roku's Use Info from TV Inputs limits tracking of antenna and connected-device viewing, but Roku may
  still collect data about the apps or services you use.
- Declining some terms stops smart features: on Vizio, declining Activity Data means no SmartCast streaming.
- Resetting the advertising ID periodically can reduce tracking.

## Stronger option
Keep the TV off the network and use a streaming device or console you control. Network-level blocking is not covered
by the cited guide, so test any DNS filtering yourself.

## Verify
- [ ] ACR/viewing data and ad personalisation settings are off on every TV, rechecked after firmware updates or resets.

## Checked
Checked 2026-11-08 against the Consumer Reports guide "How to Turn Off Smart TV Snooping Features" (updated 19 October
2025): menu paths and setting names for each platform, ACR definition, and the 2017 Vizio scrutiny. Removed: the
claim that the FTC fined Vizio (the FTC page returned 403; the guide says only regulator scrutiny), the stated Roku
"Limit ad tracking", Samsung "Support/General" and LG "Limit Ad Tracking" wording not in the guide, the Google TV
"Usage and diagnostics off" step, and the DNS blocking and isolated-network advice, none of which the pages state.
Method: docs-only read of cited pages, 2026-11-08
