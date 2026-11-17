---
id: computing-software.ai-ml-engineering.open-webui.nginx-lets-encrypt-docker
name: nginx-lets-encrypt-docker
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [https-nginx, nginx, lets-encrypt, certbot, docker-compose, tls]
level: practitioner
status: docs-checked
description: "Put Open WebUI behind a dockerised Nginx with a Let's Encrypt certificate obtained by a two-phase certbot webroot flow, plus automatic renewal."
sources:
  - https://docs.openwebui.com/reference/https/nginx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: trusted HTTPS for Open WebUI via Nginx + certbot in Docker. Needs a real domain with an `A` record to the server (Let's Encrypt cannot issue for IPs), Docker and Docker Compose.

## Phase 1: validation
1. `mkdir -p nginx/conf.d ssl/certbot/conf ssl/certbot/www`
2. Temporary `nginx/conf.d/open-webui.conf`: `listen 80; listen [::]:80; server_name <YOUR_DOMAIN_NAME>;` with `location /.well-known/acme-challenge/ { root /var/www/certbot; }` and `location / { return 404; }`.
3. Add to `docker-compose.yml`: service `nginx` (`nginx:alpine`, ports `80:80` and `443:443`, volumes `./nginx/conf.d` mounted at `/etc/nginx/conf.d`, `./ssl/certbot/conf:/etc/letsencrypt`, `./ssl/certbot/www:/var/www/certbot`, `depends_on: open-webui`, network `open-webui-network`). Put `open-webui` on the same bridge network and use `expose: [8080]` instead of publishing ports.
4. Script `enable_letsencrypt.sh` (chmod +x): `docker compose up -d nginx`, then
```bash
docker run --rm -v "./ssl/certbot/conf:/etc/letsencrypt" -v "./ssl/certbot/www:/var/www/certbot" \
  certbot/certbot certonly --webroot --webroot-path=/var/www/certbot \
  --email "$EMAIL" --agree-tos --no-eff-email --force-renewal -d "$DOMAIN"
```
then `docker compose stop nginx`; on failure stop nginx and exit 1.

## Phase 2: final config
Replace `open-webui.conf` (replace all 4 domain placeholders): port 80 server keeps the acme-challenge location and returns `301 https://$host$request_uri`. The 443 server uses `listen 443 ssl; listen [::]:443 ssl; http2 on;`, `ssl_certificate /etc/letsencrypt/live/<DOMAIN>/fullchain.pem`, `ssl_certificate_key .../privkey.pem`, `ssl_protocols TLSv1.2 TLSv1.3`. Locations:
- `~* ^/(auth|api|oauth|admin|signin|signup|signout|login|logout|sso)/`: `proxy_pass http://open-webui:8080;` HTTP/1.1, Upgrade/Connection headers, `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`, `proxy_read_timeout 10m`, `proxy_buffering off`, `proxy_cache off`, `client_max_body_size 20M`, `proxy_no_cache 1`, `proxy_cache_bypass 1`, `Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0"`, `expires -1`.
- profile image regex location: `expires 1d`.
- static extensions (`css|jpg|...|eot`): `expires 7d`, `Cache-Control "public, immutable"`.
- `/`: same proxy headers, `proxy_read_timeout`/`send`/`connect` 1800, buffering and cache off, `client_max_body_size 20M`.
Then `docker compose up -d` and browse to `https://<YOUR_DOMAIN_NAME>`.

## Renewal (certificates last 90 days)
`sudo crontab -e`, daily at 03:30:
```cron
30 3 * * * /usr/bin/docker run --rm -v "<absolute_path>/ssl/certbot/conf:/etc/letsencrypt" -v "<absolute_path>/ssl/certbot/www:/var/www/certbot" certbot/certbot renew --quiet --webroot --webroot-path=/var/www/certbot --deploy-hook "/usr/bin/docker compose -f <absolute_path>/docker-compose.yml restart nginx"
```

## Gotchas
- Set `CORS_ALLOW_ORIGIN` to the public URL or WebSockets fail.
- Never cache auth/API paths (see the nginx streaming skill).

## Checked
2026-11-04. Confirmed against the Open WebUI docs page reference/https/nginx, including its Let's Encrypt tab content (reference/tab-nginx/LetsEncrypt, read in full) and the CORS_ALLOW_ORIGIN and no-cache warnings on the page: prerequisites and the no-IP rule, the directory layout, the temporary port 80 config, the nginx and open-webui Compose changes, the enable_letsencrypt.sh flow and its failure path, the final redirect and TLS server blocks, all four location blocks with their timeouts, caching headers and 20M limit, the docker compose up step, the 90 day expiry and the daily 03:30 cron renewal with deploy hook. Nothing removed.
Method: documentation only; no commands were run.
