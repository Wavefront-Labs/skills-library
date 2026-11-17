---
id: computing-software.systems-network-administration.apache-guacamole.rdp-gateway-and-session
name: rdp-gateway-and-session
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, rdp, rd-gateway, gateway-hostname, initial-program, server-layout, timezone, console-session, load-balance-info, connection-broker]
level: practitioner
status: draft
description: "Guacamole RDP gateway parameters and session basics: initial-program, client-name, server-layout, timezone, enable-touch, console, and load-balance-info for connection brokers."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDP: gateway, session basics, brokers

Remote Desktop Gateway:
| Parameter | Default |
|---|---|
| `gateway-hostname` | none (no gateway) |
| `gateway-port` | 443 |
| `gateway-username`, `gateway-password`, `gateway-domain` | none; may differ from session credentials |

Session basics:
- `initial-program`: full path of a program to launch on connect.
- `client-name`: overrides the name sent to the server (becomes `CLIENTNAME` on Windows); default is Guacamole's hostname.
- `server-layout`: default `en-us-qwerty`; others e.g. `en-gb-qwerty`, `de-de-qwertz`, `fr-fr-azerty`, `ja-jp-qwerty`, `sv-se-qwerty`; `failsafe` exists but may break shortcuts. Set it to match the server's layout if typed characters are wrong.
- `timezone`: IANA name (`Europe/Berlin`); default detected from the client; server support varies.
- `enable-touch=true`: multi-touch via RDPEI.
- `console=true`: connect to the console (admin) session; `console-audio=true` adds audio there.

Connection brokers:
- `load-balance-info`: cookie/string required by the broker; look for `loadbalanceinfo` in the broker's `.rdp` files. Leave blank otherwise.
- Redirecting servers often need `security=tls` (apache-guacamole.rdp-network-security).

Verify: keystrokes produce the expected characters and the gateway-routed session reaches the target.
