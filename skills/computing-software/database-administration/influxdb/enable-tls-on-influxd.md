---
id: computing-software.database-administration.influxdb.enable-tls-on-influxd
name: enable-tls-on-influxd
category: computing-software
field: database-administration
product: influxdb
tags: [tls, https, certificates, tls-cert, tls-key, telegraf]
level: practitioner
status: docs-checked
description: "Enable HTTPS on influxd with --tls-cert and --tls-key, choose certificate type, set file permissions and point Telegraf at https URLs."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/security/enable-tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

InfluxData strongly recommends HTTPS whenever requests cross a network. Certificate options: single-domain CA-signed, wildcard CA-signed (reusable across instances), or self-signed (encrypts but clients cannot verify the server).

Steps: obtain or generate cert files (self-signed via `openssl`, with a Subject Alternative Name), set permissions, run `influxd` with TLS flags, verify.

```sh
sudo chown influxdb: /etc/ssl/influxdb-selfsigned.crt /etc/ssl/influxdb-selfsigned.key
sudo chmod 644 /etc/ssl/influxdb-selfsigned.crt
sudo chmod 600 /etc/ssl/influxdb-selfsigned.key

influxd \
  --tls-cert="/etc/ssl/influxdb-selfsigned.crt" \
  --tls-key="/etc/ssl/influxdb-selfsigned.key"

curl --verbose --insecure https://localhost:8086/api/v2/ping
```

Let's Encrypt with certbot installs under `/etc/letsencrypt/live/$domain` by default. Tune with `tls-min-version` and `tls-strict-ciphers`.

Telegraf `influxdb_v2` output: use `https://` URLs, and for a self-signed certificate set `insecure_skip_verify = true`.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 "Enable TLS/SSL encryption" page, lines 574-770 of the downloaded text read (requirements, configuration, Telegraf and troubleshooting sections).

Confirmed: three certificate types, certbot default path, chown/chmod commands, `--tls-cert` and `--tls-key`, verification curl, `tls-min-version`, `tls-strict-ciphers`, Telegraf `insecure_skip_verify`.
