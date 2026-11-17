---
id: computing-software.cloud-infrastructure-engineering.kubespray.kernel-requirements-and-os-matrix
name: kernel-requirements-and-os-matrix
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [kernel, cgroups-v2, preflight, os-support, kubeadm]
level: intro
status: docs-checked
description: "Check host kernels against Kubernetes 1.32+ guidance (4.19 or any 5.x/6.x; cgroups v2 needs 4.15 minimum, 5.8 recommended) and ignore SystemVerification if too old."
sources:
  - https://kubespray.io/docs/operations/kernel-requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For Kubernetes 1.32.0 and later the page recommends kernel 4.19 from the 4.x LTS series; any 5.x or 6.x is supported. For cgroups v2 the minimum is 4.15 and the recommended version is 5.8 or newer.

If the OS kernel is older than required, tell kubeadm to ignore the preflight error:

```yaml
kubeadm_ignore_preflight_errors:
  - SystemVerification
```

The page's matrix of default kernels (only the ones below 4.19 fail the 4.19 check):

| OS | Kernel | At least 4.19 |
|---|---|---|
| RHEL, Alma, Rocky, Oracle Linux 9 | 5.14 | yes |
| RHEL, Alma, Rocky, Oracle Linux 8 | 4.18 | no |
| Ubuntu 24.04 / 22.04 / 20.04 | 6.6 / 5.15 / 5.4 | yes |
| Debian 12 / 11 | 6.1 / 5.10 | yes |
| Fedora 40 / 39 | 6.8 / 6.5 | yes |
| openSUSE Leap 16.0 | 6.12 | yes |
| Amazon Linux 2 | 4.14 | no |
| openEuler 24.03 / 22.03 / 20.03 | 6.6 / 5.10 / 4.19 | yes |

## Checked

2026-11-04. Version guidance, the preflight setting and the matrix were confirmed on the Kernel Requirements page; removed derived conclusions.

Method: documentation only; no commands were run.
