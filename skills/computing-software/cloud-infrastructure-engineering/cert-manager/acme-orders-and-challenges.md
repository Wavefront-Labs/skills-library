---
id: computing-software.cloud-infrastructure-engineering.cert-manager.acme-orders-and-challenges
name: acme-orders-and-challenges
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [order, challenge, max-concurrent-challenges, self-check, scheduler, acme-lifecycle]
level: advanced
status: docs-checked
description: "Understand ACME Order and Challenge resources: creation, immutability, the nine-step Challenge lifecycle, the 60-challenge concurrency limit and scheduling conflicts."
sources:
  - https://cert-manager.io/docs/concepts/acme-orders-challenges/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Orders: created automatically when a CertificateRequest references an ACME issuer (requests come from a Certificate being created, changed or due for renewal). Users never create them, and they are immutable; to change one, create a new Order. An Order holds one Challenge per DNS name being authorized.

Challenges: complete the authorization for one DNS name; created by the order controller, immutable.

Lifecycle:
1. Created and queued.
2. Scheduled; work starts only once the scheduler allows it.
3. Synced with the ACME server; if already valid, `status.state` becomes valid and `status.processing` false.
4. If pending, presented through the HTTP01 or DNS01 solver; `status.presented` true.
5. Self-check verifies propagation.
6. A failing self-check retries every fixed 10 seconds, indefinitely, until you intervene.
7. After it passes, the authorization is accepted.
8. The final authorization state and any error reason are copied to `status.state`.
9. On valid, invalid, expired or revoked, `status.processing` goes false, freeing a slot.

Scheduling: default 60 concurrent Challenges. Set `--max-concurrent-challenges`, Helm `maxConcurrentChallenges`, or the ControllerConfiguration key. Conflicts are by validated target: same hostname for HTTP01, same `_acme-challenge` DNS name for DNS01; different ingress classes, routes or DNS backends do not make them independent. The scheduler does not model CA rate limits, tenant fairness or name ownership; use policy, admission, approval or separate deployments.

Debugging: read `status.processing`, `status.presented`, `status.state` and the reason. A Challenge stuck in self-check needs a configuration fix, or delete the Order to retry. Cleanup commands are not given on the page.

## Checked

2026-11-03. Confirmed on the cert-manager ACME Orders and Challenges page (concepts/acme-orders-challenges): Order and Challenge immutability, lifecycle steps, fixed 10 second self-check retry, 60 concurrent challenges default and the three ways to change it, conflict rules and scheduler limits. Nothing removed.
Method: documentation only; no commands were run.
