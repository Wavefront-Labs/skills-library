---
id: computing-software.cybersecurity-defensive.dex.dex-openshift-connector
name: dex-openshift-connector
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [openshift, connector, service-account, oauth]
level: advanced
status: docs-checked
description: "Connect Dex to OpenShift using a service account OAuth client with clientSecretFile, or an OAuthClient resource."
sources:
  - https://dexidp.io/docs/connectors/openshift/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Recommended: use a service account as the OAuth client. Annotate it with the redirect URI:

```bash
oc patch serviceaccount dex-server --type='json' -p='[{"op": "add", "path": "/metadata/annotations/serviceaccounts.openshift.io~1oauth-redirecturi.dex", "value":"https://dex.example.com/callback"}]'
```

The client id takes the form `system:serviceaccount:<namespace>:<service_account_name>`.

For projected short-lived tokens, point `clientSecretFile` at the mounted token so Dex picks up rotations without a pod restart:

```yaml
connectors:
- type: openshift
  id: openshift
  name: OpenShift
  config:
    issuer: https://api.mycluster.example.com:6443
    clientID: system:serviceaccount:dex:dex-server
    clientSecretFile: /var/run/secrets/kubernetes.io/serviceaccount/token
    redirectURI: http://127.0.0.1:5556/dex/callback
```

Static alternatives: generate a token with `oc create token <sa-name> -n <namespace> --duration=8760h`, or read a legacy secret with `oc get secret <secret-name> -n <namespace> -o jsonpath='{.data.token}' | base64 --decode`, then put it in `clientSecret` (via an environment variable).

Alternatively register an `OAuthClient` resource with `secret`, `redirectURIs` and `grantMethod: prompt`.

Other options shown: `insecureCA`, `rootCA` and `groups` (the example lists `users`).

The docs label the service account route as recommended. The OAuthClient example sets `grantMethod: prompt`, and `redirectURIs` must contain Dex's callback URL.

## Checked

2026-11-03: read against Dex docs, OpenShift connector (https://dexidp.io/docs/connectors/openshift/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
