---
id: computing-software.messaging-and-integration.dapr.mtls-root-certificate-expiry-monitoring
name: mtls-root-certificate-expiry-monitoring
category: computing-software
field: messaging-and-integration
product: dapr
tags: [mtls, monitoring, certificate-expiry, sentry, logs, dapr-status, alerting]
level: practitioner
status: docs-checked
description: "Alert on Dapr root certificate expiry: Sentry emits hourly warning logs for 30 days before expiry, the exact messages to match, and dapr status -k printing expiry warnings."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/security/mtls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Self-signed Dapr certs last one year, so expiry is a production hazard. Beginning 30 days before the mTLS root certificate expires, the Sentry service emits warning-level logs every hour. The page recommends alerting on these log lines:

```bash
"Dapr root certificate expiration warning: certificate expires in 2 days and 15 hours"
```

and once expired:

```bash
"Dapr root certificate expiration warning: certificate has expired."
```

Read them on Kubernetes with:

```bash
kubectl logs deployment/dapr-sentry -n dapr-system
```

The structured output carries `"level":"warning"` and `"scope":"dapr.sentry"` fields alongside the message.

Since release 1.7.0 the CLI also prints expiry status whenever you interact with a Kubernetes deployment. `dapr status -k` lists operator, placement, dashboard, sentry, scheduler (3 replicas in the example) and injector, then ends with a warning line such as "Dapr root certificate of your Kubernetes cluster expires in 2 days. Expiry date: ..." pointing you to the renewal instructions.

Action when warned: follow the rotation procedure (CLI `dapr mtls renew-certificate -k` or Helm upgrade), keeping the same root key when possible to avoid downtime.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
