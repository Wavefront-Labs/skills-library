---
id: computing-software.cloud-infrastructure-engineering.external-dns.headless-service-hostport-records
name: headless-service-hostport-records
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, headless-service, hostport, kafka-statefulset, per-pod-records]
level: practitioner
status: docs-checked
description: "Publish per-pod and root records for a headless Service (Kafka example) with hostPort, hostname annotation or fqdn-template, and the resulting record sets."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/hostport.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headless Services with hostPort

Use case: fixed addressable hostnames for something like Kafka reached from outside the cluster, where often only node IPs are routable and direct connections are preferred.

**Pod side:** set `hostPort` on the container (works only if the PodSecurityPolicy allows it). If the app needs a real hostname inside the container, set it yourself; Kafka can instead advertise another address (the example advertises `$HOSTNAME.example.org:9092`).

**Two ways to expose a headless Service** (`clusterIP: None`, `serviceName: ksvc` on the StatefulSet):
1. Start ExternalDNS with `--fqdn-template={{ .Name }}.example.org` and no annotation.
2. Annotate the Service: `external-dns.kubernetes.io/hostname: example.org`.

**Result with annotation** (4 records): `kafka-0.example.org`, `kafka-1.example.org`, `kafka-2.example.org` each to its own IP, plus the root `example.org` to all three IPs. Note the root domain record.

**Result with the template:** `kafka-0.ksvc.example.org`, `kafka-1.ksvc.example.org`, `kafka-2.ksvc.example.org`, plus `ksvc.example.org` to all IPs.

**Choosing targets**
- `external-dns.kubernetes.io/endpoints-type: HostIP` on the Service publishes each backing pod's `.status.hostIP`.
- `endpoints-type: NodeExternalIP` publishes the node's `NodeExternalIP` address for each pod's node.
- `external-dns.kubernetes.io/target: "1.2.3.4"` on the **pods** publishes that IP instead of the podIP; useful when NATing public IPs onto pod IPs.

The example deployment uses `--source=service`, `--registry=txt` and `--txt-owner-id`.

## Checked

2026-11-04. Confirmed against the ExternalDNS Headless Services tutorial: use case, hostPort note, the two exposure approaches, both record sets, endpoints-type values and the pod target annotation. Nothing removed.
Method: documentation only; no commands were run.
