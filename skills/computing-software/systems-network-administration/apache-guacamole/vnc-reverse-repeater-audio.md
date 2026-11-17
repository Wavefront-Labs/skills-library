---
id: computing-software.systems-network-administration.apache-guacamole.vnc-reverse-repeater-audio
name: vnc-reverse-repeater-audio
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, vnc, reverse-connect, listen-timeout, vnc-repeater, dest-host, dest-port, pulseaudio, enable-audio, audio-servername]
level: advanced
status: docs-checked
description: "Guacamole VNC reverse connections (guacd listens), UltraVNC repeater dest-host/dest-port, and PulseAudio sound with enable-audio."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VNC reverse connect, repeater, audio

Reverse connection (server dials guacd):
- `reverse-connect=true`: guacd listens on `port` for the VNC server to connect in.
- `listen-timeout`: milliseconds to wait for the inbound connection; default 5000.
- `autoretry` then counts allowed listen timeouts.

Repeater (e.g. UltraVNC Repeater):
- `dest-host`, `dest-port`: destination behind the proxy; set only if the proxy requires it.

Audio via PulseAudio:
- `enable-audio=true` opens a second connection to PulseAudio (off by default).
- `audio-servername`: PulseAudio host; if omitted, guacd's local PulseAudio server is used.
- PulseAudio must allow anonymous TCP connections (`auth-anonymous=1`) or Guacamole cannot connect.

General parameters: apache-guacamole.vnc-connection-parameters.

Verify: the reverse connection establishes within the listen timeout, and sound plays in the browser after audio is enabled.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Guacamole manual Configuring Guacamole page: the VNC autoretry entry, VNC Repeater, Reverse VNC connections and Audio support (via PulseAudio) sections were read; other VNC sections were not. Confirmed: reverse-connect with guacd listening on the port, listen-timeout default 5000 ms, autoretry counting listen timeouts, dest-host and dest-port for proxies such as UltraVNC Repeater, enable-audio off by default with a second PulseAudio connection, audio-servername and the local-to-guacd default, and the strict auth-anonymous=1 requirement. Removed the firewall and listen-before-connect advice, which the page does not state.
