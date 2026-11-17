---
id: computing-software.cloud-infrastructure-engineering.cert-manager.troubleshooting-acme
name: troubleshooting-acme
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [troubleshooting, acme, letsencrypt, order, challenge, self-check, temporary-certificate]
level: practitioner
status: docs-checked
description: "Debug a failing ACME or Let's Encrypt certificate in order: Issuer, Order, Challenge, then HTTP01 or DNS01 specifics, with the known error strings."
sources:
  - https://cert-manager.io/docs/troubleshooting/acme/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Walk the chain in order.

1. Issuer: `kubectl get issuer|clusterissuer` should be READY True; otherwise `kubectl describe` it. Known errors: `invalidEmail` (fix `spec.acme.email`); `secrets "acme-key" already exists` (delete the leftover Secret); `authorization must be pending` (authorization already failed or expired, check its URL).
2. Order: `kubectl describe certificaterequest <name>` for `OrderCreated`, then `kubectl describe order <name>` (State `pending` or `valid`; success event `OrderValid`). Authorization URL: `kubectl get order <order> -ojsonpath='{.status.authorizations[x].url}'`. Errors: `unknown field "spec.acme.profile"` needs v1.18.0+; "does not advertise a profile with name" and "does not support profiles" point at the server.
3. Challenges: `kubectl get challenges`, `kubectl describe challenge <name>` (Presented, Processing, Reason, State, events). URL: `kubectl get challenge <name> -ojsonpath='{.spec.authorizationURL}'`.

HTTP01: confirm the challenge URL is publicly reachable and test from inside a Pod. If the ACME server reaches it but the self-check cannot (NAT loopback, split-horizon DNS), use `waitInsteadOfSelfCheck`. `tls: handshake failure`: set `cert-manager.io/issue-temporary-certificate: "true"`. Controllers fighting over a hostname: `acme.cert-manager.io/http01-edit-in-place: "true"`. 404: check the solver Pod and `kubectl describe ingress`. 503 on OpenShift's router: the solver Ingress uses `pathType: Exact` and is not converted to a Route.

DNS01: check the `_acme-challenge.<domain>` TXT record exists. Visible publicly but not in-cluster: change the self-check nameservers. Wrong zone detected: cert-manager relies on SOA records; resolvers that filter them (dnsmasq `--filterwin2k`) break it.

## Checked

2026-11-03: Confirmed against the ACME troubleshooting page: Issuer READY checks and the three common errors, Order describe flow with `OrderCreated`, `OrderValid` and the authorization URL query, the profile errors and v1.18.0 requirement, Challenge describe fields and URL query, `waitInsteadOfSelfCheck`, `tls: handshake failure` with `cert-manager.io/issue-temporary-certificate`, `http01-edit-in-place`, the 404 and OpenShift 503 `pathType: Exact` cases, and the DNS01 SOA/dnsmasq `--filterwin2k` zone detection issue. Nothing removed.

Method: documentation only; no commands were run.
