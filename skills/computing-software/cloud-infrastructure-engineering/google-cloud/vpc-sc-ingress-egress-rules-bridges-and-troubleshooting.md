---
id: computing-software.cloud-infrastructure-engineering.google-cloud.vpc-sc-ingress-egress-rules-bridges-and-troubleshooting
name: vpc-sc-ingress-egress-rules-bridges-and-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc-service-controls, ingress-egress-rules, ingress-policies, egress-policies, perimeter-bridges, vpc-sc-troubleshooting, vpc-sc-violation]
level: advanced
status: docs-checked
description: "Open precise paths through VPC Service Controls with ingress and egress rules, decide when a perimeter bridge fits, and troubleshoot violations from their unique ID to the fix."
sources: ["https://cloud.google.com/vpc-service-controls/docs/ingress-egress-rules", "https://cloud.google.com/vpc-service-controls/docs/share-across-perimeters", "https://cloud.google.com/vpc-service-controls/docs/troubleshooting", "https://cloud.google.com/vpc-service-controls/docs/troubleshoot-with-analyzer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC-SC: ingress/egress rules, bridges and troubleshooting

## 1. Ingress rule (into the perimeter)
```yaml
# ingress.yaml — CI uploads artifacts into one bucket's project from outside
- ingressFrom:
    identities: [serviceAccount:ci-uploader@<CI_P>.iam.gserviceaccount.com]
    sources: [{resource: projects/<CI_PROJECT_NUMBER>}]     # or {accessLevel: accessPolicies/<POL>/accessLevels/corp}
  ingressTo:
    operations:
    - serviceName: storage.googleapis.com
      methodSelectors: [{method: google.storage.objects.create}]
    resources: [projects/<DATA_PROJECT_NUMBER>]
```
## 2. Egress rule (out of the perimeter)
```yaml
# egress.yaml — BigQuery job inside reads a partner's public dataset project
- egressFrom:
    identities: [serviceAccount:etl@<DATA_P>.iam.gserviceaccount.com]
  egressTo:
    operations:
    - serviceName: bigquery.googleapis.com
      methodSelectors: [{method: "*"}]
    resources: [projects/<PARTNER_PROJECT_NUMBER>]
```
```bash
gcloud access-context-manager perimeters dry-run update data-prod --set-ingress-policies=ingress.yaml --set-egress-policies=egress.yaml
gcloud access-context-manager perimeters dry-run enforce data-prod
```
Keep rules narrow: specific identities (never `ANY_IDENTITY` unless public data), specific methods,
specific projects.

## 3. Perimeter bridges
```bash
gcloud access-context-manager perimeters create bridge-analytics --perimeter-type=bridge \
  --resources=projects/<NUM_A>,projects/<NUM_B> --title="analytics bridge"
```
A bridge lets projects in **different** perimeters communicate, bidirectionally. Ingress and egress rules can replace and simplify use cases that previously required bridges, so prefer them (directional, method-level).

## 4. Troubleshoot a violation
1. The error message contains `vpcServiceControlsUniqueIdentifier: <ID>`.
2. Logs: `protoPayload.metadata.vpcServiceControlsUniqueId="<ID>"`, then read `violationReason` and the `ingressViolations` / `egressViolations` details.
3. Use the VPC Service Controls **violation analyzer** (see "Access the violation analyzer" in the troubleshooting guide) to diagnose the denial.

| Reason | Meaning |
|---|---|
| `NO_MATCHING_ACCESS_LEVEL` | the caller's IP, device or identity matches no ingress rule or access level on the perimeter; the docs recommend an ingress rule over an access level |
| `RESOURCES_NOT_IN_SAME_SERVICE_PERIMETER` | one request touches several resources that are not in the same perimeter, wherever the client is |
| `SERVICE_NOT_ALLOWED_FROM_VPC` | a client in a VPC network calls a service that the perimeter's VPC accessible services does not allow |
| `NETWORK_NOT_IN_SAME_SERVICE_PERIMETER` | a VPC client reaches a project outside its perimeter (egress violation), or an outside VPC client reaches a protected project (ingress violation) |

## Gotchas
- Dry run mode logs violations without denying them: test rules there before enforcing.
- After you create or update a perimeter it can take up to 30 minutes for changes to take effect, and requests may be blocked with `Error 403: Request is prohibited by organization's policy` meanwhile.

## Verify
- [ ] The previously failing flow succeeds; the same call by a different identity still fails.
- [ ] No `ANY_IDENTITY` rules exist without a documented reason.

## Checked

2026-10-27. Confirmed in the ingress and egress rules, share across perimeters (bridges), dry run mode, create service perimeters and troubleshooting pages and the `gcloud access-context-manager perimeters` reference pages: rule fields (`ingressFrom`, `ingressTo`, `egressFrom`, `egressTo`, `identities`, `sources`, `accessLevel`, `operations`, `serviceName`, `methodSelectors`, `ANY_IDENTITY`), `dry-run update --set-ingress-policies/--set-egress-policies`, `dry-run enforce`, `--perimeter-type=bridge`, the `vpcServiceControlsUniqueIdentifier` message and `vpcServiceControlsUniqueId` log field, the four `violationReason` meanings (corrected), 30-minute propagation, dry run semantics, bridges are bidirectional and can be replaced by rules. Removed: bridges-cannot-be-dry-run claim, console troubleshooter paste claim (the analyzer page returned 404), caller/service-agent and multi-method gotchas. Read end to end.

Method: documentation only; no commands were run.
