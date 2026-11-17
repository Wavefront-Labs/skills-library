---
id: computing-software.systems-network-administration.syncthing.reverse-proxy-gui
name: reverse-proxy-gui
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, reverse-proxy, nginx, hostcheck]
level: advanced
status: docs-checked
description: "Publish the Syncthing web GUI behind nginx or Apache, and handle the host check, frame loading and timeout settings."
sources: ["https://docs.syncthing.net/users/reverseproxy.html", "https://docs.syncthing.net/users/config.html", "https://docs.syncthing.net/users/faq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reverse proxy for the GUI

The docs' examples pass the location `/syncthing` on the web server to the GUI on localhost:8384.

## nginx
```nginx
location /syncthing/ {
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_pass http://localhost:8384/;
  proxy_read_timeout 600s;
  proxy_send_timeout 600s;
}
```
The 600s read and send timeouts are part of the docs' example.

## Apache
Execute `a2enmod proxy_http headers` to enable the Apache HTTP Proxy and headers modules, then add to the Apache httpd configuration:

```apache
<Location /syncthing/>
  ProxyPass http://localhost:8384/
  ProxyPassReverse http://localhost:8384/
  RequestHeader set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}
  Require all granted
</Location>
```

## Caddy v2
```
handle_path /syncthing/* {
  reverse_proxy http://localhost:8384 {
    header_up Host {upstream_hostport}
  }
}
```

## Host check
Since version 0.14.6, when the GUI/API is bound to localhost Syncthing checks that the browser is talking to localhost, which protects against most DNS rebinding attacks. Behind a proxy you may get "Host check error". After ensuring the proxy provides sufficient authentication, either make the proxy set a Host header containing `localhost`, set `gui.insecureSkipHostcheck` in the advanced settings, or bind the GUI/API to a non-localhost listen port. In all cases username/password authentication and HTTPS should be used.

The config page says `insecureAllowFrameLoading` allows rendering the GUI within an iframe, frame or object by not setting the `X-Frame-Options: SAMEORIGIN` header, and may be needed when serving the GUI as part of a website through a proxy.

## Checked
2026-11-04. Read Reverse Proxy Setup, the FAQ Host check entry and the config page gui element: the nginx, Apache and Caddy v2 examples match the page, the module command, the three host-check fixes, the version, and `insecureAllowFrameLoading`. Removed the long-polling explanation for the timeouts, which the page does not give.
Method: documentation only; no commands were run.
