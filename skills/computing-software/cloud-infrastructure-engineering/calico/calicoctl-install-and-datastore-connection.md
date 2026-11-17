---
id: computing-software.cloud-infrastructure-engineering.calico.calicoctl-install-and-datastore-connection
name: calicoctl-install-and-datastore-connection
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [calicoctl, install, kubeconfig, datastore, kubernetes, etcd, calicoapiconfig]
level: practitioner
status: docs-checked
description: "Install calicoctl matching the cluster version and point it at the Kubernetes datastore with kubeconfig, env variables or CalicoAPIConfig."
sources:
  - https://docs.tigera.io/calico/latest/operations/calicoctl/install
  - https://docs.tigera.io/calico/latest/operations/calicoctl/configure/kdd
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Install.** Always install the calicoctl version that matches the Calico version in the cluster. Run it as a binary or container on any host with network access to the datastore. On Linux download `calicoctl-linux-amd64` (also `arm64`, `ppc64le`) from the Calico GitHub release for your version, save it as `calicoctl`, and `chmod +x`. macOS binaries are `calicoctl-darwin-arm64` and `calicoctl-darwin-amd64`; Gatekeeper may need Allow Anyway in Security settings.

**Never edit `crd.projectcalico.org`** resources directly; they are internal representations.

**Connecting.** By default calicoctl reads the kubeconfig at `$(HOME)/.kube/config`. Options, with environment variable equivalents (each may also be prefixed `CALICO_` to avoid name clashes):

| File option | Variable | Note |
|---|---|---|
| `datastoreType` | `DATASTORE_TYPE` | `kubernetes` (default) or `etcdv3` |
| `kubeconfig` | `KUBECONFIG` | Path to kubeconfig |
| `k8sAPIEndpoint` | `K8S_API_ENDPOINT` | Not needed with kubeconfig |
| `k8sCertFile`, `k8sKeyFile`, `k8sCAFile` | `K8S_CERT_FILE` etc. | Client cert, key, CA |
| `k8sToken` | none | Token for API access |

One-shot form: `DATASTORE_TYPE=kubernetes KUBECONFIG=~/.kube/config calicoctl get nodes`.

Config file form:

```yaml
apiVersion: projectcalico.org/v3
kind: CalicoAPIConfig
metadata:
spec:
  datastoreType: 'kubernetes'
  kubeconfig: '/path/to/.kube/config'
```

When using calicoctl instead of the API server, calicoctl supplies the validation and defaulting for v3 resources that kubectl lacks.

## Checked

Read in full on 2026-11-08: the Install calicoctl page and the Configure calicoctl to connect to the Kubernetes API datastore page. Download names, the matching-version note, the option table, the one-line command and the config file match them.

Method: documentation only; no commands were run.
