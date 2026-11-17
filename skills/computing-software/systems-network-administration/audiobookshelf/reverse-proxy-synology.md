---
id: computing-software.systems-network-administration.audiobookshelf.reverse-proxy-synology
name: reverse-proxy-synology
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [reverse-proxy, synology, dsm, websocket, login-portal]
level: intro
status: docs-checked
description: "Create a Synology DSM reverse proxy rule for Audiobookshelf with the websocket custom header preset."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/reverse-proxy/5.synology-proxy-setup.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/2.docker-compose-install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In DSM open Control Panel then `Login Portal > Advanced > Reverse Proxy > Create`.

1. General: Reverse Proxy Name `audiobookshelf`.
2. Source: Protocol HTTPS, Hostname `<sub>.<quickconnectdomain>.synology.me` (for example `audiobookshelf.mydomain.synology.me`), Port 443, Access Control Profile left as is.
3. Destination: Protocol HTTP, Hostname your NAS IP, Port 13378.
4. Custom Header tab: choose `Create > Websocket`. Leave the generated headers as they are:

| Header Name | Value |
| --- | --- |
| Upgrade | `$http_upgrade` |
| Connection | `$connection_upgrade` |

5. Advanced Settings tab: leave as is.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Synology reverse proxy page.

Method: documentation only; no commands were run.
