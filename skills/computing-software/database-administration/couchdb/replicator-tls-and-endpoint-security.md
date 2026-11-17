---
id: computing-software.database-administration.couchdb.replicator-tls-and-endpoint-security
name: replicator-tls-and-endpoint-security
category: computing-software
field: database-administration
product: couchdb
tags: [replication, tls, certificates, endpoint-protocols, auth-plugins]
level: advanced
status: docs-checked
description: "Secure CouchDB replication endpoints: verify_ssl_certificates, trusted CA file, client certs, allowed protocols, insecure-endpoint logging, and auth plugins."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `[replicator]`:

- `verify_ssl_certificates = true` validates peers, using `ssl_trusted_certificates_file` if set, else OS CA files. `ssl_certificate_max_depth` must be set even if validation is off (example 3).
- `cert_file`, `key_file`, and `password` (only for a protected key) supply a client certificate.
- `cacert_reload_interval_hours` (example 24): how often to clear the Erlang VM's cached OS CA certificates and reload from disk.
- `valid_endpoint_protocols = http,https` (3.3): jobs with other endpoint URL protocols fail. `valid_proxy_protocols = http,https,socks5` likewise for proxies.
- `valid_endpoint_protocols_log = true` (3.4): logs replications using insecure `http`.
- `verify_ssl_certificates_log = true` (3.4): if a trusted file is set but verification is not, checks certificates and logs problems without failing the job.
- `auth_plugins` (2.2): tried in order, first to initialise wins: `couch_replicator_auth_session` (cookie), `couch_replicator_auth_ibm`, and `couch_replicator_auth_noop` (basic auth), which should be last.
- `ibrowse_options = [{prefer_ipv6, true}]` (3.4) supports IPv6-only endpoints.

## Checked

2026-11-04. Confirmed against the CouchDB config/replicator page ([replicator] TLS and security options): verify_ssl_certificates with ssl_trusted_certificates_file or OS CA files, ssl_certificate_max_depth, cert_file, key_file and password, cacert_reload_interval_hours, valid_endpoint_protocols and valid_proxy_protocols (3.3), the two _log options (3.4), auth_plugins (2.2) and ordering, ibrowse_options (3.4). Nothing removed.

Method: documentation only; no commands were run.
