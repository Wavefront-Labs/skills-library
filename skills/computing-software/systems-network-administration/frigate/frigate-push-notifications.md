---
id: computing-software.systems-network-administration.frigate.frigate-push-notifications
name: frigate-push-notifications
category: computing-software
field: systems-network-administration
product: frigate
tags: [webpush-notifications, notification-cooldown, device-registration, notification-ttl, notification-browser-support]
level: practitioner
status: docs-checked
description: "Enable Frigate's WebPush notifications for review alerts, set cooldowns, register devices over the authenticated port and tune latency."
sources: ["https://docs.frigate.video/configuration/notifications/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Frigate push notifications

Frigate sends native notifications using the WebPush protocol with VAPID, so the Frigate server needs internet access to the browser vendor's push service (for example Google FCM or Mozilla autopush). Only review alerts trigger notifications.

Requirements:
- Frigate accessed over `https` while signed in as a Frigate user.
- A supported browser: Chrome, Firefox and Safari are known to work. Only Chrome shows images in notifications; the others show a title and message. For iOS some users also had to enable Notifications under Settings, Apps, Safari, Advanced, Features.
- Frigate reachable externally if you want notifications away from home.

Configuration: `notifications.enabled: True`, `email` (your address) and `cooldown` in seconds (for example 10). Per-camera overrides live under `cameras.<name>.notifications` with their own `enabled` and `cooldown` (for example 30). A notification is blocked if either the global cooldown since any camera's last notification, or the camera-specific cooldown, has not elapsed.

Registration: after enabling, press Register This Device on each device that should receive them, then restart Frigate. Registration is bound to the signed-in Frigate user, so register through the authenticated port `8971`; reverse proxies and tunnels should point at 8971.

Latency: alerts are sent with a `ttl` of `immediate`, so an unreachable device (asleep, switching networks, weak signal) misses them. `notifications.ttl: reliable` retries for up to 30 seconds, at the cost of a late notification possibly describing an object that has already left.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/notifications (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
