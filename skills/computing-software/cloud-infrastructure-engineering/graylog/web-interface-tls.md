---
id: computing-software.cloud-infrastructure-engineering.graylog.web-interface-tls
name: web-interface-tls
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [web-tls, https, pem-keys, truststore, private-ca]
level: practitioner
status: docs-checked
description: "Enable HTTPS on the Graylog web interface and API: certificate and key files, PFX conversion, private CA trust and Sidecar server_url."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/secure_graylog_interface_with_tls.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# web interface tls

Graylog needs two files: a public key certificate (`public.pem`) and a private key (`private.key`). Protect both.

Notes:
- A PFX certificate must be converted to PEM, extracting public key, private key and chain, preferably with OpenSSL.
- Trust depends on the CA. Browsers trust public CAs by default; for a private CA (for example Active Directory Certificate Services) import its root certificate manually.
- Edit both the `graylog-server` service defaults file and `server.conf` so Graylog uses the right truststore.
- If Sidecars connect to a non-HTTPS URL or IP, verify `server_url` is configured correctly.
- You need SSH and root access to the Graylog servers and an SFTP client to upload the files.

Steps from the page:
1. Graylog supports only PKCS#8 private keys in PEM encoding. A key starting with `BEGIN ENCRYPTED PRIVATE KEY` is correct; `BEGIN PRIVATE KEY` or `BEGIN RSA PRIVATE KEY` must be converted with `openssl pkcs8 -topk8`. The public file is PEM (`BEGIN CERTIFICATE`), usually a chain with root, intermediate and issued certificates.
2. Store the files in a directory such as `/opt/graylog/tls/`, owned by the `graylog` user, private key mode 600 and public file mode 644.
3. For a private CA, copy the Java `cacerts` store (the system OpenJDK's, or the bundled one under the graylog-server install if no separate OpenJDK exists) to `/etc/graylog/graylog.jks`, and import each root and intermediate CA in PEM form with `keytool -importcert`.
4. Add `-Djavax.net.ssl.trustStore=/etc/graylog/graylog.jks` to the `GRAYLOG_SERVER_JAVA_OPTS` line of the graylog-server defaults file.
5. In `server.conf` set `http_enable_tls = true`, `http_tls_cert_file`, `http_tls_key_file` and `http_tls_key_password` (no quotes), then `sudo systemctl restart graylog-server`.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/setting_up_graylog/secure_graylog_interface_with_tls.htm (read in full, Graylog 7.2 docs). Dropped the unsourced load balancer note and corrected the Sidecar `server_url` wording.
