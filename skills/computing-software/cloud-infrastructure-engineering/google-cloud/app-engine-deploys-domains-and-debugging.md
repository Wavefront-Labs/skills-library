---
id: computing-software.cloud-infrastructure-engineering.google-cloud.app-engine-deploys-domains-and-debugging
name: app-engine-deploys-domains-and-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, app-engine, gcloud-app-deploy, app-engine-deploy, app-engine-custom-domains, app-engine-ssl, app-engine-logs, app-engine-debugging, traffic-splitting]
level: practitioner
status: docs-checked
description: "Operate App Engine apps: versioned deploys with no-promote and traffic splits, custom domains with managed SSL, and reading logs and debugging instances."
sources: ["https://cloud.google.com/appengine/docs/standard/testing-and-deploying-your-app", "https://cloud.google.com/appengine/docs/standard/mapping-custom-domains", "https://cloud.google.com/appengine/docs/standard/writing-application-logs", "https://cloud.google.com/sdk/gcloud/reference/app"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Engine deploys, domains and debugging

## 1. Deploy without risk
```bash
gcloud app deploy app.yaml --version=v2026-10-16-1 --no-promote --quiet
gcloud app browse --version=v2026-10-16-1            # https://v2026-10-16-1-dot-<P>.<region>.r.appspot.com
gcloud app services set-traffic default --splits=v2026-10-16-1=0.1,v2026-10-09-1=0.9 --split-by=cookie
gcloud app services set-traffic default --splits=v2026-10-16-1=1 --migrate   # full cutover, migrated gradually
```
Other config files deploy separately: `gcloud app deploy dispatch.yaml cron.yaml index.yaml`.
Rollback = `set-traffic` back to the previous version (keep it until the new one is proven).
Prune: `gcloud app versions list --service=default`, then `gcloud app versions delete` the old ones.

## 2. Custom domains and SSL
```bash
gcloud domains verify example.com
gcloud app domain-mappings create www.example.com --certificate-management=automatic
gcloud app domain-mappings describe www.example.com     # DNS records to create (A, AAAA or CNAME)
```
Verify the naked domain (`example.com`) even when mapping only a subdomain. Mapped domains get a managed certificate by default. Own certs:
`gcloud app ssl-certificates create --certificate=cert.pem --private-key=key.pem` then
`gcloud app domain-mappings create <DOMAIN> --certificate-management=manual --certificate-id=<ID>`.
Custom domains use a shared pool of IP addresses. If you front App Engine with Cloud Load Balancing and a serverless NEG, map the domain to the load balancer and use ingress controls so traffic cannot bypass it.

## 3. Logs and debugging
```bash
gcloud app logs tail -s default
gcloud app logs read --service=default --version=v2026-10-16-1 --level=error --limit=100
```
`--level` filters by severity (`critical`, `error`, `warning`, `info`, `debug`, `any`) and `--limit` defaults to 200.
Write each structured log as a single line of serialized JSON to stdout or stderr so Logs Explorer can filter by severity; the Cloud Logging client library path does not support structured logging.
SSH debugging is a flexible-environment feature: `gcloud app instances ssh <INSTANCE> --service=default --version=<V>`.

## Gotchas
- `gcloud app deploy` promotes the new version by default (the `app/promote_by_default` property); pass `--no-promote` to keep traffic where it is.
- `--split-by` accepts `cookie`, `ip` or `random` (default `ip`). IP splitting is not permanent per user and is only approximate at low traffic; cookie splitting (`GOOGAPPUID`) is more precise, but internal requests must forward the user's cookie.

## Verify
- [ ] `gcloud app versions list --service=default` shows the expected traffic split.
- [ ] `https://www.example.com` serves with a valid certificate.

## Checked
2026-10-27. Confirmed against App Engine testing-and-deploying, splitting-traffic, mapping-custom-domains and writing-application-logs pages; gcloud reference for app deploy (promote default, --no-promote), services set-traffic (--split-by choices and default, --migrate), domain-mappings create (--certificate-management values automatic/manual), logs read and tail (--level, --limit default) and instances ssh. Removed: queue.yaml deploy, stopped-version cost claim, version cap, versions-list filter expression, ghs.googlehosted.com hostname, domain-mappings update, Logs Explorer filter and request-log names, disable-debug, instance-class cost and region claims. Corrected: certificate-management values are lowercase.
Method: documentation only; no commands were run.
