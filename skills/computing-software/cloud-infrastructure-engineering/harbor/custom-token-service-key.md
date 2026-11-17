---
id: computing-software.cloud-infrastructure-engineering.harbor.custom-token-service-key
name: custom-token-service-key
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [token-service, private-key, root-crt, docker-auth, harbor]
level: advanced
status: docs-checked
description: "Replace the Harbor token service private key and registry root certificate with your own after install or prepare."
sources:
  - https://goharbor.io/docs/main/install-config/customize-token-service/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docker clients must access Harbor with a token, using the same flow as Distribution Registry v2 token authentication: the client asks the token service for a token signed with a private key, and the registry verifies it with the matching certificate. By default Harbor uses its own key and certificate. You can substitute your own.

Generate a root certificate if you have none:
1. `openssl genrsa -out private_key.pem 4096`
2. `openssl req -new -x509 -key private_key.pem -out root.crt -days 3650`
3. Answer the Distinguished Name prompts (a `.` leaves a field blank).

This creates `private_key.pem` and `root.crt` in the current directory.

Provide them to Harbor after you have run `./install` or `./prepare`, which generate the defaults. Assuming the new files are in `/root/cert` and `/srv/harbor/data` is your `data_volume`:
```sh
cp /root/cert/private_key.pem /srv/harbor/data/secret/core/private_key.pem
cp /root/cert/root.crt /srv/harbor/data/secret/registry/root.crt
```
Then go back to the directory with the compose file and start Harbor with `docker compose up -d`. Push and pull an image to confirm your certificate works.

Note the destinations: the private key goes under `secret/core` and the root certificate under `secret/registry` of the data volume.

## Checked

2026-11-03. Token flow, openssl commands, file names, copy destinations and the `docker compose up -d` step were read against the Harbor docs page Customize the Harbor Token Service. Removed: the claim that swapping the files breaks token verification (the page does not say so).

Method: documentation only; no commands were run.
