---
id: computing-software.systems-network-administration.icinga-2.certificate-signing-tickets-and-on-demand-csr
name: certificate-signing-tickets-and-on-demand-csr
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, csr, auto-signing, ticket, ticket-salt, ca-list, ca-sign, generate-ticket, pki]
level: advanced
status: docs-checked
description: Sign Icinga 2 node certificates by CSR auto-signing with a ticket from pki ticket or the generate-ticket action, or by on-demand signing with ca list and ca sign.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# certificate signing: tickets and on-demand CSR
All nodes need certificates from the same CA. Two built-in methods avoid manual signing.

**CSR auto-signing.** The client (secondary master, satellite or agent) sends a CSR containing a ticket generated on the master. Advantages: no interaction on the master, automation tools can fetch the ticket. Disadvantages: tickets must be generated and copied, no central signing management. Since v2.8 a satellite can forward signing requests to the master (the "CA Proxy"), which helps three-level clusters.

Preparation on the master: the master setup ran (CA key pair, private ticket salt in the `TicketSalt` constant / `ticket_salt` attribute of the api feature) and the master was restarted.

Get a ticket by the CLI (`icinga2 pki ticket --cn 'agent-fqdn'`) or the REST API with an ApiUser holding `actions/generate-ticket`:
```
object ApiUser "client-pki-ticket" {
  password = "..."
  permissions = [ "actions/generate-ticket" ]
}
```
`POST /v1/actions/generate-ticket` with body `{ "cn": "icinga2-agent1.localdomain" }`. Never expose the ticket salt or ApiUser credentials to client nodes; retrieve the ticket on the master (e.g. Puppet master) and pass only the ticket.

**On-demand signing** (v2.8+). The client sends a CSR without ticket and an admin reviews it. Advantages: central management, no ticket. Disadvantages: asynchronous for automation, needs client verification.
- `icinga2 ca list` shows pending requests (`--all` shows signed too, `--json` for JSON).
- `icinga2 ca sign <fingerprint>` signs one.

## Checked

2026-11-04. Confirmed against the Icinga 2 distributed monitoring chapter: CSR auto-signing, pki ticket, generate-ticket action and permission, CA Proxy since v2.8, on-demand signing, ca list --json, ca sign by fingerprint.

Method: documentation only; no commands were run.
