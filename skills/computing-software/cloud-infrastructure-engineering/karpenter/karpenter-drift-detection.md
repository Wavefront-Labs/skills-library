---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-drift-detection
name: karpenter-drift-detection
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [drift, drifted-condition, amiselectorterms, subnetselectorterms, securitygroupselectorterms, requirements, behavioral-fields]
level: practitioner
status: docs-checked
description: "Which NodePool and EC2NodeClass fields trigger Drift, which behavioural fields are ignored, the hash mechanism and special cases for resolved values."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter drift detection

A NodeClaim is drifted when its values no longer match its owning NodePool or EC2NodeClass template. Karpenter stores a hash of the template on those resources to detect changes. Drift is a graceful method, run first by the Disruption Controller, and gated by a feature gate; with the gate off Karpenter removes the `Drifted` status condition from NodeClaims.

Fields that cause drift:
- NodePool: `spec.template.spec.requirements`
- EC2NodeClass: `spec.subnetSelectorTerms`, `spec.securityGroupSelectorTerms`, `spec.amiSelectorTerms`

Behavioural fields never cause drift: NodePool `spec.weight`, `spec.limits`, `spec.disruption.*`.

Resolved-value cases: drift can occur without a CRD edit when resolved values change, for example a newer AMI matching `amiSelectorTerms`. Compatible changes do not drift: widening an instance-type requirement that still includes the node's current type does not drift it.

`expireAfter` and `terminationGracePeriod` changes on the NodePool do not modify existing NodeClaims; they induce drift, so replacements carry the new values.

Drift respects NodePool disruption budgets (reason `Drifted`), PDBs and `do-not-disrupt`, except that a NodeClaim with `terminationGracePeriod` can drift even with blocking PDBs or do-not-disrupt pods, so critical updates such as CVE patches are not blocked.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 disruption.md page; removed the deployment-template analogy and the specific m5/AMI id examples as not in the page. Field lists and behaviour unchanged.
