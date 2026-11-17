---
id: computing-software.cloud-infrastructure-engineering.kubernetes.component-log-verbosity-and-json-logging
name: component-log-verbosity-and-json-logging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, logs-events, klog-verbosity, json-logging, kubelet, kube-apiserver]
level: practitioner
status: docs-checked
description: "Raise and lower klog verbosity on control-plane components, kubelet and kubectl, change the apiserver level at runtime, and switch components to JSON logs."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/system-logs/", "https://kubernetes.io/docs/reference/kubectl/quick-reference/#kubectl-output-verbosity-and-debugging", "https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4/", "https://github.com/kubernetes/community/blob/main/contributors/devel/sig-instrumentation/logging.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# klog verbosity and JSON logging

## Levels
`--v=0` only what an operator should always see; `2` steady-state information and HTTP
requests, the recommended default for most systems; `3` extended change information; `4` debug;
`5` trace. Raise verbosity briefly and put it back; high levels on a busy apiserver are very
noisy. Error messages are always logged.

## Set it
```yaml
# static pod (kubeadm ClusterConfiguration v1beta4: extraArgs is a list of name/value pairs)
apiServer:
  extraArgs:
  - {name: v, value: "4"}
---
# kubelet: /var/lib/kubelet/config.yaml
logging:
  verbosity: 4
  format: json          # or text
```
Then restart (kubelet: `systemctl restart kubelet`; static pods restart when the manifest changes).

## Change apiserver verbosity at runtime
```bash
kubectl proxy &
curl -X PUT -d '4' http://127.0.0.1:8001/debug/flags/v
curl -X PUT -d '2' http://127.0.0.1:8001/debug/flags/v      # put it back
```
The apiserver serves `/debug/flags/v` and accepts `PUT` to change `--v`; the request is
authorized like any non-resource URL (cluster-admin can do it). The kubelet serves the same
endpoint when `enableDebugFlagsHandler` is true (the default).

## JSON logs
`--logging-format=json` on kube-apiserver, kube-controller-manager, kube-scheduler and the
kubelet (the components the docs list) gives one JSON object per line with `ts`, `v`, `msg` and
optional `err` plus key-value fields, which log pipelines parse without regex. The docs warn
that field names and serialization may change, that some lines (for example at start-up) are
not JSON, and that JSON output does not support many klog flags.

## kubectl
```bash
kubectl get pods -v=6     # requested resources
kubectl get pods -v=7     # plus HTTP request headers
kubectl get pods -v=8     # plus HTTP request contents
kubectl get pods -v=9     # contents without truncation
```

## Verify
`crictl logs <apiserver-container> | head -1 | jq .` parses when JSON is on; logs volume returns to
normal after lowering verbosity.

## Checked
2026-10-27 against the System Logs page, the kubectl quick reference verbosity table, the kubelet
and kubeadm v1beta4 configuration references (kubernetes/website main, v1.38 development tree;
v1.37 is the latest release), the SIG Instrumentation logging conventions (kubernetes/community
main) and the apiserver debug flags route source. Confirmed: verbosity level meanings, structured
`extraArgs`, kubelet `logging.verbosity`/`format`, the `/debug/flags/v` PUT handler and
`enableDebugFlagsHandler`, the JSON keys and the list of components supporting JSON. Fixed: kube-proxy
was listed as supporting JSON, JSON key names were called stable (the docs say they may change),
and the kubectl `-v` descriptions.
Method: documentation only; no commands were run.
