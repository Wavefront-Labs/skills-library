---
id: computing-software.search-and-information-retrieval.meilisearch.enable-http2-with-ssl
name: enable-http2-with-ssl
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [http2, ssl-certificate, ssl-cert-path, meilisearch]
level: practitioner
status: docs-checked
description: "Serve Meilisearch over HTTP/2 by starting it with --ssl-cert-path and --ssl-key-path, generating a local cert with mkcert and testing with curl --http2."
sources: ["https://www.meilisearch.com/docs/resources/self_hosting/security/http2_ssl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP/2 and SSL

HTTP/2 only works when the server has an SSL certificate. Without one, Meilisearch ignores the upgrade request and keeps answering with HTTP/1.

## Without SSL

Run `./meilisearch`, then `curl -kvs --http2 --request GET 'http://localhost:7700/indexes'`. The request header shows `Connection: Upgrade, HTTP2-Settings` but the reply is `HTTP/1.1 200 OK`: the upgrade failed.

## With SSL

1. Generate a certificate and key. The docs use mkcert: `mkcert '127.0.0.1'` writes `127.0.0.1.pem` and `127.0.0.1-key.pem`. On a remote server you can use certbot or a certificate from a Certificate Authority.
2. Start with `./meilisearch --ssl-cert-path ./127.0.0.1.pem --ssl-key-path ./127.0.0.1-key.pem`.
3. Repeat the request over `https://`: `curl -kvs --http2 --request GET 'https://localhost:7700/indexes'`. The output shows ALPN accepting `h2`, `HTTP/2 confirmed` and `< HTTP/2 200`.

## Docker

Pass the same parameters through environment variables and mount the certificates into the container with a volume.

## Checked

2026-11-03. Confirmed claim by claim against the HTTP/2 and SSL page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
