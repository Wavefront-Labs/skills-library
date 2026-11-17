---
id: computing-software.systems-network-administration.linux.web-server-nginx-apache
name: web-server-nginx-apache
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nginx, apache, httpd, apache2, vhost, virtual-host, reverse-proxy, server-block, tls, https, certbot, http2, proxy-pass, upstream, php-fpm, mod-ssl, htaccess, a2ensite, nginx-t, selinux-httpd, lpic-2, web-server, sysadmin, limit-req, location-blocks, access-log]
level: practitioner
status: docs-checked
description: "Serve sites with nginx or Apache httpd: name-based vhosts, TLS with certbot, reverse-proxying with correct headers, static/PHP serving, config test and reload, SELinux gotchas."
sources:
  - https://nginx.org/en/docs/
  - https://httpd.apache.org/docs/2.4/
  - https://ssl-config.mozilla.org/
  - https://eff-certbot.readthedocs.io/en/stable/
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Web serving with nginx and Apache — vhosts, TLS, and a correct reverse proxy

**Goal:** host several names on one box, terminate TLS properly, proxy to an app without
losing client IPs or breaking redirects, and reload without downtime.

## 1. nginx
```bash
dnf install nginx     # apt install nginx; config /etc/nginx/nginx.conf + conf.d/*.conf (RHEL) or sites-available/ + sites-enabled/ symlinks (Debian)
```
`/etc/nginx/conf.d/app.example.com.conf`:
```nginx
upstream app { server 127.0.0.1:8000; keepalive 32; }

server {
    listen 80;
    listen [::]:80;
    server_name app.example.com;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;                               # before 1.25.1: "listen 443 ssl http2;"
    server_name app.example.com;
    ssl_certificate     /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;   # or Mozilla "intermediate" settings
    add_header Strict-Transport-Security "max-age=63072000" always;
    client_max_body_size 50m;
    access_log /var/log/nginx/app.access.log;

    location /static/ { alias /srv/app/static/; expires 7d; }

    location / {
        proxy_pass http://app;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection        "";       # keepalive to upstream
        proxy_read_timeout 60s;
    }
    location /ws/ {                                   # websockets
        proxy_pass http://app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```
```bash
nginx -t && systemctl reload nginx      # reload = zero-downtime; restart drops connections
nginx -T | grep -A3 server_name          # dump the effective merged config
```
- A `default_server` catch-all (`server_name _; return 444;`) stops random hostnames
  landing on your first vhost. Without it, nginx uses the first `server` block for the port.
- `root` vs `alias`: `location /static/ { root /srv/app; }` serves `/srv/app/static/x`;
  `alias /srv/app/static/;` strips the prefix. Trailing slashes must match.
- `proxy_pass http://app/` (with a URI) rewrites the path; without one it passes it through.
- 502 = upstream refused (app down, wrong port, or an SELinux denial: check the audit log).
  504 = upstream too slow (`proxy_read_timeout`). 413 = `client_max_body_size`.
- Serving files from `/home` or `/srv`: nginx user (`nginx`/`www-data`) needs `x` on every
  parent dir; on SELinux hosts the files also need a web-content label (check the audit log for denials).
- PHP: `fastcgi_pass unix:/run/php-fpm/www.sock;` with `include fastcgi_params;` and
  `fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;`.
- Rate limit abusive paths: `limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;` + `limit_req zone=login burst=10 nodelay;` in the location.

## 2. Apache httpd
```bash
dnf install httpd mod_ssl     # apt install apache2; Debian: a2enmod ssl proxy proxy_http headers rewrite http2; a2ensite app.conf
```
`/etc/httpd/conf.d/app.example.com.conf` (Debian: `/etc/apache2/sites-available/app.conf`):
```apache
<VirtualHost *:80>
    ServerName app.example.com
    Redirect permanent / https://app.example.com/
</VirtualHost>
<VirtualHost *:443>
    ServerName app.example.com
    ServerAlias www.app.example.com
    DocumentRoot /srv/app/public
    Protocols h2 http/1.1
    SSLEngine on
    SSLCertificateFile    /etc/letsencrypt/live/app.example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/app.example.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
    Header always set Strict-Transport-Security "max-age=63072000"

    <Directory /srv/app/public>
        Options -Indexes +FollowSymLinks
        AllowOverride None          # .htaccess off = faster; "All" only if the app needs it
        Require all granted
    </Directory>
    ProxyPreserveHost On
    ProxyPass        /api/ http://127.0.0.1:8000/api/
    ProxyPassReverse /api/ http://127.0.0.1:8000/api/
    RequestHeader set X-Forwarded-Proto "https"
    ErrorLog  /var/log/httpd/app.error.log
    CustomLog /var/log/httpd/app.access.log combined
</VirtualHost>
```
```bash
apachectl configtest && systemctl reload httpd    # Debian: apache2ctl configtest; apache2
apachectl -S                                      # vhost/ServerName map; "default" vhost is the first loaded file
```
- Apache picks the vhost by `ServerName`/`ServerAlias`; the first `<VirtualHost>` for an
  address:port is the default — name the file `000-default.conf` deliberately.
