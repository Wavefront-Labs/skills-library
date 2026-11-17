---
id: computing-software.devops-ci-cd.helm.version-skew-policy
name: version-skew-policy
category: computing-software
field: devops-ci-cd
product: helm
tags: [version-skew, kubernetes-compatibility, supported-versions, helm-4, n-3, release-policy]
level: practitioner
status: docs-checked
description: "Which Kubernetes versions each Helm release supports: Helm 4 supports n-3 minor versions, with a table of 4.0.x to 4.3.x."
sources:
  - "https://helm.sh/docs/topics/version_skew/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Each Helm release is compiled against one Kubernetes minor version's client. As of Helm 4, Helm is assumed compatible with n-3 versions of Kubernetes it was compiled against. Helm v4.0.0 uses the Kubernetes 1.34.1 client, so it is compatible with Kubernetes 1.34. The page does not recommend using Helm with a Kubernetes newer than the one it was compiled against, as there are no forward-compatibility guarantees, and using an unsupported version is at your own risk.

Table from the version skew page:

- Helm 4.3.x: Kubernetes 1.37 to 1.34
- Helm 4.2.x: Kubernetes 1.36 to 1.33
- Helm 4.1.x: Kubernetes 1.35 to 1.32
- Helm 4.0.x: Kubernetes 1.34 to 1.31

The project maintains a release branch for the most recent minor release only; fixes, including security fixes, are cherry-picked there depending on severity and feasibility.

`Chart.yaml`'s `kubeVersion` range is a separate chart-level check.

## Checked

2026-11-08. Read the Version Support Policy page (current docs source, Helm 4) in full. The 4.0.x to 4.3.x table matches. Removed unsupported practical consequences and the helm version --short claim; replaced the Helm 3 sentence with the page's compile-against and n-3 wording.

Method: documentation only; no commands were run.
