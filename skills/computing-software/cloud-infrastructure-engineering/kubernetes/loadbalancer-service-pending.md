---
id: computing-software.cloud-infrastructure-engineering.kubernetes.loadbalancer-service-pending
name: loadbalancer-service-pending
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshoot-networking, loadbalancer-pending, loadbalancer, metallb, cloud-controller-manager]
level: practitioner
status: docs-checked
description: "Fix a LoadBalancer Service stuck with EXTERNAL-IP pending: missing cloud controller or MetalLB, quotas, subnet tags, annotations and controller events."
sources: ["https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer", "https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/deploy/subnet_discovery/", "https://metallb.universe.tf/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LoadBalancer stuck in pending

```bash
kubectl get svc web            # EXTERNAL-IP <pending>
kubectl describe svc web       # read the Events section
```

## No events at all
Nothing implements LoadBalancer:
- Setting `type: LoadBalancer` on a cloud provider that supports external load balancers makes
  the cloud-controller-manager configure the external balancer. On bare metal, or in a cluster
  without a cloud provider, install a LoadBalancer implementation such as MetalLB, or use NodePort.
- `spec.loadBalancerClass` is set to a class that no controller handles: the default
  implementation ignores Services that set it, and an implementation matching the class is
  assumed to be watching.

## Events with errors
| Cause | Where to look |
|---|---|
| AWS Load Balancer Controller cannot discover subnets | subnets need the tag `kubernetes.io/role/elb` (public) or `kubernetes.io/role/internal-elb` (internal) with value `1` or empty; see the controller's subnet discovery page |
| quota or permission errors | the cloud provider's limits and the controller's credentials |
| annotation errors | the annotation reference of the controller you use |
| MetalLB assigns no address | an `IPAddressPool` must exist with free addresses |
| MetalLB address assigned but unreachable | the pool's addresses must be advertised, for example with an `L2Advertisement` resource |

## Controller logs
Find the controller that owns the class (cloud-controller-manager, AWS Load Balancer Controller,
MetalLB controller) and read its logs for the Service's namespace and name.

## Verify
`EXTERNAL-IP` is populated, then test from outside. With `externalTrafficPolicy: Local`, load
balancer health checks should pass only on nodes that run endpoints.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Service concept page (cloud-controller-manager behaviour, loadBalancerClass semantics), the AWS Load Balancer Controller subnet discovery documentation (role/elb and role/internal-elb tags, value 1 or empty) and the MetalLB configuration documentation (IPAddressPool and L2Advertisement). Removed event strings and deployment names that no document states, kube-vip and Cilium LB IPAM claims, and the sed pipeline.

Method: documentation only; no commands were run.