- MPM: the MPM is chosen at build or package level; `apachectl -M | grep mpm` shows which is loaded.
  `event` is the usual pairing with PHP-FPM through `mod_proxy_fcgi`.
- `Require all granted` replaced `Allow from all` in 2.4; mixing them yields 403s.
- SELinux: proxying to a backend, serving home directories, NFS content and non-standard listen
  ports may be blocked by SELinux; read the audit log for the exact denial, then use the
  matching SELinux boolean or port label.

## 3. TLS with certbot (both servers)
```bash
dnf install certbot python3-certbot-nginx     # or python3-certbot-apache
certbot --nginx -d app.example.com -d www.app.example.com --agree-tos -m ops@example.com --redirect
certbot renew --dry-run; systemctl list-timers | grep certbot    # package installs usually add a systemd timer or cron job for `certbot renew`; add `--deploy-hook` to reload the server
```
Behind a firewall or for wildcards: `certbot certonly --dns-<provider>` (DNS-01).
Mozilla's SSL config generator gives the cipher/protocol lines; pick the profile that matches your client base. Test with `openssl s_client -connect app.example.com:443 -servername app.example.com`
or an external scanner.

## 4. Operations
- Logs: `tail -f /var/log/nginx/app.access.log | awk '$9 >= 500'`.
- Firewall: `firewall-cmd --add-service={http,https} --permanent && firewall-cmd --reload`.
- Health: `curl -sI -H 'Host: app.example.com' http://127.0.0.1/ | head -1` bypasses DNS/TLS.
- Rotate logs via the package's logrotate rule (sends `USR1`/`graceful`); don't `> file`.

## Verify
- [ ] `nginx -t` / `apachectl configtest` clean; `curl -I https://app.example.com` returns 200 with HSTS and `http://` returns 301.
- [ ] Proxied app logs show the real client IP (it reads `X-Forwarded-For`) and generates `https://` links.
- [ ] `certbot renew --dry-run` succeeds and an unknown Host header gets the catch-all, not your site.

## Checked

2026-10-28

Confirmed: nginx.org module references (core: default_server, 444, root/alias; proxy: proxy_pass URI behaviour, proxy_http_version, proxy_set_header, proxy_read_timeout; ssl; limit_req; fastcgi; upstream keepalive; v2: http2 directive appeared in 1.25.1), Apache 2.4 manual (core, mod_proxy, mod_ssl, mod_headers, name-based vhosts, upgrading: Require replaces Allow), certbot user guide (--nginx, --apache, --agree-tos, --redirect, --dns-*, cron or systemd timer, --deploy-hook).

Removed or corrected: The 'before 1.25' http2 version gate (it is 1.25.1), SELinux boolean and fcontext commands, the claim that event is Apache's default MPM, the 'timer renews twice daily' claim, and the claim that Mozilla intermediate is the production default.

Run 2026-11-01 on nginx 1.30.6 (Windows, 127.0.0.1 only): the nginx proxy block (`proxy_pass`, `proxy_http_version 1.1`, `Host`, `X-Forwarded-For`, `X-Forwarded-Proto`, empty `Connection`) passes `nginx -t`; the upstream saw `Host: app.example.com`, `X-Forwarded-For: <client>, 127.0.0.1` and `X-Forwarded-Proto: http` (the skill's value is `$scheme`); `alias` stripped the location prefix and `root` kept it; `proxy_pass http://app/` replaced the `/strip/` prefix while `proxy_pass http://app` kept the URI; the websocket location sent `Upgrade` and `Connection: upgrade`; a dead upstream gave 502, a body over `client_max_body_size` gave 413, and the `default_server ... return 444` block closed the connection for an unknown Host (curl error 52, empty reply). Not run, so the status stays docs-checked: Apache, certbot, dnf/apt, SELinux, firewalld, logrotate, the 504 timeout and `limit_req` in this skill's own block.

Method: documentation, plus the nginx parts run locally as described above; Apache and the OS tooling were not run.
