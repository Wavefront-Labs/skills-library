---
id: computing-software.cloud-infrastructure-engineering.rancher.api-keys-create-scope-expiry
name: api-keys-create-scope-expiry
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [api-keys, bearer-token, access-key, secret-key, rancher-cli, auth-token-max-ttl-minutes, scoped-token]
level: intro
status: docs-checked
description: "Create and revoke Rancher API keys: the four parts of a key, expiry bounded by auth-token-max-ttl-minutes, cluster scoping, and the one-time display of the secret."
sources:
  - https://ranchermanager.docs.rancher.com/reference-guides/user-settings/api-keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Applications and the Rancher CLI authenticate to the Rancher API with an API key, created in the UI. A key has four components:

- **Endpoint**: where requests are sent to the Rancher API.
- **Access Key**: the token's username.
- **Secret Key**: the token's password. For tools that ask for two strings, enter the two keys; some ask for one.
- **Bearer Token**: access and secret key concatenated, for tools that want a single authentication string. Use it with the Rancher CLI.

Create one from **User Avatar > Account & API Keys > Create API Key**. Optionally add a description and pick an **expiration period** or a **scope**. The page recommends setting an expiry, since shorter periods are more secure. The expiry is bounded by the setting `auth-token-max-ttl-minutes` (under `v3/settings`): if your choice exceeds it, the key is created with the maximum instead.

A **scope** restricts the key to the Kubernetes API of one cluster. If that cluster has an Authorized Cluster Endpoint configured, a scoped token can be used directly against the cluster's API without proxying through the Rancher server.

After **Create**, the endpoint, access key, secret key and bearer token are shown **once**; copy them to a secure place, as a lost key must be replaced with a new one. Users may also opt to enable token hashing.

Revoke a key by selecting it and clicking **Delete**. Delete keys that may be compromised or have expired.

Token deprecation: Rancher v2.13 introduced a `tokens.ext.cattle.io` token resource, and from v2.14.0 the legacy v3 tokens (`tokens.management.cattle.io`) are being phased out for removal in a future release. The dashboard supports create, view or list, and delete for the new tokens.

## Checked

2026-11-09. Read in full the Rancher Manager API Keys page (ranchermanager.docs.rancher.com, reference-guides/user-settings/api-keys). Added the v3 token deprecation note; the rest matched.

Method: documentation only; no commands were run.
