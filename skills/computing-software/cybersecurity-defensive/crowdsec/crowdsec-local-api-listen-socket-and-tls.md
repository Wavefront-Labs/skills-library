---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-local-api-listen-socket-and-tls
name: crowdsec-local-api-listen-socket-and-tls
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [listen-uri, unix-socket, listen-socket, local-api-tls, ssl, ports]
level: advanced
status: docs-checked
description: "Expose the CrowdSec Local API to remote clients, over a unix socket or with TLS, and know the ports and outbound connections CrowdSec needs."
sources: ["https://docs.crowdsec.net/docs/local_api/configuration", "https://docs.crowdsec.net/docs/configuration/network_management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the Local API listens on `127.0.0.1:8080`; `crowdsec` and `cscli` use that as their API too. To serve remote Log Processors or bouncers change `listen_uri` under `api.server` in `config.yaml`.

## Unix socket

If every Log Processor and bouncer runs on the same machine, listen on a socket instead of, or in addition to, TCP:

```yaml
api:
  server:
    listen_socket: /run/crowdsec/crowdsec_api.sock
```

Clients then use the socket path as `url` in their credentials file. Socket traffic is never encrypted and client certificate authentication does not apply to it; access control is the filesystem permission on the socket.

## TLS

If the API is exposed to the internet, enable TLS or use a reverse proxy with SSL termination; inside a LAN or VPN it is not necessary:

```yaml
api:
  server:
    tls:
      cert_file: "/path/to/cert.pem"
      key_file: "/path/to/key.pem"
```

## Ports and outbound traffic

- `tcp/8080`: REST API for bouncers, cscli and Log Processors
- `tcp/6060`: `/metrics` (Prometheus) and `/debug` (pprof)

Outbound: the LAPI connects to `api.crowdsec.net`, `blocklists.api.crowdsec.net` and `papi.api.crowdsec.net` on 443 (signals, blocklists, console management); cscli reaches `cdn-hub.crowdsec.net`, `version.crowdsec.net` and `hub-data.crowdsec.net`. If the agent configuration is wrong on a host that also runs the LAPI, the LAPI fails to start too, by design.

## Checked

2026-11-03. Confirmed against the Local API configuration and network-management pages: default 127.0.0.1:8080, listen_uri, listen_socket and its unencrypted/no-client-cert warning, tls cert_file/key_file, ports 8080 and 6060, outbound hosts and the agent/LAPI failure note. Fixed: TLS wording to match the page.

Method: documentation only; no commands were run.
