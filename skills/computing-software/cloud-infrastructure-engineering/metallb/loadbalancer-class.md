---
id: computing-software.cloud-infrastructure-engineering.metallb.loadbalancer-class
name: loadbalancer-class
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, lb-class, loadbalancerclass, speaker, controller, helm]
level: advanced
status: docs-checked
description: "Make MetalLB handle only Services with a given LoadBalancerClass so several load balancer implementations can coexist, via --lb-class on speaker and controller."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LoadBalancerClass

MetalLB supports Kubernetes `LoadBalancerClass`, which lets multiple load balancer implementations co-exist in one cluster.

To choose the class MetalLB listens for, pass the parameter to both components:
```
--lb-class=<CLASS_NAME>
```
- It must be given to the speaker and the controller.
- With Helm, set the `loadBalancerClass` parameter instead of editing args.

The MetalLB page links the Kubernetes Service documentation for LoadBalancerClass; it does not describe how Services select a class or what happens to Services without one.

## Checked

2026-11-04. Confirmed against the MetalLB Installation page (Setting the LoadBalancer Class: `--lb-class=<CLASS_NAME>` on both speaker and controller, Helm `loadBalancerClass`). Removed the Service-side field claim and the Verify paragraph, which the page does not state.

Method: documentation only; no commands were run.
