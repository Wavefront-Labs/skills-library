---
id: computing-software.digital-privacy-hygiene.vpn-tools.signal-proxy-for-censorship
name: signal-proxy-for-censorship
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, signal-proxy, signal, bridges]
level: practitioner
status: docs-checked
description: "Connect to Signal where it's blocked using a Signal TLS proxy link, run your own proxy on a host you control, and know the risks of public proxies."
sources:
  - "https://github.com/signalapp/Signal-TLS-Proxy"
  - "https://signal.org/blog/help-iran-reconnect/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Signal proxy for censorship

**Goal:** keep using Signal on a network or in a country that blocks it.

## Using a proxy
- Tap a `https://signal.tube/#<proxy-host>` link from another app and Signal configures proxy support
  automatically. Signal's blog says this happens before any web request is made, so blocking that domain does not
  stop it.
- Or enter the proxy information manually in Signal's settings (exact menu names vary by version; check the app).
- The Signal client makes an ordinary TLS connection to the proxy, which forwards the bytes to the Signal service
  and blocks non-Signal traffic. Signal's end-to-end encryption and its TLS session to Signal both continue
  through the tunnel, so traffic is opaque to the proxy operator.

## Running one for others
From the Signal-TLS-Proxy README you need a host with ports 80 and 443 available and a domain name pointing at it.
1. Install Docker.
2. Clone the repository.
3. Run the certificate script in the repository (`./init-certificate.sh`).
4. Run `docker compose up --detach`.
Share it as `https://signal.tube/#<your_host_name>`. Signal's blog says an inexpensive small VPS can handle
hundreds of concurrent users.

Operators should check for updates at least every thirty days (git pull, docker compose down, build, up); Signal
aims to publish required changes thirty days ahead but may not always manage.

## Gotchas
- Posting a `signal.tube` link publicly, or a server becoming too popular, raises the chance that censors add its
  IP addresses to a block list. Share links privately.
- A proxy sees your IP address and connection to it, even though it cannot read content (the IP point is an
  inference from how proxies work; the cited pages do not state it).

## Checked
Method: docs-checked 2026-11-09 against the Signal-TLS-Proxy README (read in full) and the Signal blog post "Help Iran reconnect" (read from the downloaded HTML). Dropped as unconfirmed: the Settings menu path, the Let's Encrypt statement, the VPN/Tor/Orbot alternatives, the built-in censorship-circumvention setting, and the SMS-registration gotcha. The script name was corrected from init-certificates.sh to init-certificate.sh. support.signal.org could not be read and was removed.
