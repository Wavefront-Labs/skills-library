---
id: computing-software.messaging-and-integration.apache-pulsar.namespace-isolation-policy
name: namespace-isolation-policy
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [broker-isolation, ns-isolation-policy, primary-secondary, advertised-address, auto-failover-policy]
level: advanced
status: docs-checked
description: "Restrict namespaces to chosen brokers with pulsar-admin ns-isolation-policy set: matching registered broker IDs by regex, primary vs secondary, failover params."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-isolation-broker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pin the bundles of selected namespaces to a defined set of brokers.

A namespace isolation policy limits the brokers eligible for assignment of a namespace's bundles. It uses `--primary` and `--secondary` regular expressions that match the hostname/address part of the registered broker ID, without the port; the expression must match the entire address.

What address is matched:
- `advertisedAddress` configured: that value, even if `advertisedListeners` plus `internalListenerName` advertise a different hostname.
- `advertisedAddress` unset or blank: the local canonical hostname (normally the FQDN).
Listener hostnames never change the isolation matching address. Check what is actually registered before writing the regex:
```shell
pulsar-admin brokers list my-cluster
```
For an ID such as `broker-0.brokers.example.com:8080`, match `broker-0.brokers.example.com`.

Create a policy (example from the page, Kubernetes headless-service names):
```shell
pulsar-admin ns-isolation-policy set production payments-brokers \
  --auto-failover-policy-type min_available \
  --auto-failover-policy-params min_limit=1,usage_threshold=80 \
  --namespaces 'finance/payments' \
  --primary 'pulsar-broker-[01][.]pulsar-broker-headless[.]pulsar[.]svc[.]cluster[.]local' \
  --secondary 'pulsar-broker-([2-9]|1[0-9])[.]pulsar-broker-headless[.]pulsar[.]svc[.]cluster[.]local'
```
The same is available through the REST API and the Java admin API.

Gotcha: brokers matching a policy primary regex are excluded from normal bundle assignment for namespaces without an isolation policy. Secondary brokers stay in the shared pool unless another policy lists them as primary. Do not build the regex from a listener URL.

## Checked

2026-11-03. Confirmed against the pulsar-site page administration-isolation-broker: address matching table, the example command and regexes, broker reservation note and REST/Java availability. Removed the invented Verify step.

Method: documentation only; no commands were run.
