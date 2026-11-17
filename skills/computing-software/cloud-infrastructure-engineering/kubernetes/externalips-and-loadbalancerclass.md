---
id: computing-software.cloud-infrastructure-engineering.kubernetes.externalips-and-loadbalancerclass
name: externalips-and-loadbalancerclass
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, services, externalips, loadbalancerclass, denyserviceexternalips, cve-2020-8554]
level: practitioner
status: docs-checked
description: "Use Service externalIPs and loadBalancerClass correctly, and block the externalIPs traffic-interception risk with DenyServiceExternalIPs or policy."
sources: ["https://kubernetes.io/docs/concepts/services-networking/service/#external-ips", "https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-class", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#denyserviceexternalips"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# externalIPs and loadBalancerClass

## externalIPs
Deprecated in Kubernetes 1.36; the Service documentation tells all users to start migrating away
from `externalIPs` (use an external load balancer controller or a Gateway API implementation).
```yaml
spec:
  type: ClusterIP
  externalIPs: [198.51.100.32]
  ports: [{port: 80, targetPort: 8080}]
```
Traffic that arrives in the cluster with that destination IP and a matching port is routed to the
Service's endpoints. Kubernetes does not manage allocation of `externalIPs`; routing the address to
a node is the cluster administrator's job.

### The risk
`externalIPs` allows network traffic interception and is not well controlled by policy. The
`DenyServiceExternalIPs` validating admission controller rejects all net-new usage: users cannot
create Services using `externalIPs` or add new values on existing Services, existing uses are
unaffected and values can still be removed. Enable it with kube-apiserver
`--enable-admission-plugins`, or restrict values with a policy engine.
Audit existing use:
```bash
kubectl get svc -A -o yaml
```
and look for `spec.externalIPs`.

## loadBalancerClass
Selects a load balancer implementation other than the cloud provider default for a
`type: LoadBalancer` Service:
```yaml
spec:
  type: LoadBalancer
  loadBalancerClass: example.com/internal-vip
```
- Unset (the default): the cloud provider's default implementation is used.
- Set: the default implementation (the cloud provider) ignores the Service; an implementation
  matching the class is assumed to be watching for it.
- Valid only on `type: LoadBalancer`; once set it cannot be changed. Recreate the Service to
  change it. The value is a label-style identifier with an optional prefix.
- The class names are defined by each controller; read its documentation.

## Verify
`kubectl get svc <name> -o jsonpath='{.status.loadBalancer.ingress}'` is populated by the intended
controller (check its logs and events), and no unexpected `externalIPs` exist.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Service concept page (externalIPs deprecated in v1.36, not managed by Kubernetes, loadBalancerClass semantics, immutability and value syntax) and the admission controllers reference (DenyServiceExternalIPs behaviour). Removed the CVE number claim, the jq pipeline, the AWS class example and the claim about a permanent pending state.

Method: documentation only; no commands were run.
