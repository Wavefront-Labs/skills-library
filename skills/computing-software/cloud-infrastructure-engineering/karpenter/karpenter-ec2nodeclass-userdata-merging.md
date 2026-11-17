---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-userdata-merging
name: karpenter-ec2nodeclass-userdata-merging
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [userdata, nodeconfig, mime, toml, powershell, ca-rotation, ec2nodeclass, merge]
level: advanced
status: docs-checked
description: "How spec.userData merges per amiFamily: AL2 MIME part, AL2023 NodeConfig precedence, Bottlerocket TOML, Windows prepend, Custom none, and the CA rotation size warning."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass userData merge behaviour

Karpenter merges `spec.userData` with the family default; it does not replace it (except Custom).

- AL2: bash or MIME multipart. Your script becomes a MIME part and Karpenter appends the bootstrap part last. Extra kubelet settings can be changed by editing `/etc/kubernetes/kubelet/kubelet-config.json` in your script (for example with `jq '.kubeAPIQPS=50'`).
- AL2023: shell script, MIME multipart, or NodeConfig YAML/JSON. The result is MIME: your parts first, then Karpenter's generated NodeConfig. Values in Karpenter's NodeConfig win: cluster name, CIDR, endpoint, CA, taints, labels and everything in `spec.kubelet`. Set those through Karpenter.
- Bottlerocket: must be valid TOML; unknown fields are ignored; Karpenter-controlled values (cluster name, endpoint, certificate, taints, labels, `spec.kubelet`) override yours. For device ownership on v1.30.0+ set `[settings.kubernetes] device-ownership-from-security-context = true`.
- Windows: PowerShell; your commands are prepended to the managed section. Karpenter does not pass `-ServiceCIDR`; the effective CIDR (172.20.0.0/16 or 10.100.0.0/16) can be checked in the vpc-bridge.conf on the node.
- Custom: no merging; your userData must register the `karpenter.sh/unregistered:NoExecute` taint and match `spec.kubelet`.

```yaml
amiSelectorTerms: [{alias: al2023@v20240807}]
kubelet: {maxPods: 42}
userData: |
  apiVersion: node.eks.aws/v1alpha1
  kind: NodeConfig
  spec:
    kubelet:
      config:
        registryPullQPS: 10
```

Warning: during an EKS CA rotation the generated userData grows with a second CA. Karpenter does not compress user data, so if yours is near the EC2 limit, launch template creation fails. Shrink it beforehand.

## Checked

2026-11-04. Confirmed against the NodeClasses concept page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
