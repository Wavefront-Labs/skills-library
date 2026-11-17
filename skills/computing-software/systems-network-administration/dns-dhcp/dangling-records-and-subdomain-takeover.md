---
id: computing-software.systems-network-administration.dns-dhcp.dangling-records-and-subdomain-takeover
name: dangling-records-and-subdomain-takeover
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-security, subdomain-takeover, dangling-cname, dangling-dns, cloud-resources, s3-bucket, cname-audit, attack-surface, dns-hygiene]
level: practitioner
status: docs-checked
description: "Find and prevent subdomain takeovers: dangling CNAME records to deleted cloud resources, zone audits, fingerprints and a cleanup process."
sources:
  - https://github.com/EdOverflow/can-i-take-over-xyz
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dangling records and subdomain takeover

## How it happens
A subdomain takeover is possible when a subdomain (for example shop.example.org) points to a service (GitHub Pages, Heroku and so on) whose resource has been removed or deleted, while the DNS record stays. An attacker sets up a resource with the same name on that service, claims the subdomain, and serves their own content under your domain. The can-i-take-over-xyz project catalogues which services are exposed.

## Audit
- Export every zone and list the CNAME records that point at third-party services.
- For each, resolve the target. Two fingerprint types are recorded per service: the target does not resolve (`NXDOMAIN`), or the service returns a specific error page. Examples from the project list: Azure services such as azurewebsites.net (NXDOMAIN, marked vulnerable); AWS S3 ("The specified bucket does not exist", vulnerable); Heroku ("No such app", edge case); GitHub Pages ("There isn't a GitHub Pages site here.", edge case).
  ```
  dig +short CNAME shop.example.org
  dig +short <target-from-above>        # empty or NXDOMAIN on a provider domain = suspect
  curl -sI https://shop.example.org     # compare the page with the service's known error text
  ```
- Statuses change: the list marks some services as not vulnerable (for example CloudFront, Fastly, Zendesk) and others as edge cases needing manual checking, so consult the current list and its linked discussion for the service in question rather than relying on memory.
- The project warns that it does not guarantee accuracy; confirm a suspected takeover yourself before acting.

## Prevent
- Remove the DNS record when you delete the service resource it points to (ideally in the same change or the same infrastructure code).
- Some services have added domain-ownership verification to block takeovers (the list notes this for Statuspage); use it where offered.
- Review the zone regularly for records whose targets no longer resolve.

## Verify
- [ ] Zone audit shows no CNAME whose target is NXDOMAIN or shows a provider "not found" page.
- [ ] Deprovisioning steps include removing the DNS record.

## Checked
Method: docs-checked 2026-11-09 against the can-i-take-over-xyz README (definition and full engine table), read in full. The Microsoft Learn source is not fetchable and was dropped. Removed the A-record and NS-takeover claims, named scanner tools, Azure asuid and CloudFront verification features, and the wildcard CNAME advice as not confirmed there, and corrected CloudFront and Fastly, which the list marks as not vulnerable.
