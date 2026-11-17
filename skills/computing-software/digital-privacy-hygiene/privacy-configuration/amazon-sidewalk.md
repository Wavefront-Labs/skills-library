---
id: computing-software.digital-privacy-hygiene.privacy-configuration.amazon-sidewalk
name: amazon-sidewalk
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, amazon-sidewalk, smart-home, wifi-bluetooth-scanning]
level: practitioner
status: docs-checked
description: "Decide whether to share your Echo or Ring device's bandwidth with Amazon Sidewalk, turn it off in the Alexa and Ring apps, and understand the privacy model."
sources:
  - "https://www.amazon.com/Amazon-Sidewalk/b?node=21328123011"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Amazon Sidewalk

**Goal:** a deliberate choice about whether your smart devices act as neighbourhood network bridges.

## What it is
Sidewalk is a community wireless network. Compatible Echo and Ring devices act as **Sidewalk Bridges** and share a
small, capped amount of your home internet bandwidth so nearby Sidewalk devices (such as the Ring Mailbox sensor)
stay connected. Amazon says it is currently available only in the US, and that your own Ring devices are not
affected by the cap.

## Turn it off
- **Ring app:** Control Center.
- **Alexa app:** Account Settings.
Amazon says the setting applies to all applicable Echo and Ring devices linked to the account.
Also look at **Community Finding**: it shares the approximate location of the bridge a Sidewalk device is near, to
help others find items; Amazon says neighbours cannot see where your bridge is, only the approximate location of
their own device.

## Privacy and security model (per Amazon)
Amazon says Sidewalk uses multiple layers of encryption and unique security keys, with content encrypted in a way
designed to prevent anyone, including Amazon, from reading it in transit. You are still trusting Amazon's
implementation and lending out part of your connection.

## Decide
| Keep on | Turn off |
|---|---|
| You use Sidewalk devices (mailbox sensors, trackers) | You don't use them; you prefer not to share bandwidth |
| You value neighbourhood coverage | Metered/slow connection |

## Checked
2026-11-01. Confirmed on the Amazon Sidewalk page and its FAQ: bridges, capped bandwidth, US-only availability,
off switch in Ring Control Center and Alexa Account Settings, account-wide effect, encryption statement, Community
Finding behaviour. Removed: the Kbps/MB figures, Bluetooth LE/LoRa radio names, default-on history, exact Alexa menu
path, re-prompt and "no effect on normal functions" claims (not stated on the pages read); the second cited help
page returned 404.
Method: documentation only; no commands were run.
