---
id: computing-software.search-and-information-retrieval.typesense.server-networking-tls-and-cors
name: server-networking-tls-and-cors
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [api-port, ssl-certificate, cors-domains, typesense]
level: practitioner
status: docs-checked
description: "Set Typesense bind addresses, API and peering ports, HTTPS certificate flags, certificate refresh, CORS origins and cluster node parameters."
sources: ["https://typesense.org/docs/30.2/api/server-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Networking, TLS and CORS parameters

## Networking

- `--api-address`: address the API binds to, default `0.0.0.0`; IPv6 such as `::` is allowed.
- `--api-port`: default `8108`.
- `--peering-address`: internal IP for the peering service; if unset, Typesense uses the first available internal IP. IPv6 allowed.
- `--peering-port`: default `8107`.
- `--peering-subnet`: internal subnet to use for peering, e.g. `192.160.1.0/24` (IPv6 prefixes also work).

## HTTPS

Give both `--ssl-certificate` and `--ssl-certificate-key` (paths to the certificate and key files); one without the other does not enable HTTPS. `--ssl-refresh-interval-seconds` controls how often certs are reloaded from disk, default `8 * 60 * 60`.

## CORS

`--enable-cors` lets a JavaScript client reach Typesense directly from the browser. `--cors-domains` takes a comma separated list of allowed domains such as `https://example.com,https://example2.com`, with no trailing slashes.

## Clustering

`--nodes` is a path to a file containing a comma separated string of all nodes. `--reset-peers-on-error` forcibly resets the node's peers after an irrecoverable clustering error; it may cause intermittent data loss and is a last resort.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Server Configuration (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
