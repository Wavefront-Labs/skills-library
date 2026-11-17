---
id: computing-software.general-digital-literacy.web-browsers.browser-performance-and-energy-saver
name: browser-performance-and-energy-saver
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-settings, energy-saver, efficiency-mode, battery-life]
level: intro
status: docs-checked
description: "Use Chrome Energy Saver and Edge energy saver to extend laptop battery, choose when they run, and exclude sites that misbehave when throttled."
sources:
  - https://support.google.com/chrome/answer/12929150
  - https://support.microsoft.com/en-gb/topic/learn-about-performance-features-in-microsoft-edge-7b36f363-2119-448a-8de6-375cfd88ab25
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Performance and energy saver

## Chrome
- More > Settings > **Performance** > Energy Saver. It works automatically when the device is unplugged or the battery is low, and does not turn on when plugged in. Chrome reduces its image capture rate and stops eligible CPU-intensive background tabs; tabs in video calls or playing audio are not affected.
- Available on Windows, Mac and Chromebook devices with a battery. Chrome warns gaming and video performance may change.
- To keep background tabs active for one session, use the address-bar Energy Saver button > **Turn off now**.
- **Memory Saver** is on the same page (Moderate, Balanced or Maximum) and deactivates tabs you are not using.

## Edge
Microsoft calls the feature **energy saver** (formerly efficiency mode): Settings and more > Settings > System and performance > Performance.
- It becomes active when the device is unplugged and stays active until plugged in. To use it while plugged in, enable "Use energy saver even when connected to power".
- **Balanced** (recommended) takes moderate steps on battery and more when battery is low; **Maximum** takes the extra steps the whole time unplugged. Either may make videos less smooth.
- Background tabs sleep after 30 minutes of inactivity on moderate steps (when Automatically put tabs to sleep is on) and after five minutes with maximum savings.
- Exclude sites you never want affected (Microsoft suggests browser games) in the same settings area.
- Windows Task Manager also has a separate "Efficiency mode"; turning one off does not turn off the other.

## Verify
- [ ] The energy saver indicator shows when unplugged and a heavy site still works as needed.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Personalize Chrome performance" and Microsoft Support "Learn about performance features in Microsoft Edge", read in October 2026. Confirmed: Chrome path, behaviour, platforms and session override; Edge naming, path, Balanced and Maximum, sleep timings, plugged-in option, exclusions, Task Manager distinction. Removed as unconfirmed: the Chrome 20 percent battery threshold and leaf icon, Edge Startup boost, Firefox and Safari power tips.
Method: documentation only; no commands were run.
