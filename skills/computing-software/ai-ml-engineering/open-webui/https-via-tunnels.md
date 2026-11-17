---
id: computing-software.ai-ml-engineering.open-webui.https-via-tunnels
name: https-via-tunnels
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [https-tunnels, cloudflare-tunnel, ngrok, tailscale, webui-url, cors]
level: practitioner
status: docs-checked
description: "Get HTTPS for Open WebUI without open ports using Cloudflare Tunnel, ngrok or Tailscale serve/funnel, and set WEBUI_URL and CORS_ALLOW_ORIGIN to match."
sources:
  - https://docs.openwebui.com/reference/https
  - https://docs.openwebui.com/reference/https/cloudflare-tunnel
  - https://docs.openwebui.com/reference/https/ngrok
  - https://docs.openwebui.com/reference/https/tailscale
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: HTTPS (needed for Voice Calls; browsers block microphone on non-HTTPS origins except localhost) with no certificate management. Assumes Open WebUI listens on port 8080.

Always set `WEBUI_URL` to the public HTTPS URL (OAuth callbacks, internal links) and `CORS_ALLOW_ORIGIN` to the same origin (otherwise WebSockets fail silently). Proxy buffering must be off for SSE, WebSocket `Upgrade` and `Connection` headers must pass, and read timeouts should be at least 300 s.

## Cloudflare Tunnel (recommended for production, domain must be on Cloudflare)
Dashboard path: Zero Trust > Networks > Connectors > Create a tunnel > Cloudflared, run the connector it shows, add a Public Hostname (subdomain `chat`, service type HTTP, URL `localhost:8080`); DNS is created automatically.

CLI path:
```bash
cloudflared tunnel login
cloudflared tunnel create open-webui
cloudflared tunnel route dns open-webui chat.your-domain.com
cloudflared tunnel run open-webui
```
`~/.cloudflared/config.yml`:
```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /path/to/YOUR_TUNNEL_ID.json
ingress:
  - hostname: chat.your-domain.com
    service: http://localhost:8080
  - service: http_status:404
```
Service on boot: `sudo cloudflared service install`, `sudo systemctl enable cloudflared`, `sudo systemctl start cloudflared`.

Compose variant: add a service `cloudflare/cloudflared:latest` with `command: tunnel --no-autoupdate run --token YOUR_TUNNEL_TOKEN` (token starts `eyJ...`, from the tunnel's "Add a replica" install command). The open-webui service needs no `ports`; set the tunnel service URL to `http://open-webui:8080`. Optional access gating: Zero Trust > Access controls > Applications, self-hosted app plus an Access Policy.

## ngrok (development and demos only)
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
ngrok http 8080
```
Output like `https://a1b2-203-0-113-42.ngrok-free.app`; run Open WebUI with `-e WEBUI_URL=` that URL. Free-tier URLs change on every restart (update `WEBUI_URL`), show an interstitial page and have rate limits. Paid: `ngrok http 8080 --url=your-name.ngrok-free.app`. Inspect traffic at `http://localhost:4040`.

## Tailscale (private across your devices)
1. `sudo tailscale up`; find the hostname (`my-server.tail1234.ts.net`) with `tailscale status`. Plain `http://my-server.tail1234.ts.net:8080` is already WireGuard-encrypted, but browser features that need HTTPS (Voice Calls) need the steps below.
2. Admin console > DNS > enable HTTPS Certificates.
3. `sudo tailscale serve https / http://localhost:8080` then browse `https://my-server.tail1234.ts.net` (no port). `sudo tailscale cert <host>` writes `.crt` and `.key` files if you need them.
4. Public exposure: `sudo tailscale funnel https / http://localhost:8080`. Warning: anyone on the internet can reach it, so configure authentication first.

## Gotcha
Tunnels fix the URL, not the app: after changing the public URL, update `WEBUI_URL` and `CORS_ALLOW_ORIGIN`.

## Checked
2026-11-04. Confirmed against the Open WebUI docs pages reference/https (index), reference/https/cloudflare-tunnel, reference/https/ngrok and reference/https/tailscale (all read in full): the Voice Calls HTTPS requirement, the key configuration notes (WEBUI_URL, CORS_ALLOW_ORIGIN, buffering off, Upgrade and Connection headers, 300s timeouts), the Cloudflare dashboard and CLI paths, config.yml, service install, the Compose token variant and Access policy steps, the ngrok commands, URL rotation, interstitial, rate limits, custom domain and local inspector, and the Tailscale up, status, HTTPS certificates, cert, serve and funnel steps with the Funnel warning. Reworded the Tailscale plain-HTTP sentence, which called it not a secure context; the page only says to continue for browser features that need HTTPS.
Method: documentation only; no commands were run.
