---
id: computing-software.ai-ml-engineering.open-webui.caddy-https-reverse-proxy
name: caddy-https-reverse-proxy
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [https-caddy, caddy, tls, security-headers, hsts, reverse-proxy]
level: practitioner
status: docs-checked
description: "Serve Open WebUI over automatic HTTPS with Caddy on Ubuntu, and optionally add proxy-layer security headers without duplicating app-level ones."
sources:
  - https://docs.openwebui.com/reference/https/caddy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: HTTPS with automatic certificate management in front of Open WebUI.

## Steps
1. Install Docker (apt repository; packages `docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`) and Caddy (Caddy's Debian/Ubuntu install guide).
2. In `~/open-webui/docker-compose.yml`:
```yaml
services:
    open-webui:
        image: ghcr.io/open-webui/open-webui:main
        container_name: open-webui
        ports:
            - "8080:8080"
        volumes:
            - ./data:/app/backend/data
        restart: unless-stopped
```
(env vars such as `QDRANT_API_KEY` and `QDRANT_URI` can go under `environment`.)
3. Edit `/etc/caddy/Caddyfile`:
```caddyfile
your-domain.com {
  reverse_proxy localhost:8080
}
```
4. DNS must already point to the server. `docker compose up -d`, then open `https://your-domain.com`. Caddy handles WebSocket upgrades and SSE streaming automatically.
5. Update: `docker rm -f open-webui`, `docker pull ghcr.io/open-webui/open-webui:main`, `docker compose up -d`; the bind-mounted `./data` keeps your data.

## Optional security headers at the proxy
Prefer app-level environment variables (`HSTS`, `XFRAME_OPTIONS`, `XCONTENT_TYPE`, `REFERRER_POLICY`, `PERMISSIONS_POLICY`, `CONTENT_SECURITY_POLICY`). Choose ONE layer only: duplicate CSP headers are intersected by browsers and duplicate HSTS/X-Frame-Options are ambiguous. If you set any via env vars, skip this.
```caddyfile
your.domain.example {
	header {
		Strict-Transport-Security "max-age=31536000; includeSubDomains"
		X-Frame-Options "DENY"
		X-Content-Type-Options "nosniff"
		Referrer-Policy "strict-origin-when-cross-origin"
		Permissions-Policy "camera=(), microphone=(), geolocation=()"
		-Server
	}
	reverse_proxy localhost:8080
}
```
Verify: `curl -sI https://your.domain.example | grep -E "Strict-Transport|X-Frame|X-Content|Referrer|Permissions"`.

## Gotchas
- HSTS is sticky: one year with `includeSubDomains` forces HTTPS on all subdomains and can only be undone by serving `max-age=0` and waiting for clients. Start with `max-age=300`. Do not add `preload` casually.
- If you use voice input or webcam, set `Permissions-Policy` directives to `(self)` rather than empty.
- No proxy-layer CSP is provided; set `CONTENT_SECURITY_POLICY`, and derive it with `CONTENT_SECURITY_POLICY_REPORT_ONLY`.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page reference/https/caddy (read in full): Docker packages, compose file, Caddyfile, DNS and compose up, update steps, the security-header block, the env var names, the choose-one-layer warning, HSTS stickiness, Permissions-Policy and CSP notes, and the verification curl. Removed: the WEBUI_URL and CORS_ALLOW_ORIGIN line, which the page does not state.
Method: documentation only; no commands were run.
