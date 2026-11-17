---
id: computing-software.systems-network-administration.frigate.frigate-home-assistant-integration
name: frigate-home-assistant-integration
category: computing-software
field: systems-network-administration
product: frigate
tags: [home-assistant-integration, hacs, integration-url, rtsp-url-template, notification-api, media-browser, cast-clips]
level: practitioner
status: docs-checked
description: "Install and configure the Frigate Home Assistant integration through HACS, choose the right Frigate URL and port, and use its entities and notification endpoints."
sources: ["https://docs.frigate.video/integrations/home-assistant/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Frigate Home Assistant integration

Prerequisites: a running Frigate, the Home Assistant `mqtt` integration configured, and MQTT enabled in Frigate's config (`mqtt.enabled`, `host`, `user`, `password`) pointing at the same broker. Install via HACS (search "Frigate", a default repository), restart Home Assistant, then add the Frigate integration under Devices and Services. `media_source` must be enabled for the Media Browser. The optional Lovelace card is a separate project.

URL to enter: the internal unauthenticated `5000` or the authenticated `8971`.
- Same Compose file, Home Assistant on host networking: `http://172.17.0.1:5000` (binding `172.17.0.1:5000:5000`); host networking for Frigate is not recommended.
- Without host networking: the authenticated `http://frigate:8971`, with no port mapping needed.
- Home Assistant App: `http://ccab4aaf-frigate:5000` (variant names differ for Full Access and Beta); do not point at the proxy app's URL.
- Separate machine: `http://<frigate_ip>:8971` with TLS disabled, because Home Assistant fails against the default self-signed certificate; otherwise install a valid certificate.
- Tailscale: `http://<tailscale_ip>:5000`.

Live camera streams need the RTSP port `8554` reachable from Home Assistant. For reverse proxies or firewalls, the advanced RTSP URL Template option accepts a jinja2 template using the Frigate camera dict only.

Entities: `camera`, `image` (latest detected object), `sensor` (performance and object counts), `switch` (detection, recordings, snapshots) and `binary_sensor` (motion and occupancy). The Media Browser covers recordings and snapshots. Casting clips needs audio enabled in recordings. Camera turn_on and turn_off actions toggle runtime state and do not persist across restarts.

Because many people do not expose Frigate, the integration adds notification endpoints under `https://HA_URL/api/frigate/notifications/<event-id>/` such as `thumbnail.jpg`, `snapshot.jpg`, `clip.mp4` (Android), `master.m3u8` (iOS) and `event_preview.gif`.

## Checked

2026-11-04. Confirmed against the Home Assistant Integration page: mqtt prerequisites, HACS default repository, media_source, optional Lovelace card, connection URLs for each setup (host networking, separate compose, App variants, separate machine with TLS note, Tailscale), RTSP port 8554 and URL template, entity platforms, Media Browser, casting audio note, camera turn_on/turn_off not persisting, and notification endpoints. Removed the cross-origin live-stream claim (not on the page).
Method: documentation only; no commands were run.
