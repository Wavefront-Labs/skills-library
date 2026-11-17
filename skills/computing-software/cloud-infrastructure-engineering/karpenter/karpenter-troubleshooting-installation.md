---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-troubleshooting-installation
name: karpenter-troubleshooting-installation
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [troubleshooting, install, helm, service-linked-role, sts, dnspolicy, crd]
level: practitioner
status: docs-checked
description: "Fixing Karpenter install problems: spot service-linked role, STS DNS timeout, 64-character role name, unknown CRD fields, replicas, Helm OCI errors, karpenter-crd ownership."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/troubleshooting.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting Karpenter installation

- `AuthFailure.ServiceLinkedRoleCreationNotPermitted`: account never used EC2 Spot. Run `aws iam create-service-linked-role --aws-service-name spot.amazonaws.com`.
- STS credential error `dial tcp: lookup sts.<region>.amazonaws.com: i/o timeout`: in-cluster DNS is not running yet (Karpenter uses `dnsPolicy: ClusterFirst`). Either set `--set dnsPolicy=Default` in Helm so it uses VPC DNS, or ensure a managed node group or Fargate profile hosts CoreDNS with the right tolerations.
- `KarpenterNodeRole-${Cluster_Name}` over 64 characters (common with CDK-generated names): the prefix is only a recommendation; use a shorter role name.
- `strict decoding error: unknown field "spec.template.spec.nodeClassRef.foo"`: CRDs are older than the feature. Follow the CRD upgrade guidance and check release notes for CRD changes.
- Second Karpenter pod unschedulable: default replicas are 2 (since 0.16.0) and Karpenter will not launch capacity for itself (it sees a `karpenter.sh/nodepool DoesNotExist` requirement). Reduce replicas to 1 or keep at least 2 nodes not managed by Karpenter (raise node group min and desired).
- Helm pull errors: need Helm 3.8.0+ for OCI (no `helm repo add`); versions 0.17.0 to 0.34.x need a `v` prefix; for 403 run `docker logout public.ecr.aws`; add `--debug`.
- `karpenter-crd` chart `invalid ownership metadata`: label the CRDs `app.kubernetes.io/managed-by=Helm` and annotate `meta.helm.sh/release-name=karpenter-crd` and `meta.helm.sh/release-namespace=<ns>` on ec2nodeclasses.karpenter.k8s.aws, nodepools.karpenter.sh, nodeclaims.karpenter.sh and nodeoverlays.karpenter.sh, with `--overwrite`.

## Checked

2026-11-04. Confirmed against the Troubleshooting page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
