---
id: computing-software.web-development.appwrite.appwrite-sites-domains-dns
name: appwrite-sites-domains-dns
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, sites, domains, dns, vercel-migration]
level: practitioner
status: docs-checked
description: "Attach custom domains to a site with the right rule type and DNS records for apex and subdomains, including Vercel migration notes."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/domains/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/migrations/vercel/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve a site on your own domain.

Rule types: Active deployment (serves the current active deployment), Git branch (serves the latest deployment of a branch), and Redirect (send traffic to another URL). Redirect statuses are 301, 302, 303, 307 and 308; the path and query are ignored.

DNS:
- Subdomains: add a CNAME record to the target shown in the Console.
- Apex domains: either point nameservers to `ns1.appwrite.zone` and `ns2.appwrite.zone`, or use CNAME flattening (ALIAS/ANAME) with a CAA record allowing the certificate authority.
Verification and certificates are shown in the Console after DNS propagates.

Migrating from Vercel: apex domains need NS records instead of the A records Vercel used, and because nameservers move wholesale, recreate other records such as MX at the new DNS service so email keeps working.

Gotcha: when nameservers move to Appwrite DNS, existing records such as MX must be recreated in Appwrite DNS.

Use a Git branch rule to give a staging branch its own domain, and a Redirect rule to send a bare domain to the canonical one.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/sites/domains, products/sites/migrations/vercel. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the invented Verify and the note that rules can be added or removed without redeploying; dropped "first" from the Vercel MX advice; Gotcha reworded neutrally.

Method: documentation only; no commands were run.
