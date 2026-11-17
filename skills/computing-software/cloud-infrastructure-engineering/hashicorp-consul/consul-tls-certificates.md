---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-tls-certificates
name: consul-tls-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-tls, consul-tls-cert, verify-server-hostname]
level: practitioner
status: docs-checked
description: "Create a CA and server, client and CLI certificates with consul tls, and configure verify_incoming, verify_outgoing and verify_server_hostname."
sources: ["https://developer.hashicorp.com/consul/commands/tls/ca", "https://developer.hashicorp.com/consul/commands/tls/cert", "https://developer.hashicorp.com/consul/docs/reference/agent/configuration-file/tls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`consul tls ca create` makes a self-signed CA; `consul tls cert create` makes certificates from it. Use your own PKI where you need more than this generator.

```sh
consul tls ca create                          # writes <ca>.pem and <ca>-key.pem
consul tls cert create -server -dc dc1
consul tls cert create -client
consul tls cert create -cli
```

Options: `cert create` takes `-days` (default 1 year), `-dc` (server certs only, default `dc1`), `-domain`, `-node` (adds `<node>.server.<datacenter>.<domain>` as a DNS name), `-additional-dnsname`, `-additional-ipaddress`, `-ca` and `-key` (paths to CA and key). `localhost` and `127.0.0.1` are always included. `ca create` takes `-days` (default 1825), `-domain`, `-name-constraint` and `-additional-name-constraint`.

```hcl
tls {
  defaults {
    ca_file         = "<path to CA certificate>"
    cert_file       = "<path to agent certificate>"
    key_file        = "<path to agent key>"
    verify_incoming = true
    verify_outgoing = true
  }
  internal_rpc {
    verify_server_hostname = true
  }
}
```

Settings (all default false):
- `verify_incoming`: require TLS on incoming connections with a client certificate signed by the CA.
- `verify_outgoing`: require TLS on outgoing connections and a server certificate signed by the CA. It does not apply to gRPC.
- `verify_server_hostname` (under `internal_rpc`): also check that server certificates match `server.<datacenter>.<domain>`.

Gotchas:
- The tool warns that server certificates grant authority to become a server and access all state, including root keys and all ACL tokens. Do not put them on hosts that are not servers, and store them as securely as CA keys.
- Certificates expire after the `-days` you set (1 year by default), and the CA after 1825 days by default; plan renewal before then.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/tls/ca, commands/tls/cert (flags, defaults, warning text) and reference/agent/configuration-file/tls (the three verify settings, defaults, `tls.defaults`, `internal_rpc`). Removed: example file names that the pages do not give, the claim that plaintext to port 8300 is rejected, the `openssl` Verify step, and the renewal-with-`consul reload` remark (the reloadable list covers TLS only for an already-TLS-enabled setup).
Method: documentation only; no commands were run.
