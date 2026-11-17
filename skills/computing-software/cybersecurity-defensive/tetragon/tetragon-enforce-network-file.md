---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-enforce-network-file
name: tetragon-enforce-network-file
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [enforce-demo, tetragon, sigkill, egress]
level: practitioner
status: docs-checked
description: "Apply Tetragon quickstart enforcement policies that Sigkill egress TCP connections leaving the cluster and reads or writes of sensitive files."
sources:
  - "https://tetragon.io/docs/getting-started/enforcement/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enforce network and file restrictions with Tetragon

Goal: block, not just observe. In-kernel filtering lets a policy issue `SIGKILL` so the process never returns from the syscall.

## Network egress

Capture CIDRs, then substitute and apply a namespaced policy:

```shell
export PODCIDR=`kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}'`
# set SERVICECIDR per platform (GKE, Kind, EKS, AKS commands on the page)
wget https://raw.githubusercontent.com/cilium/tetragon/main/examples/quickstart/network_egress_cluster_enforce.yaml
envsubst < network_egress_cluster_enforce.yaml | kubectl apply -n default -f -
```

The policy (`TracingPolicyNamespaced`) hooks `tcp_connect` with a `sock` arg and uses operator `NotDAddr` over `127.0.0.1`, `${PODCIDR}`, `${SERVICECIDR}`, with action `Sigkill`. Watch with `kubectl exec -ti -n kube-system ds/tetragon -c tetragon -- tetra getevents -o compact --pods xwing`. A `curl` to an outside site gives exit code 137 and an `exit ... SIGKILL` event; in-cluster connections work and are not shown.

## File access

Same as the monitoring policy but each `matchArgs` selector gains `matchActions: - action: Sigkill`. Replace it:

```shell
kubectl delete -f https://raw.githubusercontent.com/cilium/tetragon/main/examples/quickstart/file_monitoring.yaml
kubectl apply -f https://raw.githubusercontent.com/cilium/tetragon/main/examples/quickstart/file_monitoring_enforce.yaml
```

`file_monitoring_enforce.yaml` (`TracingPolicyNamespaced`) hooks `security_file_permission`, `security_mmap_file` and `security_path_truncate`: Prefix matches (e.g. `/boot`, `/root/.ssh`, `/etc/shadow`, `/etc/sudoers`) with MAY_READ `4`, Postfix matches (`.bashrc`, `.profile`, ...) with MAY_READ, and writes (`2`) under `/etc`, `/bin`, `/usr/bin`, `/var/log` and similar.

`cat /etc/shadow` in the xwing pod now exits 137 and shows read events then `exit ... SIGKILL`. Files not in the policy are unaffected. With Docker, mount the yaml at `/etc/tetragon/tetragon.tp.d/` and run `docker exec -ti tetragon tetra getevents -o compact`.

## Checked

Date: 2026-11-07

Enforcement getting-started page read in full, plus the network_egress_cluster_enforce, network_egress_cluster and file_monitoring_enforce quickstart YAML files it applies.

Method: documentation only; no commands were run.
