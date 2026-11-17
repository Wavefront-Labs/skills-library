---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-cassandra-tls
name: jaeger-cassandra-tls
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, cassandra-tls, cqlshrc, client-certificates, jaeger-cassandra]
level: advanced
status: docs-checked
description: "Enable client-to-node TLS for Jaeger's Cassandra connection and give the schema tool a custom cqlshrc."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/cassandra/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt and authenticate the Cassandra connection.

Jaeger supports TLS client-to-node connections as long as the Cassandra cluster is configured for it. Specify paths to the TLS certificates (.pem files) in the `tls:` section under `connection:`; available properties follow `configtls.ClientConfig` from the OpenTelemetry Collector repository. Tip from the docs: verify the certificates with cqlsh first.

The schema tool also supports TLS. Make a custom cqlshrc and a volume containing four files: the cqlshrc, ca-cert (the certificate authority), client-key and client-cert. Map the volume to `/root/.cassandra` in the schema container and set the environment variable `CQLSH_SSL=--ssl`. The cqlshrc looks like:
```
[ssl]
certfile = ~/.cassandra/ca-cert
userkey = ~/.cassandra/client-key
usercert = ~/.cassandra/client-cert
# validate = false
```
Uncomment `validate = false` only if a DNS mismatch makes you want to ignore server validation issues.

## Checked

Method: docs-checked 2026-11-09 against the Jaeger 2.22 Cassandra storage page (read in full); the unconfirmed security-matrix sentence was removed.
