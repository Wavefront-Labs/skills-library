---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hugepages-resources
name: hugepages-resources
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resource-requests, hugepages, device-plugin, kubelet]
level: practitioner
status: docs-checked
description: "Pre-allocate huge pages on nodes and consume them from pods with hugepages-2Mi or 1Gi resources and medium HugePages volumes, with the quota and limits rules."
sources: ["https://kubernetes.io/docs/tasks/manage-hugepages/scheduling-hugepages/", "https://kubernetes.io/docs/concepts/policy/resource-quotas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Huge pages

Used by DPDK, databases (PostgreSQL `huge_pages`, Oracle), JVMs with `-XX:+UseLargePages`.

## Node setup
Nodes must pre-allocate huge pages for the node to report their capacity. The Kubernetes docs show
a kernel command line such as:
```bash
# /etc/default/grub: GRUB_CMDLINE_LINUX="hugepagesz=1G hugepages=2 hugepagesz=2M hugepages=512"
kubectl describe node <n>      # Capacity and Allocatable list hugepages-1Gi and hugepages-2Mi
```
The node discovers and reports all huge page sizes automatically. For pages allocated dynamically after
boot, the kubelet must be restarted for the new allocation to be reflected.

## Pod
```yaml
containers:
- name: dpdk
  image: <image>
  resources:
    requests: {memory: 1Gi, hugepages-2Mi: 512Mi, cpu: "2"}
    limits:   {memory: 1Gi, hugepages-2Mi: 512Mi, cpu: "2"}
  volumeMounts:
  - {name: hugepage, mountPath: /hugepages}
volumes:
- name: hugepage
  emptyDir:
    medium: HugePages-2Mi       # or HugePages when only one size is used
```

## Rules
- Huge page requests must equal limits (the default if only limits are set); no overcommit.
- A memory or CPU request is also required.
- A pod using several sizes must use `medium: HugePages-<size>` for all its mounts; `medium: HugePages`
  is allowed only when the pod requests one size.
- An emptyDir backed by huge pages may not consume more than the pod's huge page request.
- ResourceQuota can cap them with the `hugepages-<size>` token, for example `hugepages-2Mi: 4Gi`.
- Applications using `shmget()` with `SHM_HUGETLB` need a supplemental group matching
  `/proc/sys/vm/hugetlb_shm_group`.

## Verify
```bash
kubectl exec <p> -- grep -i huge /proc/meminfo
kubectl describe node <n>      # allocatable hugepages vs requests
```

## Checked
2026-10-23, against the Kubernetes website manage-HugePages task (pre-allocation requirement, node reports capacity automatically, kubelet restart for dynamic pages, hugepages-<size> naming, no overcommit, memory or CPU request required, medium rules, emptyDir limit, hugetlb_shm_group, ResourceQuota token). The allocatable-subtraction statement, swap statement, and the mmap error message were removed as unconfirmed.
Method: documentation only; no commands were run.
