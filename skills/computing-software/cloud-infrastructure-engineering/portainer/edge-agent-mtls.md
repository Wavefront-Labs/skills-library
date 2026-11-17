---
id: computing-software.cloud-infrastructure-engineering.portainer.edge-agent-mtls
name: edge-agent-mtls
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [mtls, edge-agent, certificates, ca, business-edition]
level: advanced
status: docs-checked
description: "Set up mutual TLS between the Portainer Server and Edge Agents using your own certificate authority and the mtls CLI flags."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/mtls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
mTLS makes the Edge Agent and the Server authenticate each other with certificates from a trusted CA. It is Business Edition only.

You need: a CA you control and its certificate in PEM (`mtlsca.crt`); a domain dedicated to mTLS pointing at the Server; a server certificate and key (`mtlsserver.crt`, `mtlsserver.key`) issued with `serverAuth` in extendedKeyUsage and containing that domain; and a client certificate and key (`client.crt`, `client.key`) issued with `clientAuth`.

Configure the Server by mounting the certificates and adding these flags to the Portainer command:

```
--mtlscacert /certs/mtlsca.crt \
--mtlscert /certs/mtlsserver.crt \
--mtlskey /certs/mtlsserver.key
```

On Docker Swarm, create Docker secrets (for example `docker secret create portainer.mtlscacert ...`) and reference them as `/run/secrets/portainer.mtlscacert` and so on in the service command, attaching the secrets in the stack file. On an existing Server you can instead open Settings, Edge Compute, turn on Use separate mTLS cert and upload the CA certificate, server certificate and key; changing the CA this way needs a Server restart and updated Edge Agents. The older `--sslcacert` flag is deprecated in favour of mTLS.

On the Edge Agent, use the mTLS domain as the Portainer API server URL and tunnel address, set `EDGE_INSECURE_POLL=0`, mount the CA certificate, `client.crt` and `client.key`, and add `--mtlscacert`, `--mtlscert` and `--mtlskey` to the agent command. The page says mTLS for the Agent on Kubernetes is a work in progress.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed the unconfirmed claim about what happens without the separate mTLS cert; added the Edge Agent side and the post-install UI route.

Method: documentation only; no commands were run.
