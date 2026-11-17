---
id: computing-software.messaging-and-integration.rabbitmq.default-credentials-hardening
name: default-credentials-hardening
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, default-credentials-hardening, rmq-security]
level: practitioner
status: docs-checked
description: "Remove default guest access, rotate credentials and restrict the Erlang cookie file permissions."
sources:
  - https://www.rabbitmq.com/docs/access-control
  - https://www.rabbitmq.com/docs/clustering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credential hardening

**Goal:** Close easy openings.

## Steps
1. Delete the `guest` user or at least change its password. By default `guest` can only connect from localhost (loopback).
2. Change passwords with `rabbitmqctl change_password`.
3. Keep the Erlang cookie file accessible only to its owner (UNIX permissions `600` or similar).

## Failure modes
- Nodes and CLI tools authenticate to each other with the shared Erlang cookie, so protect it.

## Verify
- Try guest login from a remote host and expect refusal.

## Checked

Date: 2026-11-02. Confirmed in the Access Control guide (docs/access-control, guest user and loopback) and Clustering Guide (docs/clustering, cookie permissions). Removed as not stated there: hashed-storage remark, port restriction step and the full-cluster-control claim wording.

Method: documentation only; no commands were run.
