---
id: computing-software.cloud-infrastructure-engineering.aws.eks-fargate-profiles
name: eks-fargate-profiles
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eks, eks-fargate-profile, fargate, pod-execution-role, coredns-fargate, serverless-kubernetes]
level: practitioner
status: docs-checked
description: "Run EKS pods on Fargate: profiles and selectors, pod execution role, private subnets, CoreDNS on Fargate, sizing rounding, logging via Fluent Bit, and Fargate limits."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/fargate.html", "https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html", "https://docs.aws.amazon.com/eks/latest/userguide/fargate-pod-configuration.html", "https://docs.aws.amazon.com/eks/latest/userguide/fargate-logging.html", "https://docs.aws.amazon.com/eks/latest/userguide/fargate-getting-started.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EKS Fargate profiles

## 1. Profile
A Fargate profile says which pods run on Fargate: up to 5 selectors (each needs a namespace, labels optional; `*` and `?` wildcards are allowed in namespaces and label keys/values), private subnets only (no direct route to an internet gateway), and a pod execution role.
```bash
aws eks create-fargate-profile --cluster-name prod --fargate-profile-name batch \
  --pod-execution-role-arn arn:aws:iam::111122223333:role/EKSFargatePodExecution \
  --subnets subnet-priv-a subnet-priv-b \
  --selectors namespace=batch namespace=jobs,labels={compute=fargate}
```
- A pod must match a profile's selectors when it is **scheduled** to run on Fargate; pods that match no profile are not scheduled onto Fargate and can stay `Pending` if there are no nodes for them. If several profiles match, the pod can pick one with the label `eks.amazonaws.com/fargate-profile: <name>`; otherwise the profile whose name sorts first alphanumerically wins.
- Profiles cannot be changed: create a new profile and delete the old one. Pods running on a profile are stopped and set to pending when it is deleted. Fargate spreads pods over the profile's subnets unevenly; use one subnet per profile if you need an even spread. `topologySpreadConstraints` are not supported.
- Pod execution role: its trust policy uses the `eks-fargate-pods.amazonaws.com` service principal; it lets the kubelet register the node and read ECR images, and EKS adds it to the cluster's RBAC. App permissions
  come from IAM roles for service accounts (the instance metadata service is not available to Fargate pods), not this role.

## 2. CoreDNS on Fargate-only clusters
By default CoreDNS is configured to run on EC2 (annotation `eks.amazonaws.com/compute-type: ec2`).
For a cluster with no nodes, create a profile for `kube-system` with label
`k8s-app=kube-dns`, remove the annotation, then restart CoreDNS (the Fargate getting-started guide covers these steps):
```bash
kubectl patch deployment coredns -n kube-system --type json \
  -p='[{"op":"remove","path":"/spec/template/metadata/annotations/eks.amazonaws.com~1compute-type"}]'
kubectl rollout restart -n kube-system deployment coredns
```

## 3. Sizing
Fargate picks a vCPU/memory combination from the pod's **requests**: the larger of the summed long-running containers and the largest init container, plus 256 MB for `kubelet`, `kube-proxy` and `containerd`, rounded up to the next
supported size (0.25 vCPU / 0.5 GB up to 16 vCPU / 120 GB; the smallest size if none is requested). The extra 256 MB can push a pod up a size (1 vCPU with 8 GB provisions 2 vCPU with 9 GB). Check the chosen size:
`kubectl get pod x -o jsonpath='{.metadata.annotations.CapacityProvisioned}'`.
Fargate pods run with guaranteed QoS, so set requests equal to limits. Ephemeral storage is 20 GiB
by default (somewhat less is usable), up to 175 GiB via `ephemeral-storage` requests.

## 4. Logging
No DaemonSets on Fargate. Use the built-in Fluent Bit router: create namespace
`aws-observability` with label `aws-observability: enabled` and a ConfigMap
`aws-logging` (maximum 5300 characters) containing `output.conf` and
optional `filters.conf`/`parsers.conf`; only `[FILTER]`, `[OUTPUT]` and `[PARSER]` sections are accepted, with outputs `es`, `firehose`/`kinesis_firehose`, `cloudwatch`/`cloudwatch_logs` or `kinesis`, and filters `grep`, `parser`, `record_modifier`, `rewrite_tag`, `throttle`, `nest`, `modify` or `kubernetes`. ConfigMap changes apply only to new pods. The pod execution role needs permissions for the
destination; plan about 50 MB of memory for the log router (up to 100 MB at very high throughput). `kubectl describe pod` shows whether logging is enabled.

## 5. What does not work on Fargate
DaemonSets, privileged containers, hostNetwork/hostPort, GPUs and Inferentia, Arm processors, EBS volumes (EFS works through static provisioning, not dynamic), Fargate Spot, Windows containers, alternate CNI plugins, Outposts/Wavelength/Local Zones, public subnets. Each pod has its own compute boundary, kernel and network interface, so subnets must have room, and load balancers must use IP targets.

## Gotchas
- A pod stuck `Pending` with no events often matches no profile, or its namespace
  matches but labels do not.
- Patching: EKS periodically patches Fargate pods and may need to delete pods it cannot evict; see "Set actions for AWS Fargate OS patching events" in the EKS guide.
- Completed Jobs keep their pods (and cost) on Fargate; set `ttlSecondsAfterFinished`.

## Verify
- [ ] `kubectl get pods -o wide` shows each profile workload on its own Fargate node.
- [ ] CoreDNS runs and resolves in Fargate-only clusters.
- [ ] App logs arrive in the configured destination via `aws-logging`.

## Checked
Checked 2026-10-24 against the Amazon EKS User Guide (Fargate, Fargate profile, Pod configuration, Fargate logging) and the AWS Prescriptive Guidance CoreDNS pattern.
Confirmed: selector limit and wildcards, private-subnet requirement, immutable profiles, profile matching and tie-break, pod execution role purpose and service principal, memory and CPU sizing rules, size table up to 16 vCPU / 120 GB, CapacityProvisioned annotation, guaranteed QoS, ephemeral storage 20 GiB default and 175 GiB maximum, unsupported features list, Fargate logging ConfigMap rules, memory sizing for the log router, CoreDNS compute-type annotation removal and rollout restart.
Removed as unconfirmed: aws:SourceArn trust condition, managed policy name, Pod Identity statement, network policy statement, CoreDNS add-on computeType setting, 30-60 s start time.

Method: documentation only; no commands were run.
