---
id: computing-software.collaboration-platform-administration.mattermost.encryption-options
name: encryption-options
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [encryption, tls, gossip-encryption, encryption-at-rest]
level: practitioner
status: docs-checked
description: "Mattermost encryption in transit (TLS, calls DTLS/SRTP, gossip), at rest (disk, S3 SSE) and supported SAML encryption methods."
sources: ["https://docs.mattermost.com/deployment-guide/encryption-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Encryption options

In transit: Mattermost supports TLS, including AES-256 with 2048-bit RSA, between clients and the server. Either set up TLS on the Mattermost server itself or put a proxy such as NGINX in front and terminate TLS there. LDAP connections can optionally be secured with TLS or stunnel. Calls are protected by TLS on the existing WebSocket signaling path, mandatory DTLS v1.2 for the initial key exchange, and mandatory SRTP for all media packets (voice and screen share).

Gossip encryption: in high availability mode, cluster data sent by the gossip protocol can be encrypted. From v10.11 it is enabled by default for new deployments, while existing deployments keep their current configuration. It uses AES-256 by default and is not configurable through settings; the key can be set manually in the ClusterEncryptionKey row of the Systems table as a base64 byte array of 16, 24 or 32 bytes, which selects AES-128, AES-192 or AES-256.

At rest: Mattermost does not encrypt message content itself, so that user search and compliance reporting keep working. Instead secure the database and file storage with full-disk or storage encryption such as LUKS on Linux, BitLocker on Windows, or database Transparent Data Encryption. For local, NFS or S3-compatible file storage use disk encryption on the storage server. For Amazon S3 an Enterprise setting enables server-side encryption with S3-managed keys.

SAML assertion encryption is configured with the identity provider settings, not at the infrastructure layer; see the supported SAML encryption methods in the authentication configuration settings. Encryption is not required for GDPR but can be used as an additional safeguard against data breach.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/deployment-guide/encryption-options (TLS, calls, gossip, at rest). Removed the SAML cipher list, which is not on this page.

Method: documentation only; no commands were run.
