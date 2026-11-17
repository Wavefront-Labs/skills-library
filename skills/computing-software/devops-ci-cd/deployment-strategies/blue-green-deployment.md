---
id: computing-software.devops-ci-cd.deployment-strategies.blue-green-deployment
name: blue-green-deployment
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, blue-green, blue-green-deployment, red-black, traffic-switch, cutover, load-balancer, target-groups, aws-alb, weighted-target-groups, kubernetes-service-selector, dns-cutover, dns-ttl, aws-codedeploy, connection-draining, websockets, warm-up, smoke-test, preview-environment, session-state, background-workers, queue-consumers, cron, instant-rollback, zero-downtime]
level: practitioner
status: draft
description: "Run blue-green cutovers that are really instant to undo: where to switch traffic, warming and testing green privately, draining, workers/cron running twice, shared-DB rules and teardown."
sources: ["https://martinfowler.com/bliki/BlueGreenDeployment.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html#welcome-deployment-overview-blue-green", "https://kubernetes.io/docs/concepts/services-networking/service/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blue-green deployment

**Goal:** the new version (green) is fully running and verified *before* any user sees
it; the switch is one atomic action; switching back is the same action in reverse and
takes seconds.

(Choosing between rolling, blue-green and canary is covered in
`computing-software.devops-ci-cd.deployment-strategies.canary-blue-green-and-rollback`.)

## 1. Where to flip the switch
| Switch point | Speed of cutover/rollback | Caveats |
|---|---|---|
| Load-balancer listener / target group (AWS ALB, GCP backend service, HAProxy, NGINX upstream) | seconds | Best default. ALB weighted target groups also allow a 90/10 "soft" switch |
| Kubernetes `Service` selector (`version: blue` → `green`) | seconds | Only for in-cluster traffic paths; Ingress/mesh variants similar |
| Service mesh route (Istio VirtualService, Linkerd) | seconds | Also gives header-based preview routing |
| DNS record | minutes to hours | Resolvers and clients ignore low TTLs; rollback is *not* instant. Avoid unless unavoidable |
| Managed tooling (AWS CodeDeploy blue/green, Argo Rollouts `blueGreen`) | seconds | Encodes the steps below; read its defaults for termination wait |
The switch must be a single change you can script and reverse. Hand-editing three
config files is not blue-green.

## 2. The cutover runbook
1. **Deploy green** alongside blue with production config, scaled to full production
   capacity (not "a couple of pods" — it receives 100% at once).
2. **Warm it:** JIT/JVM warm-up, cache priming, connection pools filled. Cold green +
   instant 100% switch = latency spike that looks like a failed release.
3. **Test it privately:** a preview hostname, a separate listener port, or a header route
   (`x-env: green`) that only testers/synthetic checks use. Run smoke + key journeys.
4. **Switch** traffic. Keep blue running and **unchanged**.
5. **Watch** error rate, latency, saturation, business KPIs for a defined window
   (e.g. 30-60 min, longer for daily-batch-heavy systems).
6. **Rollback = switch back**, no redeploy. Decide the rollback trigger in advance.
7. After the window, scale blue down (keep the artifact/config to recreate it). Next
   release, blue becomes the target.

## 3. Draining and long-lived connections
- Set LB deregistration/draining delay so in-flight requests on blue finish (AWS ALB
  `deregistration_delay` defaults to 300 s — *verify*; shorten for fast APIs).
- WebSockets, gRPC streams, SSE: existing connections stay on blue until they close.
  Either let clients reconnect naturally (and accept blue lives longer) or have blue
  send a "reconnect" signal after the switch.
- Sessions: externalise session state (Redis, signed cookies) — in-memory sessions on
  blue are lost at cutover.

## 4. The things that run twice
Blue-green duplicates everything, not just the HTTP tier:
- **Queue consumers** in both stacks consume the same queue → green processes messages
  *before* the switch. Either keep green's consumers scaled to zero until cutover, or
  make consumers version-tolerant and idempotent.
- **Cron / schedulers** fire in both → double emails, double billing runs. Use a leader
  lock, or enable schedules only in the live colour (config flag flipped with the switch).
- **Migrations** at startup run when green boots — before cutover. They must be
  backward-compatible with blue (expand/contract), which is the same rule as rolling deploys.

## 5. Shared database: the limit of instant rollback
Blue and green almost always share the database. Rollback is instant for code, but data
green wrote must be readable by blue. If green writes a new format, rollback silently
corrupts or crashes blue. Blue-green does **not** remove the need for expand/contract.
Separate blue/green databases (with replication) exist but are rarely worth the
consistency risk; *treat as specialist territory*.

## 6. Cost and when not to use it
- Requires ~2× capacity during the window; on Kubernetes with autoscaling, that's
  usually tolerable, for big VM fleets often not.
- Poor fit for stateful services (databases, brokers) and for apps where any version mix
  over minutes is fine — rolling is cheaper there.

## Verify
- [ ] Switch and switch-back are each a single scripted command; both rehearsed in staging.
- [ ] Synthetic load during cutover shows no 5xx and no latency spike beyond the SLO.
- [ ] Green's queue consumers and cron jobs are inactive until cutover (checked in logs).
- [ ] Blue reading data written by green has been tested for this release.
- [ ] Rollback triggers and the observation window are written in the release plan.
