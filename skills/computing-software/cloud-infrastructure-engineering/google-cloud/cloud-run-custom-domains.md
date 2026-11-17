---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-run-custom-domains
name: cloud-run-custom-domains
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run, cloud-run-custom-domains, domain-mapping, serverless-neg, managed-certificates, firebase-hosting]
level: practitioner
status: docs-checked
description: "Put a custom domain on Cloud Run: global external load balancer with serverless NEG and managed cert (production), domain mappings (limited), or Firebase Hosting rewrites."
sources: ["https://docs.cloud.google.com/run/docs/mapping-custom-domains", "https://docs.cloud.google.com/load-balancing/docs/https/setup-global-ext-https-serverless", "https://docs.cloud.google.com/certificate-manager/docs/deploy-google-managed-lb-auth", "https://firebase.google.com/docs/hosting/cloud-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Run custom domains

| Option | When | Notes |
|---|---|---|
| Global external Application LB + serverless NEG | production (the recommended option) | own or Google-managed certs, URL path routing, Cloud CDN, Cloud Armor |
| Cloud Run domain mappings | quick tests | preview launch stage, not recommended for production, limited regions, root path `/` only, no wildcard or self-managed certificates |
| Firebase Hosting rewrite | static site + API | Hosting rewrites route requests to a Cloud Run service (colocate the service in a Hosting-supported region) |

## 1. Load balancer (recommended)
```bash
gcloud compute addresses create orders-ip --global
gcloud compute network-endpoint-groups create orders-neg --region=europe-west2 \
  --network-endpoint-type=serverless --cloud-run-service=orders
gcloud compute backend-services create orders-bes --global --load-balancing-scheme=EXTERNAL_MANAGED
gcloud compute backend-services add-backend orders-bes --global \
  --network-endpoint-group=orders-neg --network-endpoint-group-region=europe-west2
gcloud compute url-maps create orders-um --default-service=orders-bes
gcloud certificate-manager certificates create orders-cert --domains=api.example.com   # load balancer authorization needs no extra DNS records
gcloud certificate-manager maps create orders-map
gcloud certificate-manager maps entries create orders-entry --map=orders-map --hostname=api.example.com --certificates=orders-cert
gcloud compute target-https-proxies create orders-px --global --url-map=orders-um --certificate-map=orders-map
gcloud compute forwarding-rules create orders-fr --global --load-balancing-scheme=EXTERNAL_MANAGED \
  --address=orders-ip --target-https-proxy=orders-px --ports=443
```
DNS: `A api.example.com → orders-ip`. Then restrict the service:
`gcloud run services update orders --ingress=internal-and-cloud-load-balancing`.

## 2. Domain mapping (simple)
```bash
gcloud domains verify example.com                       # verify the base domain first
gcloud beta run domain-mappings create --service=orders --domain=api.example.com --region=<R>
gcloud beta run domain-mappings describe --domain=api.example.com --region=<R>   # DNS records to add
```
Provisioning the certificate usually takes about 15 minutes but can take up to 24 hours. Mappings are available only in the regions listed on the domain-mapping page.

## Gotchas
- Managed certs only issue once DNS points at the load balancer (or the DNS authorization record is in place).
- Leaving ingress `all` with an LB in front lets clients bypass Armor via `run.app`; Google recommends ingress `internal-and-cloud-load-balancing` and optionally disabling the default URL.
- Domain mappings are a preview feature, are not available in every region and are not recommended for production.

## Verify
- [ ] `curl -I https://api.example.com` returns the service response with a valid Google-issued cert.
- [ ] `curl https://orders-<hash>.a.run.app` is rejected when ingress is restricted.

## Checked

2026-10-24, Cloud Run domain-mapping, global external Application Load Balancer serverless setup and Certificate Manager load-balancer-authorization pages as served on docs.cloud.google.com. Confirmed: domain mappings are in the preview launch stage and not recommended for production; certificate provisioning time (about 15 minutes, up to 24 hours); the gcloud commands and flags for the NEG, backend service, URL map, Certificate Manager certificate, map and map entry, and target proxy (`--certificate-map`, `--global`); the recommendation to set ingress to internal and Cloud Load Balancing. Removed unconfirmed claims about CAA records, Firebase CDN pricing and the `/api/**` rewrite pattern.

Method: documentation only; no commands were run.
