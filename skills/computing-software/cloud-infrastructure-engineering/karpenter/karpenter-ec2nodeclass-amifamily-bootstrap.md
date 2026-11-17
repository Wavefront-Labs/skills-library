---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-amifamily-bootstrap
name: karpenter-ec2nodeclass-amifamily-bootstrap
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [amifamily, al2, al2023, bottlerocket, windows, custom, ubuntu, nodeconfig, registerwithtaints]
level: advanced
status: docs-checked
description: "amiFamily and generated bootstrap for AL2, AL2023, Bottlerocket, Windows and Custom, the Ubuntu removal at v1, AL2 end of life, and the unregistered taint required for Custom."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass amiFamily and bootstrap

`spec.amiFamily` controls UserData generation and default block devices, not which AMI is found. It is only required if you do not use an `alias` term (an alias implies the family, for example `al2023@...` means AL2023). Families: AL2, AL2023, Bottlerocket, Windows2019, Windows2022, Windows2025, Custom.

Generated bootstrap:
- AL2: a call to `/etc/eks/bootstrap.sh` with `--use-max-pods false` and `--kubelet-extra-args`. EKS releases AL2 AMIs only through Kubernetes 1.32.
- AL2023: a MIME part of type `application/node.eks.aws` containing a `NodeConfig` (`node.eks.aws/v1alpha1`) with cluster name, endpoint, CA, cidr, `kubelet.config.maxPods`, and `--node-labels` flags.
- Bottlerocket: TOML `[settings.kubernetes]` with api-server, cluster-certificate, cluster-name, cluster-dns-ip, max-pods and node-labels.
- Windows: `Start-EKSBootstrap.ps1` with `-EKSClusterName`, `-APIServerEndpoint`, `-Base64ClusterCA`, `-KubeletExtraArgs`, `-DNSClusterIP`.
- Custom: no default userData. The kubelet must register with taint `karpenter.sh/unregistered:NoExecute` (`--register-with-taints` or `registerWithTaints`), or Karpenter will fail to register the node.

Ubuntu: support dropped at v1.0.0. Select Ubuntu AMIs with `amiSelectorTerms`, then either maintain UserData with `Custom` or use `amiFamily: AL2` with custom `blockDeviceMappings` (for example `/dev/sda1`, `rootVolume: true`, gp3, 20Gi). The AL2 userData compatibility is not guaranteed long term.

## Checked

2026-11-04. Confirmed against the NodeClasses concept page (v1.13) (identifiers, defaults, limits and prose). Removed the unconfirmed 'do not call bootstrap.sh' remark.

Method: documentation only; no commands were run.
