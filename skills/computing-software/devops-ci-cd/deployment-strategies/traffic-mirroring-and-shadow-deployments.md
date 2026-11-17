---
id: computing-software.devops-ci-cd.deployment-strategies.traffic-mirroring-and-shadow-deployments
name: traffic-mirroring-and-shadow-deployments
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, traffic-mirroring, shadow-deployment, shadow-traffic, dark-traffic, dark-launch, request-shadowing, istio-mirror, envoy-request-mirror-policy, nginx-mirror, goreplay, gor, diffy, response-diffing, scientist, github-scientist, side-effects, idempotent-replay, write-suppression, pii-in-replay, sampling-percentage, mirror-percentage, fire-and-forget, latency-impact, capacity-validation, migration-validation]
level: advanced
status: draft
description: "Test a new version with real production traffic and zero user impact: Istio/Envoy/NGINX mirroring, GoReplay capture and replay, response diffing (Diffy/Scientist), side-effect and PII rules."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/mirroring/", "https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/route/v3/route_components.proto#config-route-v3-routeaction-requestmirrorpolicy", "https://nginx.org/en/docs/http/ngx_http_mirror_module.html", "https://github.com/buger/goreplay", "https://github.com/github/scientist", "Humble & Farley, Continuous Delivery (2010), ch. 10 - dark launching"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Traffic mirroring and shadow deployments

**Goal:** the new version receives a copy of real production requests, its responses
are compared and its resource usage observed — while users only ever see the old
version's responses. Then a canary is a formality.

## 1. When shadowing beats a canary
- Rewrites/migrations (new language, new datastore, new service extracted from a
  monolith) where you need *behavioural equivalence* over thousands of real inputs.
- Capacity validation of a new version under real load shape without risk.
- Read-heavy APIs where responses can be diffed.
Not for: flows with unavoidable side effects you can't suppress (payments, emails),
or where the new version's latency would be judged — mirroring is fire-and-forget, so
measure latency on the shadow side's own metrics.

## 2. Mirroring at the proxy
**Istio** (`VirtualService`):
```yaml
http:
  - route: [{ destination: { host: orders, subset: v1 }, weight: 100 }]
    mirror: { host: orders, subset: v2 }
    mirrorPercentage: { value: 10.0 }
```
Envoy mirrors the request asynchronously; the mirrored response is discarded; `Host`
header gets a `-shadow` suffix (`orders-shadow`) — use it to tell shadow traffic apart in
logs and to suppress side effects. Body mirroring works for buffered requests; streaming
bodies aren't mirrored. Mirrored requests count against v2's resources, not the user's
latency, but they **do** add egress and upstream (DB) load.
**Envoy** directly: `request_mirror_policies: [{ cluster: orders_v2, runtime_fraction: { default_value: { numerator: 10, denominator: HUNDRED } } }]`.
**NGINX**: `mirror /mirror; mirror_request_body on;` with `location = /mirror { internal; proxy_pass http://orders-v2$request_uri; }` —
note NGINX **waits** for the mirror subrequest before freeing the connection in some
versions/configs (`proxy_ignore_client_abort`), so slow shadows can hold worker
connections; set short `proxy_read_timeout` on the mirror location.
**AWS**: VPC Traffic Mirroring is packet-level (for IDS, not app shadowing); ALB has no
mirroring — use Envoy/App Mesh or GoReplay on instances. **GCP** internal LB/Traffic
Director (`requestMirrorPolicy`) supports it.
**Linkerd**: no native mirroring; use `kube-replay`/GoReplay.

## 3. Capture and replay (GoReplay)
When you lack a proxy, or want to replay later/at different rates:
```bash
# on a production node (or a sidecar with NET_RAW/host network): capture 10 % and forward live
gor --input-raw :8080 --input-raw-track-response --output-http "http://orders-v2.staging:8080|10%" \
    --http-set-header "X-Shadow: 1" --output-http-workers 50 --output-http-timeout 2s
# or record to a file and replay later at 2x speed
gor --input-raw :8080 --output-file requests.gor
gor --input-file "requests.gor|200%" --output-http http://orders-v2.staging:8080 --output-http-track-response --output-http-stats
```
Middleware (`--middleware`) scripts can rewrite/anonymise bodies, drop writes, or
replace auth tokens. Replaying into **staging** (not a prod-adjacent shadow) is the
safest way to test against a datastore you own.

## 4. Side effects — the whole safety story
Shadow requests must not: charge cards, send emails/SMS/push, enqueue jobs consumed by
prod workers, write to shared databases, call rate-limited partners, or mutate caches
users read. Techniques:
- **Suppress at the boundary**: the shadow deployment runs with config
  `SIDE_EFFECTS=off` / sandbox credentials for every outbound integration, and an
  outbound egress NetworkPolicy that allows only its own datastore + read-only replicas.
- **Detect shadow requests**: `X-Shadow: 1` header or the `-shadow` Host suffix; the
  app short-circuits writes to a scratch store or logs the intended write instead.
- **Own datastore**: shadow v2 points at a replica/clone (read-only replica for reads;
  a restored snapshot for writes) — never the primary.
- **Idempotency keys**: if the shadow *must* hit a shared system, replay with
  idempotency keys so duplicates are no-ops.
- Mirror only GET/HEAD at first (`match: [{ method: { exact: GET } }]` in Istio) and
  expand once suppression is proven.
Test the suppression with a canary request carrying a known marker; verify no email/job/
charge happened before enabling percentages.

## 5. Comparing responses
- **Diffy** (Twitter/OpenDiffy): routes a request to primary, secondary (same old
  version, to learn noise) and candidate; reports diffs minus the noise. Still the
  reference design; maintained forks exist.
- **Scientist** pattern (GitHub `scientist` Ruby, `laboratory` Python, `scientist.net`,
  Go ports): inside the *old* code, run old and new implementations, return old,
  compare, publish mismatches with context. In-process, no proxy; perfect for refactors.
- DIY: log `(request-id, status, normalised body hash)` from both; join in your log
  store; normalise timestamps/ids/ordering before hashing; alert on mismatch rate and
  show samples. Target: mismatch rate < 0.1 % with every mismatch explained before
  promotion.
Compare **status codes, body semantics, headers that matter** (cache-control, content-type),
and the shadow's **latency and error rate** from its own metrics — the comparison
endpoint tells you about correctness, the metrics about readiness.

## 6. Capacity and blast radius
Start at 1 %, step to 10/50/100 %; the shadow should be sized like the canary it will
become. Watch *shared* dependencies (DB replica CPU, cache hit rate, partner quotas)
since mirrored load doubles the reads. Kill switch: set `mirrorPercentage` to 0 (one
config change) — practise it. Mirroring across regions/clouds costs egress; estimate first.

## 7. Privacy
Mirrored traffic contains real user data; the shadow environment must meet the same
controls as production (encryption, access, retention). Scrub/strip PII in GoReplay
middleware when replaying into lower environments; never record raw captures to
laptops; delete capture files on a schedule.

## Verify
- [ ] A marker request proves side-effect suppression (no email/job/charge/write on the primary store).
- [ ] At 10 % mirror, user-facing p95 and error rate are unchanged; the shadow's own dashboards show load.
- [ ] Response diff report runs daily with a mismatch rate and sample diffs; mismatches are triaged.
- [ ] Setting mirror to 0 % stops shadow traffic within seconds (tested).
