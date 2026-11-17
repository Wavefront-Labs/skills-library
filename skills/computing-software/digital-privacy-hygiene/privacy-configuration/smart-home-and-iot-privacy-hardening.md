---
id: computing-software.digital-privacy-hygiene.privacy-configuration.smart-home-and-iot-privacy-hardening
name: smart-home-and-iot-privacy-hardening
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, smart-home, iot, smart-speaker, smart-camera, voice-assistant, network-segmentation, guest-network, vlan, local-processing, home-assistant, matter, voice-recording-review, camera-privacy, firmware-updates-iot]
level: practitioner
status: draft
description: "Harden smart speakers, cameras and IoT devices: mic/camera cutoffs, voice-recording review and deletion, network segmentation, and local-only alternatives to cloud processing."
sources:
  - "https://www.ftc.gov/business-guidance/privacy-security/internet-things"
  - "https://www.home-assistant.io/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smart home and IoT privacy hardening

**Goal:** get the convenience of smart speakers, cameras and connected devices
without an always-listening microphone, an internet-exposed camera, or a vendor
retaining years of voice/video data you never reviewed — and contain any single
compromised gadget to its own slice of the network.

## 1. The core risk model for IoT specifically
Most smart-home devices: run infrequently updated firmware, are designed for
convenience over security by vendors who may not support them for long, and
have direct access to your home network once connected. A single compromised
smart plug or camera on a flat home network can be used to pivot toward your
computers and phone — the device doesn't need to be interesting on its own to
be a security problem.

## 2. Network segmentation — the single highest-leverage step
- Put **every** smart-home device on your router's **guest network** or a
  separate **VLAN**, isolated from your main devices (computers, phones storing
  financial apps and password managers). Most consumer routers now offer a
  guest network option in settings; some higher-end ones support proper VLANs.
- This means a compromised smart bulb cannot reach your laptop even if it's
  fully compromised — it's blast-radius containment, not a guarantee the device
  itself is safe.
- **Matter** (the newer cross-vendor smart-home standard) is designed with
  this kind of segmentation and local control in mind, but actual router/hub
  support and how well it enforces isolation varies by implementation — verify
  on your specific hardware rather than assuming the standard alone guarantees it.

## 3. Smart speakers and voice assistants
- **Physical mute switch** (most Amazon Echo and Google Nest devices have a
  hardware mic-off button, not just a software toggle) — use it during
  sensitive conversations; a hardware switch cannot be bypassed by a software
  compromise the way a settings toggle theoretically could.
- **Review and delete voice history**: Amazon (Alexa Privacy settings → Review
  Voice History), Google (myactivity.google.com → filter to Assistant), Apple
  (Siri requests are processed with on-device methods for much of the pipeline
  and Apple states it doesn't use audio recordings to build an advertising
  profile — policies and architectures do shift, check current documentation
  rather than relying on this staying accurate).
- **Disable "help improve" / human-review programs** where offered — several
  major voice assistants have had reporting in past years about human
  contractors reviewing snippets of voice recordings for quality purposes;
  opting out where the setting exists reduces exposure even if you keep the
  device.
- Consider **local-only voice assistants** (e.g. openWakeWord/Home Assistant
  Voice, Rhasspy) for a privacy-first setup — no cloud round-trip at all for
  wake-word and command processing, at the cost of more setup effort and
  reduced capability versus commercial assistants.

## 4. Cameras
- Prefer cameras with a **local recording option** (microSD card or local NVR)
  over cloud-only storage, or at minimum confirm you can delete cloud recordings
  and set a short retention window.
- **Never port-forward a camera directly to the internet** — use the vendor's
  app/cloud relay (accepting that trade-off) or a self-hosted solution (e.g.
  **Home Assistant** with a local camera integration, or Frigate for local
  AI-based detection) that doesn't require opening inbound ports.
- Physically cover or reposition any camera pointed at a space you don't want
  recorded when not actively monitoring (a laptop's own webcam cover habit
  applies here too, especially for indoor cameras with microphones).
- Change the camera's **default admin password** immediately — default
  credentials on IoT cameras are the single most common path to the
  mass-compromise botnets (Mirai and its many descendants) that scan the
  internet for exactly this.

## 5. Firmware and lifecycle
- Enable automatic firmware updates where offered; check the vendor's actual
  support/update history before buying a new device — cheap, little-known
  brands frequently stop patching within a year or two, after which a
  previously fine device becomes a standing risk.
- When a device reaches end of support, remove it from the network rather than
  leaving it running "because it still works" — this is the same end-of-support
  logic as `computing-software.digital-privacy-hygiene.device-hardening.personal-device-hardening-checklist`,
  applied to the device category least likely to get a nudge to replace it.

## Gotchas
- A software "mic off" toggle in an app is not the same guarantee as a
  hardware mute switch — prefer the hardware one when sensitivity matters.
- A device with no update history and a rock-bottom price on a marketplace is
  the typical profile of something that will never get a security patch.
- Uncertain: specific vendors' current voice/video retention policies and
  human-review programs change — re-check the current privacy policy for any
  device before assuming last year's settings still apply.

## Verify
- [ ] Every smart-home device lives on a guest network/VLAN separate from
      computers and phones.
- [ ] No camera is directly port-forwarded to the internet; default admin
      passwords changed on every IoT device.
- [ ] Voice history review/deletion and "help improve" opt-outs checked on each
      voice assistant in use.
- [ ] You know which devices in the home are past vendor support and have a
      plan to replace or remove them.
