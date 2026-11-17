---
id: computing-software.cloud-infrastructure-engineering.kubernetes.external-dns-record-publishing
name: external-dns-record-publishing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, coredns, external-dns, ingress, service, dns]
level: practitioner
status: docs-checked
description: "Publish DNS records for Ingresses, Gateways and LoadBalancer Services with ExternalDNS: providers, ownership TXT registry, domain filters and safe policies."
sources: ["https://kubernetes-sigs.github.io/external-dns/latest/", "https://github.com/kubernetes-sigs/external-dns/blob/master/charts/external-dns/README.md", "https://github.com/kubernetes-sigs/external-dns/blob/master/docs/annotations/annotations.md", "https://github.com/kubernetes-sigs/external-dns/blob/master/docs/registry/txt.md", "https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExternalDNS

ExternalDNS watches Kubernetes sources and writes records to a DNS provider (Route 53, Cloud
DNS, Azure DNS, Cloudflare, RFC2136 and others).

## Install (Route 53 example)
```bash
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm install external-dns external-dns/external-dns -n external-dns --create-namespace \
  --set provider.name=aws \
  --set 'sources={service,ingress,gateway-httproute}' \
  --set 'domainFilters={example.com}' \
  --set policy=upsert-only \
  --set registry=txt --set txtOwnerId=prod-eu-1 \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=arn:aws:iam::111122223333:role/external-dns
```
IAM needs `route53:ChangeResourceRecordSets`, `route53:ListResourceRecordSets` and `route53:ListTagsForResources` on the hosted zones, and `route53:ListHostedZones` (per the AWS tutorial).

## Sources
- Ingress: hosts from `spec.rules[].host`, target from `status.loadBalancer`.
- Service type LoadBalancer: annotation `external-dns.kubernetes.io/hostname: api.example.com`
  (the default prefix is `external-dns.kubernetes.io/`; releases before v0.22.0 used
  `external-dns.alpha.kubernetes.io/`, which now needs `--enable-legacy-annotation-prefix`).
- Gateway API routes: hostnames from the route, target from the parent Gateway address.
- Per-object TTL: `external-dns.kubernetes.io/ttl: "60"` (a duration or integer seconds; `0` means use the default).

## Ownership and safety
- TXT registry records which cluster (`txtOwnerId`) owns each record; ExternalDNS never touches
  records owned by others. Unique owner ID per cluster.
- The chart requires `policy` to be set explicitly (`create-only`, `sync` or `upsert-only`).
  `upsert-only` never deletes; `sync` deletes records whose sources are gone (cleaner,
  riskier). Start with upsert-only; never share one owner id across clusters in a zone where
  any cluster runs `sync`.
- `domainFilters` / `zoneIdFilters` keep it out of zones it must not manage.

## Verify
```bash
kubectl -n external-dns logs deploy/external-dns | grep -E 'Desired change|CREATE|UPSERT' | tail
dig +short app.example.com
```
No changes logged: check the source is included and the hostname falls inside domainFilters.

## Checked
2026-10-26. Checked against the external-dns docs source (repository kubernetes-sigs/external-dns, last commit 2026-10-25). Confirmed: Helm repository URL, `provider.name`, `sources`, `domainFilters`, `registry` (default txt), `txtOwnerId`, and that the chart's `policy` value has no default and must be set to create-only, sync or upsert-only; `serviceAccount.annotations`; the Route 53 permissions `route53:ChangeResourceRecordSets`, `ListResourceRecordSets`, `ListTagsForResources` and `ListHostedZones`; unique TXT owner id per cluster; `gateway-httproute` source. Corrected: annotations use the prefix `external-dns.kubernetes.io/` by default; the old `external-dns.alpha.kubernetes.io/` prefix applied before v0.22.0 and is honoured now only with `--enable-legacy-annotation-prefix`. TTL accepts a duration or integer seconds.
Method: documentation only; no commands were run.
