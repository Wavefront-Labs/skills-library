---
id: computing-software.devops-ci-cd.deployment-strategies.load-balancer-deregistration-delay
name: load-balancer-deregistration-delay
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, zero-downtime, load-balancer-deregistration-delay, deregistration-delay, connection-draining, aws-alb, target-groups, nlb, prestop, graceful-shutdown, aws-load-balancer-controller, pod-readiness-gates, 502-during-deploy]
level: advanced
status: draft
description: "Eliminate 502/504s during deploys by aligning LB deregistration delay, preStop sleep, app graceful shutdown and terminationGracePeriodSeconds, for ALB/NLB, Kubernetes and ECS."
sources: ["https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html#deregistration-delay", "https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/deploy/pod_readiness_gate/", "https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-connection-draining.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Load balancer deregistration delay

## The race
On rollout the old instance/pod gets SIGTERM at roughly the same moment the LB is told
to deregister it. LB propagation takes seconds; if the app exits first, requests still
routed to it fail (502/503/504, connection reset).

## The timeline you want
```
t0   pod marked Terminating -> endpoints removed; LB deregistration starts (state: draining)
t0   preStop: sleep 15            (app keeps serving while LBs/kube-proxy catch up)
t15  SIGTERM -> app stops accepting new conns, finishes in-flight (<= 20 s)
t35  app exits
     deregistration_delay (e.g. 30 s) >= preStop + drain time; no new requests after t0+~5s
     terminationGracePeriodSeconds (e.g. 60) > preStop + drain, else SIGKILL mid-request
```

## AWS ALB/NLB target group
```bash
aws elbv2 modify-target-group-attributes --target-group-arn "$TG" \
  --attributes Key=deregistration_delay.timeout_seconds,Value=30
```
- Default **300 s**: deploys take 5 minutes per batch for no reason on fast APIs. Set it
  just above your longest normal request (30-60 s); keep longer for websockets/uploads.
- NLB also has `deregistration_delay.connection_termination.enabled` to close
  connections at the end of the delay.
- Kubernetes (AWS Load Balancer Controller):
  `alb.ingress.kubernetes.io/target-group-attributes: deregistration_delay.timeout_seconds=30`
  on the Ingress/Service; use `target-type: ip` plus **pod readiness gates** (label the
  namespace `elbv2.k8s.aws/pod-readiness-gate-inject=enabled`) so rollouts wait until new
  pods are healthy *in the target group*, not just Ready in Kubernetes.
- ECS: set the target group delay; ECS waits for draining before stopping tasks;
  container `stopTimeout` must exceed the app drain time.

## Kubernetes pod side
```yaml
spec:
  terminationGracePeriodSeconds: 60
  containers:
  - name: api
    lifecycle:
      preStop:
        sleep: { seconds: 15 }          # K8s 1.30+ native; older: exec ["sh","-c","sleep 15"]
```
App must handle SIGTERM: stop accepting, drain keep-alive connections (send
`Connection: close`), finish in-flight, exit. Node.js `server.close()`, Go
`srv.Shutdown(ctx)`, Spring `server.shutdown=graceful`.

## Other LBs
GCP: backend service `connectionDraining.drainingTimeoutSec`; NGINX ingress relies on
endpoint updates plus preStop; Azure App Gateway: *connection draining* timeout on the
backend settings.

## Verify
Run constant load (`hey -z 3m -q 50 https://api.example.com/health`) during a rollout:
zero non-2xx. Then temporarily remove the preStop: 502s appear, proving the setup matters.
