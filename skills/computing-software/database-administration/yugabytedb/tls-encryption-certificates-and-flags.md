---
id: computing-software.database-administration.yugabytedb.tls-encryption-certificates-and-flags
name: tls-encryption-certificates-and-flags
category: computing-software
field: database-administration
product: yugabytedb
tags: [tls, certificates, openssl, node-to-node-encryption, client-to-server-encryption, allow-insecure-connections, certs-dir, ca-crt]
level: advanced
status: docs-checked
description: "Enable TLS in YugabyteDB: generate a CA and per-node certificates with OpenSSL or yugabyted, place node files, and set the encryption flags on masters and tservers."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/tls-encryption/server-certificates.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/tls-encryption/server-to-server.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/security-checklist.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS encryption: certificates and flags

**Certificates.** Create a CA, then a key and certificate per node. The node.conf sets commonName to the node IP address (the page marks it required, do not change) and may list extra IP and DNS subject alternative names:
1. In a `secure-data` directory write an OpenSSL `ca.conf`, create `index.txt` and `serial.txt` (containing `01`), generate the CA key with `openssl genrsa -out secure-data/ca.key` and restrict it with `chmod 400`.
2. Create the CA certificate with `openssl req -x509`.
3. For each node write a `node.conf` with the SAN, create a key and CSR, and sign it with `openssl ca`.
4. Check each chain with `openssl verify -CAfile ca.crt node.<name>.crt`.

Each node needs only `ca.crt`, `node.<commonName>.crt` and `node.<commonName>.key`; YugabyteDB recognizes the key only in the `node.<commonName>.key` format. Copy them to a directory on the node (the page uses `~/certs/<node-ip-address>`) and delete or secure the temporary copies.

**Flags** (set on both yb-master and yb-tserver):
- `--use_node_to_node_encryption=true` (default false)
- `--use_client_to_server_encryption=true` (default false)
- `--allow_insecure_connections=false` (default true) disallows any service with unencrypted communication from joining the cluster; it requires `--use_node_to_node_encryption` or `--use_client_to_server_encryption` to be enabled
- `--certs_dir=/path/to/tls/<node_ip>` (optional): the node's certificate directory. The default is `<data drive>/yb-data/master/data/certs` for masters and `<data drive>/yb-data/tserver/data/certs` for tservers
- `--certs_for_client_dir` (optional): the client TLS configuration directory; defaults to the same directory as `--certs_dir`

Apply the flags to every master and tserver. `yb-ts-cli reload_certificates` triggers a reload of TLS certificates and private keys from disk on the specified server (the page's example certificates are valid for 3650 days). To connect yb-admin to a TLS cluster, pass `--certs_dir_name` with the directory holding the root certificate.

## Checked

2026-11-04. Confirmed against the Create server certificates page (secure-data directory, ca.conf, index.txt and serial.txt, openssl genrsa, chmod 400, openssl req -x509, node.conf, openssl ca, openssl verify, required file names and copy step), the Enable encryption in transit page (flag names, defaults, certs_dir defaults, certs_for_client_dir), the yb-ts-cli reference (reload_certificates), the yb-admin reference (certs_dir_name) and the security checklist (TLS for intra-cluster and client-to-server traffic). Removed: the yugabyted cert generate_server_certs command, which no cited page documents, and the advice to renew certificates before expiry. Corrected allow_insecure_connections, which requires either node-to-node or client-to-server encryption.

Method: documentation only; no commands were run.
