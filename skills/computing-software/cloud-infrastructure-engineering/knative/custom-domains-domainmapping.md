---
id: computing-software.cloud-infrastructure-engineering.knative.custom-domains-domainmapping
name: custom-domains-domainmapping
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [config-domain, custom-domain, dns]
level: practitioner
status: docs-checked
description: "Set the default cluster domain with config-domain and publish it through DNS."
sources:
  - https://knative.dev/docs/serving/using-a-custom-domain/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve Services on your own domain names.

The default fully qualified route domain is `{route}.{namespace}.svc.cluster.local`.

Default domain for all Services: edit the `config-domain` ConfigMap in `knative-serving` and replace `svc.cluster.local` with your domain, for example `knative.dev`. Existing deployments are reconciled: Knative updates the host name of deployed Services and Routes. Verify by deploying an app, retrieving the Route URL and observing the new domain. Publishing the domain also needs DNS pointing at your cluster.

Single Service: the page points to the DomainMapping documentation for customising the domain of an individual Service; that page was not fetched here, so DomainMapping details are not covered.

Publish the domain: update your DNS provider to point at the ingress IP address. A wildcard record for the namespace and domain (for example `*.default.knative.dev`) covers several Services in the namespace; otherwise create an A record from each fully qualified domain name to the Knative gateway IP, per Service or Route.

## Checked

2026-11-03. Confirmed on the Knative Serving using-a-custom-domain page: the default route domain, config-domain procedure, reconciliation and DNS publishing. Removed: the DomainMapping, ClusterDomainClaim and autocreate-cluster-domain-claims details (page only links to DomainMapping docs).
Method: documentation only; no commands were run.
