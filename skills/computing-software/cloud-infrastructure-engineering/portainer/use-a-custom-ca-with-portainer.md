---
id: computing-software.cloud-infrastructure-engineering.portainer.use-a-custom-ca-with-portainer
name: use-a-custom-ca-with-portainer
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [certificates, custom-ca, trust-store, bind-mount]
level: advanced
status: docs-checked
description: "Make Portainer trust a private certificate authority for custom template URLs and other external resources by mounting the host CA store."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/troubleshooting/certificates-and-security/how-can-i-use-my-custom-certificate-authority-ca-with-portainer.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Symptom: Portainer fails to reach an external resource, such as a custom template URL, whose certificate was signed by your private CA.

Fix: inject the CA into both the Portainer Server and every Portainer Agent container. First add the CA to the host's CA store; on most Linux distributions use the `ca-certificates` package (Ubuntu has a documented procedure for installing a root CA). Do this on every host that runs Portainer or the Agent.

Then mount the host store into the container by modifying the command used to create it. For Docker Standalone `docker run`, add a bind mount such as:

```
-v /etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt
```

For Docker Swarm, add the same volume to both the Portainer Server and Agent services in the stack file. The page's examples cover Docker Standalone and Swarm.

If your host's CA store is elsewhere, change only the host side of the mount; the containers expect the store at `/etc/ssl/certs/ca-certificates.crt`. The same applies to the Agent's own `docker run` command.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed unconfirmed claims about Agent outbound calls, Kubernetes manifests and recreating containers; added the required container-side path.

Method: documentation only; no commands were run.
