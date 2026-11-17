---
id: computing-software.firmware-embedded-development.esphome.esphome-web-server
name: esphome-web-server
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, web-server, rest-api, http-auth, css-include, js-include, offline-web-ui, mdns]
level: practitioner
status: docs-checked
description: "Enable and configure the ESPHome web_server component: port, offline CSS and JS, HTTP authentication, and the web UI versions and memory cost."
sources: ["https://esphome.io/components/web_server/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome web server

`web_server` runs a small web server on the node reachable from any browser, plus a simple REST API. It uses less flash than older releases and is much cheaper to include, including on the ESP8266, but each connected client uses memory, so check free heap when combining it with many other features on small boards. There are three UI versions (1, 2 and 3).

Access it by the node's IP address or `<node_name>.local/` via mDNS (note the trailing slash).

Options:
- `port`: the socket port.
- `css_url` and `js_url`: external assets, defaulting to the `oi.esphome.io` v1 stylesheet and script; either can be set to an empty string.
- `css_include` and `js_include`: local files served from the device as `/0.css` and `/0.js`. Use these for builds that must work without internet access, for example with the built-in access point and web server.
- `auth` with `username` and `password` (both required) enables HTTP authentication; `type` selects the scheme. `basic` is the default and sends the password in an easily reversible Base64 form on every request; `digest` sends only hashes and is the recommended scheme (the page says the default will change to `digest` in ESPHome 2027.1.0).

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/web_server/ (fetched this batch). Removed an unsourced closing tip; added the documented `digest` auth scheme.

Method: documentation only; no commands were run.
