---
id: computing-software.cloud-infrastructure-engineering.ansible.eda-event-streams
name: eda-event-streams
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, event-driven-ansible, event-streams, eda-controller, webhooks, hmac, rulebook-activation, aap-2-5]
level: advanced
status: docs-checked
description: "Receive webhooks in AAP through EDA event streams: stream types, credentials, creating a stream, forwarding toggle for testing, source mapping onto an activation."
sources: ["https://github.com/ansible/aap-docs/blob/main/downstream/modules/eda/con-event-streams.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/eda/proc-eda-create-event-stream.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/eda/proc-eda-create-event-stream-credential.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/eda/proc-eda-replace-sources-with-event-streams.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/eda/proc-eda-event-streams-not-sending-events.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EDA event streams

Goal: external systems post events to one authenticated endpoint on the platform and rulebook activations consume them, instead of exposing a port per activation.

## What an event stream is
An event stream is the secure, authenticated entry point for external systems to send events over the internet directly to Event-Driven Ansible. One stream can be attached to several rulebook activations.

## Types
Six basic types: HMAC (shared secret, message integrity; GitHub), Basic authentication (Datadog, Dynatrace), Token authentication (an `Authorization` header by default, customizable such as `X-Gitlab-Token`; GitLab, ServiceNow), OAuth2 (client-credentials, opaque token), OAuth2 with JWT (Datadog), ECDSA (sender signs with a private key; SendGrid, Twilio), and mTLS (certificate or subject sub-types; PagerDuty). Specialized GitLab, GitHub, ServiceNow and Dynatrace types are built on these and pre-fill defaults (GitHub is a specialization of HMAC).

mTLS behind a load balancer needs SSL pass-through (or L4 routing), because TLS termination and client-certificate validation must happen at the platform gateway proxy.

## 1. Credential
Platform Credentials → Create credential, choose the event stream credential type, fill the Type Details (for the GitHub type, an HMAC secret shared with the sender). Each event stream has exactly one credential, and a credential cannot be deleted while a stream uses it.

## 2. Event stream
Automation Decisions → Event Streams → Create event stream. Fields: Name, Organization, Event stream type, Credentials, Headers (HTTP header keys, comma-separated, to include in the event payload; define them explicitly so sensitive headers are not exposed), and Forward events to rulebook activation. Disable forwarding while diagnosing: you can test the connection, inspect the header and payload and diagnose credential issues without triggering rules. You can toggle it any time. Creating the stream generates the URL to configure in the sender's webhook. The list shows Events received, Last event received and Event stream type.

## 3. Attach to a rulebook activation
When creating the activation, select the rulebook, then use the Event streams gear icon to map a rulebook source (unnamed sources appear as `__SOURCE_{n}`) to a stream.
- Replacement affects that activation only; it changes the source type, name and arguments, while filters, rules, conditions and actions are unchanged. Webhook-type sources such as `ansible.eda.webhook` can be replaced.
- A stream can be used once per source swap; mappings are lost if the rulebook is modified, and a restart then fails.
- Repeat the mapping for every activation that uses the rulebook.

A rulebook for the stream still looks like a normal source plus rules, for example a condition on `event.payload.action == "opened"` for GitHub.

## Troubleshooting events that do not arrive
Check the stream is not in test mode (forwarding off), the sender is sending correctly, the network path to the gateway, the gateway proxy and the event stream worker are up, the credential matches the request's authentication mechanism (for example HMAC needs a signature header), and the rulebook has rules consuming the events. Credentials changed in the platform must also be changed in the sender. With self-signed certificates, vendors usually offer a non-production option to skip certificate validation.

## Verify
- [ ] The stream's Events received and Last event received update after a sender test.
- [ ] With forwarding on, the activation's rule audit shows the rule fired.

## Checked
2026-11-09. Checked against ansible/aap-docs EDA modules: event streams concept, creating an event stream, creating an event stream credential, replacing sources with event streams, and event streams not sending events.
Removed as unsupported: the stream URL shape, "gateway terminates HTTPS" and "AAP 2.5+" statements, ServiceNow/Dynatrace "presets" row detail, the GitHub webhook-form walk-through, `event.meta.headers`, duplicate-launch and rotation gotchas, and the 401/403 rejection verify step.
Method: documentation only; no commands were run.
