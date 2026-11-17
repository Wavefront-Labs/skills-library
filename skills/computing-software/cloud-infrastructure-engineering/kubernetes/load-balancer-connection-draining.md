---
id: computing-software.cloud-infrastructure-engineering.kubernetes.load-balancer-connection-draining
name: load-balancer-connection-draining
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, connection-draining, deregistration-delay, graceful-termination, aws-load-balancer-controller, ip-targets, zero-downtime]
level: advanced
status: docs-checked
description: "Avoid errors on rollouts behind cloud load balancers: align deregistration delay and termination grace period, and use IP targets with readiness gates (AWS controller)."
sources: ["https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/#target-group-attributes", "https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/service/annotations/", "https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/deploy/pod_readiness_gate/", "https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/#conditions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Load balancer deregistration and connection draining

## The race
When a pod is deleted, the kubelet runs its shutdown sequence while the pod's endpoint is marked
terminating in EndpointSlices. A load balancer controller deregisters the target on its own
schedule, and the external load balancer notices the change only after its health checks or
deregistration complete. If the application exits before the load balancer stops sending
requests, clients see errors. Service proxies may keep routing to endpoints that are both `serving` and
`terminating` when all available endpoints are terminating.

## AWS Load Balancer Controller (documented annotations)
```yaml
# Ingress (ALB): set the deregistration delay (available range 0-3600 seconds)
alb.ingress.kubernetes.io/target-type: ip
alb.ingress.kubernetes.io/target-group-attributes: deregistration_delay.timeout_seconds=30
# Service (NLB)
service.beta.kubernetes.io/aws-load-balancer-target-group-attributes: deregistration_delay.timeout_seconds=120,deregistration_delay.connection_termination.enabled=true
```
- `target-type: ip` registers pods directly; `instance` routes through the node (NodePort hop).
  With `spec.loadBalancerClass` on a Service, the controller defaults to `instance`.
- Pod readiness gates: label the namespace `elbv2.k8s.aws/pod-readiness-gate-inject: enabled`
  to inject the gate. It works only with `target-type: ip`, and the controller documents it as
  needed under some circumstances to achieve full zero-downtime rolling deployments.
- Choose the deregistration delay and `terminationGracePeriodSeconds` together: the grace
  period must cover the application's drain time plus any preStop delay you add.
- Long-lived connections (WebSockets, streams) need a longer delay or client reconnect logic.

## Other platforms
Check your provider's documentation for its draining setting; this skill states only the AWS
controller annotations above.

## Also check
- The application's keep-alive timeout versus the load balancer's idle timeout: read both in the
  provider's documentation and keep the server's longer than the balancer's.
- HPA scale-in and node consolidation use the same pod termination path.

## Verify
- [ ] Under continuous load during `kubectl rollout restart`, no requests fail, and the target group shows targets draining for the configured delay.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the AWS Load Balancer Controller annotation reference (target-group-attributes examples, deregistration range 0-3600, connection termination attribute, loadBalancerClass default of instance targets) and its pod readiness gate page (namespace label, ip target type only, zero-downtime rationale), plus the EndpointSlice page for serving and terminating. Removed the timeline numbers, AWS default delay and ALB idle timeout, the GKE BackendConfig and Azure annotation lines, and the load-tool names.

Method: documentation only; no commands were run.
