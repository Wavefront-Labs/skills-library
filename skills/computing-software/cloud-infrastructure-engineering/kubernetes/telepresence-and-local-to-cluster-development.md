---
id: computing-software.cloud-infrastructure-engineering.kubernetes.telepresence-and-local-to-cluster-development
name: telepresence-and-local-to-cluster-development
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [telepresence, mirrord, local-to-cluster, traffic-intercept, dev-loop, service-mesh-dev, remote-debugging, personal-intercept, inner-loop, local-dev-against-cluster]
level: advanced
status: docs-checked
description: "Intercepting live cluster traffic into a locally-running service with Telepresence or mirrord, for an inner dev loop against real dependencies without full local stacks."
sources: ["https://github.com/telepresenceio/telepresence/blob/HEAD/docs/concepts/architecture.md", "https://github.com/telepresenceio/telepresence/blob/HEAD/docs/reference/cli/telepresence_intercept.md", "https://github.com/telepresenceio/telepresence/blob/HEAD/docs/reference/rbac.md", "https://github.com/telepresenceio/telepresence/blob/HEAD/docs/howtos/mtls.md", "https://github.com/telepresenceio/telepresence/blob/HEAD/docs/compare/mirrord.md", "https://github.com/metalbear-co/mirrord"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Telepresence / mirrord — local-to-cluster development

**Goal:** let a developer run one service locally in their IDE (full
breakpoint debugging) while it transparently talks to — and optionally
receives live traffic from — everything else running in a real cluster,
instead of maintaining a docker-compose stack that drifts from production
topology. Complements devcontainers
(`computing-software.cloud-infrastructure-engineering.kubernetes.devcontainers-for-kubernetes-platform-teams`)
as the other half of "developer environment patterns": devcontainers fix the
*shell*, this fixes the *network*.

## 1. Two different mechanisms, pick based on what you need
- **Telepresence**: a traffic-manager installed in the cluster injects a
  Traffic Agent sidecar into attached pods (or uses a node-hosted agent);
  local daemons set up a virtual network interface, so after
  `telepresence connect` the local process resolves cluster DNS and reaches
  cluster services directly. Attaching to a workload (`replace`, `intercept`,
  `wiretap` or `ingest`) relays traffic, environment and volumes.
  `telepresence intercept <name> --port 8080:<port-identifier>` sends inbound
  traffic for that workload to the local process: either *all* of it (risky on
  a shared service, use only in dedicated dev namespaces) or, with
  `--http-header "X-Dev-User=alice"` (or `--http-path-equal`), only matching
  requests (several headers are ANDed). The header must survive every hop up
  to the intercepted pod, so callers in between must propagate it.
- **mirrord**: no VPN. `mirrord exec <cmd> --target pod/<name>` loads a layer
  into the local process that intercepts its network, file and environment
  calls; mirrord launches an agent pod on the same node as the target, which
  mirrors the target's incoming traffic to the local process and routes its
  outgoing traffic, file reads/writes and environment through the target pod.
  Nothing is pre-installed in the cluster, but the agent needs
  `CAP_NET_ADMIN`, `CAP_SYS_PTRACE` and `CAP_SYS_ADMIN` (configurable via
  `agent.disabled_capabilities`), and only that one process sees the cluster.

## 2. The real payoff and the real risk, in the same feature
Traffic interception is valuable because it removes "docker-compose stack
with 12 fake dependencies that don't match staging." It is risky for the
same reason: a developer's laptop, with a debugger paused on a breakpoint,
is now in the request path of whatever traffic got intercepted. On a shared
dev/staging cluster, an un-scoped intercept (no header filter) can silently
eat real traffic meant for the real deployment — including traffic from
other developers' testing, QA, or (if the namespace isn't properly isolated)
anything upstream. **Default policy**: require header-scoped personal
intercepts in any shared namespace; allow unscoped "steal all traffic"
intercepts only in a developer's own ephemeral namespace.

## 3. Platform-side setup that makes this usable
- Install the Telepresence traffic-manager once with its Helm chart, usually
  by a cluster administrator (not per developer); developers need the CLI
  and `telepresence connect`, and the client RBAC can be pared down.
  RBAC: without a namespace selector, or with a label-based one, the
  traffic-manager needs cluster-wide access; a static namespace selector
  confines it to the listed namespaces.
- Header-filtered intercepts only catch requests that still carry the
  header when they reach the intercepted pod. If an upstream service or
  gateway drops it, those requests go to the real deployment and the
  developer sees nothing; verify propagation end to end before telling
  developers personal intercepts are ready on shared namespaces.
- Document a hard timeout/auto-disconnect policy — a forgotten overnight
  intercept on a shared namespace is a classic on-call page for "why is
  staging returning errors," traced hours later to someone's closed laptop
  still nominally "connected."

## 4. Gotchas
- Local DNS resolution for cluster services only works while `telepresence
  connect` is active; code that caches a resolved IP at startup can keep
  working after a disconnect and give false confidence the feature isn't
  needed, until a redeploy changes the backing pod IP.
- mirrord routes file reads and writes through the target pod, which can
  surprise developers expecting local files (test fixtures); scope its file
  configuration per use case.
- HTTP-filtered Telepresence intercepts need to read headers, so with
  TLS/mTLS traffic Telepresence must be given the certificates to decrypt
  (and re-encrypt, with a client certificate for mTLS upstreams); see its
  TLS/mTLS how-to before promising header filters on encrypted services.

## Verify
- A header-scoped personal intercept only receives traffic carrying that
  header; traffic without it continues to the real deployment, confirmed by
  hitting the service both with and without the header during an active
  intercept.
- Disconnecting (or a laptop going to sleep) stops traffic routing to the
  local process within the tool's advertised timeout, with the Service
  falling back to healthy pods, not erroring.
- A new developer can intercept a service and hit a breakpoint from a real
  upstream request within one onboarding session, without platform-team help
  beyond the documented setup steps.

## Checked
2026-10-27, against Telepresence docs on the default branch (telepresenceio/telepresence `docs/`: architecture, `telepresence intercept` reference, RBAC, TLS/mTLS how-to, mirrord comparison) and the mirrord README (metalbear-co/mirrord main). Confirmed: traffic-manager, Traffic Agent sidecar or node agent, local daemons and virtual network, the replace/intercept/wiretap/ingest modes, `intercept <name>`, `--port <local>:<identifier>`, `--http-header` (AND logic) and `--http-path-equal`, namespace-selector RBAC scope, TLS/mTLS decryption for HTTP filters; mirrord `exec --target`, the per-process layer, the on-demand agent pod on the target's node mirroring incoming traffic, file and environment routing, and its required capabilities.
Method: documentation only; no commands were run.
