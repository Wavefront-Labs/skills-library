---
id: computing-software.systems-network-administration.dns-dhcp.phpipam-setup-and-subnet-management
name: phpipam-setup-and-subnet-management
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [ipam, phpipam-setup, phpipam, subnet-discovery, ip-address-management, rest-api, ddi]
level: practitioner
status: docs-checked
description: "Run phpIPAM as a lightweight IPAM: install via the Docker images, schedule discovery scans with the cron container, and allocate addresses through its REST API."
sources:
  - https://phpipam.net/documents/
  - https://phpipam.net/api/api_documentation/
  - https://hub.docker.com/r/phpipam/phpipam-www
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# phpIPAM setup and subnet management

phpIPAM is an open-source PHP/MySQL IPAM focused on addresses.

## Install (Docker compose)
```yaml
services:
  phpipam-web:
    image: phpipam/phpipam-www:latest
    ports: ["8080:80"]
    environment: {TZ: UTC, IPAM_DATABASE_HOST: phpipam-mariadb, IPAM_DATABASE_PASS: "change-me"}
    depends_on: [phpipam-mariadb]
  phpipam-cron:
    image: phpipam/phpipam-cron:latest
    environment: {TZ: UTC, IPAM_DATABASE_HOST: phpipam-mariadb, IPAM_DATABASE_PASS: "change-me", SCAN_INTERVAL: "1h"}
    depends_on: [phpipam-mariadb]
  phpipam-mariadb:
    image: mariadb:latest
    environment: {MYSQL_ROOT_PASSWORD: "change-me-too"}
    volumes: ["phpipam-db:/var/lib/mysql"]
volumes: {phpipam-db: {}}
```
The Docker Hub page describes `phpipam-www` as the Apache/PHP frontend and `phpipam-cron` as the cron container for
scheduled network discovery jobs. Several `phpipam-www` replicas can be load-balanced; run only one `phpipam-cron`.
Replace the placeholder passwords, then finish setup in the web installer and put the site behind HTTPS.

## Discovery
The cron container runs the discovery scans every `SCAN_INTERVAL`. Enable scanning per subnet in the web UI
(the phpIPAM guide "Automatic host availability and discovery check" covers it). Use the results to reclaim stale
allocations.

## API allocation
Create an API app in the web UI (the app ID goes in the URL; SSL security is recommended because BASIC auth is sent
unencrypted). Authenticate with a POST to `/api/<app_id>/user/` to get a token valid for 6 hours by default (each
successful request resets it), then send it in the `token` or `phpipam-token` header:
```
curl -s -X POST https://ipam.example.net/api/automation/user/ -u svc:pass      # get token
curl -s -H "token: $TOKEN" https://ipam.example.net/api/automation/subnets/42/first_free/
curl -s -X POST -H "token: $TOKEN" https://ipam.example.net/api/automation/addresses/first_free/42/ \
  -d hostname=web07.example.net -d description="created by automation"
```
`GET /api/<app_id>/subnets/{id}/first_free/` returns the first available address in a subnet; `POST
/api/<app_id>/addresses/first_free/{subnetId}/` creates the address.

## Gotchas
- Back up the database; IPAM data is hard to rebuild.

## Verify
- [ ] Subnets match the routing table, scans show recent results, and API allocation returns the next free address.

## Checked
Date: 2026-10-28.
Confirmed against the phpIPAM API documentation (authentication via POST to `/api/<app_id>/user/`, `token` and
`phpipam-token` headers, 6 hour default expiry, SSL recommendation, `first_free` endpoints) and the phpipam/phpipam-www
Docker Hub page (image names, `IPAM_DATABASE_HOST`/`IPAM_DATABASE_PASS`, `SCAN_INTERVAL`, `MYSQL_ROOT_PASSWORD`,
cron replica rule). Corrected: MariaDB root password variable (`MYSQL_ROOT_PASSWORD`, as on the Hub page), added the
cron container's `depends_on`. Removed: LDAP/SAML login, section/VRF/address-state data model details, "Ping check" and
"Discover new hosts" option names, remote scan agents, Terraform/Ansible providers and the NetBox comparison (none
confirmed on fetched pages).
Method: documentation only; no commands were run.
