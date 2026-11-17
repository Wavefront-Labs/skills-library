---
id: computing-software.cloud-infrastructure-engineering.cilium.lb-ipam-service-allocation
name: lb-ipam-service-allocation
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, lb-ipam, loadbalancer, lbipam-cilium-io-ips, sharing-key, loadbalancerclass]
level: practitioner
status: docs-checked
description: "Request and share LoadBalancer IPs with lbipam.cilium.io/ips and sharing-key, set IP family policy, use loadBalancerClass or defaultLBServiceIPAM."
sources:
  - https://docs.cilium.io/en/stable/network/lb-ipam/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LB IPAM service allocation

## Diagnose pending
A LoadBalancer Service with `EXTERNAL-IP <pending>` has no IP. Read `kubectl -n example get svc/service-red -o jsonpath='{.status.conditions}'`: condition type `io.cilium/lb-ipam-request-satisfied` with reason `no_pool` and message "There are no enabled CiliumLoadBalancerIPPools that match this service" means labels do not match any pool selector; fix labels and it flips to reason `satisfied`.

## IP families
`.spec.ipFamilyPolicy` default SingleStack (IPv4 when both enabled). `PreferDualStack` tries both but is satisfied with one family. `RequireDualStack` is unsatisfied if either family is disabled. `.spec.ipFamilies` order does not matter to LB IPAM.

## loadBalancerClass
LB IPAM allocates for services with no class. It does not load balance; use `io.cilium/bgp-control-plane` or `io.cilium/l2-announcer`. A service with some other class is ignored entirely, no condition set. To allocate only for recognised classes, set Helm `defaultLBServiceIPAM=none` (ConfigMap `default-lb-service-ipam: none`).

## Requesting IPs
Annotation `lbipam.cilium.io/ips: "20.0.10.100,20.0.10.200"` (comma list). Legacy `.spec.loadBalancerIP` is deprecated since k8s 1.24. The pool selector still applies. Do not request the first or last IP of a pool.

## Sharing
Services with the same annotation `lbipam.cilium.io/sharing-key` (any string) share IPs. Not supported with L2 announcements (independent per-service node elections).

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the LB IPAM page: https://docs.cilium.io/en/stable/network/lb-ipam/. Confirmed the pending diagnosis, IP family policy, loadBalancerClass, requested IP annotation and sharing key statements above. Nothing was removed.

Method: documentation only; no commands were run.
