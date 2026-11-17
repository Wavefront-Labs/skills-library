---
id: computing-software.systems-network-administration.syncthing.discovery-server-stdiscosrv
name: discovery-server-stdiscosrv
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, stdiscosrv, global-discovery, discovery-server]
level: advanced
status: docs-checked
description: "Run your own Syncthing discovery server (stdiscosrv), choose its TLS mode, and point clients at it."
sources: ["https://docs.syncthing.net/users/stdiscosrv.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running stdiscosrv

## Start
```sh
stdiscosrv --cert=/path/to/cert.pem --key=/path/to/key.pem
```
It prints `Server device ID is ...`. Useful flags: `--listen` (default `:8443`), `--db-dir` (default `.`), `--db-flush-interval` (default `5m`), `--metrics-listen` (Prometheus compatible metrics endpoint, disabled by default), `--compression` (GZIP of HTTP responses), `--http`, `--debug`. `--cert` and `--key` default to `./cert.pem` and `./key.pem`. At first start it generates certificate files and a database in the current directory unless given flags to the contrary.

## Certificates
1. A CA-signed certificate for your domain. Clients verify it normally.
2. Any certificate, with clients authenticating the server by device ID.
3. `--http` behind an SSL-secured reverse proxy. Cert and key are unused in this mode.

## Point clients at it
In Settings > Global Discovery Server, add your address to the comma-separated list. The `default` entry stands for the global discovery servers; keep it to use them as well, or remove it to use only yours. For a non CA-signed certificate give the printed device ID in the URL:

```
https://disco.example.com:8443/?id=<server device ID>
```
Otherwise omit `?id=`. With a proxy using a valid HTTPS certificate, clients omit it too. The port is 8443 by default, and a dynamic IP address needs a dynamic DNS service to be reachable from the internet.

## Reverse proxy requirements
- Run with `-http` and configure an SSL certificate/key for the proxy.
- Pass `X-Forwarded-For` with the real client IP.
- Pass `X-Client-Port` (added in version 1.8.0) with the client's real connection port.
- Pass `X-SSL-Cert` with the PEM-encoded client certificate. It is present in POST requests and may be empty in GET requests. If the server logs `no certificates` for POST requests, the proxy is not passing the header.
- The proxy must request the client certificate but not require it to be signed by a trusted CA (nginx: `ssl_verify_client optional_no_ca`).

## Colocation
If an instance of Syncthing runs on the discovery server, either add that instance to other devices using a static address or bind the discovery server and Syncthing to different IP addresses.

## Checked
2026-11-04. Read the Syncthing Discovery Server page: synopsis and option defaults, the three certificate options, device-ID URL form, GUI path, `default` entry, reverse proxy headers and requirements, the nginx directive, and the colocation note. Tightened wording for the proxy header requirements and the dynamic DNS note.
Method: documentation only; no commands were run.
