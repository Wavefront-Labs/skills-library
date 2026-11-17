---
id: computing-software.devops-ci-cd.argo-events.argo-events-webhook-eventsource-token-and-basic-auth
name: argo-events-webhook-eventsource-token-and-basic-auth
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, webhook, authsecret, basicauth, bearer-token, secret, authentication]
level: practitioner
status: docs-checked
description: "Protect webhook EventSource endpoints with a bearer token (authSecret) or HTTP Basic Auth (basicAuth), which are mutually exclusive."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/webhook-authentication.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events webhook eventsource token and basic auth

From v1.0, webhook EventSources (and extended ones lacking their own authenticator) can require authentication.

Bearer token: create a Secret, reference it with `authSecret`:

```sh
kubectl create secret generic my-webhook-token --from-file=my-token=./token.txt
```

```yaml
spec:
  webhook:
    example:
      port: "12000"
      endpoint: /example
      method: POST
      authSecret:
        name: my-webhook-token
        key: my-token
```

Callers send `Authorization: Bearer <token>` (`curl -X POST -H "Authorization: Bearer <token>" -d ... http://host:12000/example`). The docs write the token file with `echo -n`.

Basic auth: create a Secret with `--from-literal=username=... --from-literal=password=...` and reference both keys:

```yaml
      basicAuth:
        username:
          name: my-webhook-basic-auth
          key: username
        password:
          name: my-webhook-basic-auth
          key: password
```

Callers use `curl -u my-username:my-password`. `authSecret` and `basicAuth` are mutually exclusive on a given endpoint.

Both approaches also apply to extended webhook sources that have no built-in authenticator. The feature is marked GA from v1.0.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/eventsources/webhook-authentication.md. Confirmed: v1.0 GA, authSecret and basicAuth examples, Bearer header, curl -u, mutual exclusivity, extended sources without an authenticator. Removed or changed: the stated reason for echo -n and a repeated closing paragraph. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
