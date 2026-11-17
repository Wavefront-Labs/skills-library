---
id: computing-software.cybersecurity-defensive.threat-modelling.kubernetes-threat-modelling
name: kubernetes-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling, kubernetes-threat-modelling, microsoft-threat-matrix-for-kubernetes, trust-boundaries, cluster-security]
level: advanced
status: docs-checked
description: "Threat model a Kubernetes platform: use the Microsoft Threat Matrix for Kubernetes tactics as prompts and map each to the cluster security mechanisms Kubernetes documents."
sources: ["https://microsoft.github.io/Threat-Matrix-for-Kubernetes/", "https://kubernetes.io/docs/concepts/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes threat modelling

Use the Microsoft Threat Matrix for Kubernetes as the threat prompt list and the Kubernetes
security overview as the list of controls to check against each one.

## Threat prompts: matrix tactics
The matrix has ten tactics: Initial Access, Execution, Persistence, Privilege Escalation,
Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection and Impact. For
each tactic, ask which techniques apply to your cluster. Techniques named on the page
include:
- Using cloud credentials, compromised image in registry, kubeconfig file, application
  vulnerability, exposed sensitive interfaces, and application credentials in configuration
  files.
- Exec into container, bash/cmd inside container, new container, Kubernetes CronJob,
  application exploit (RCE), SSH server running inside container, and sidecar injection.
- Backdoor container, writable hostPath mount, static pods, and malicious admission
  controller.
- Privileged container, cluster-admin binding, hostPath mount, and access to the cloud
  resources, managed identity credentials and instance metadata API.
- Clear container logs, delete K8S events, and pod or container name similarity.
- List K8S secrets, mount service principal, container service account, and access to the
  Kubernetes API server and the Kubelet API.
- Network mapping, cluster internal networking, CoreDNS poisoning, and ARP poisoning and IP
  spoofing.
- Data destruction, resource hijacking and denial of service.
The page states its purpose is to educate on Kubernetes-based tactics, techniques and
procedures, not to teach how to weaponise them.

## Controls to check (Kubernetes security overview)
- **Control plane**: control access to the Kubernetes API; Kubernetes expects TLS for
  encryption in transit within the control plane and to its clients; encryption at rest can be
  enabled for control plane data and is separate from encrypting your own workloads' data.
- **Secrets**: the Secret API gives basic protection for confidential configuration values.
- **Workload**: Pod Security Standards isolate pods and containers; RuntimeClasses define custom
  isolation; NetworkPolicies control traffic between pods and to the outside.
- **Admission control**: plugins that intercept API requests and can validate or mutate them;
  ValidatingAdmissionPolicy is a declarative restriction on API changes.
- **Auditing**: audit logging records the sequence of actions by users, applications using the
  API, and the control plane itself.
- **Cloud provider**: the overview points to each provider's own security documentation.
- Related pages the overview lists: RBAC good practices, service accounts, multi-tenancy,
  good practices for Secrets, API server bypass risks and the security checklists.

## Output
Register each applicable technique against the trust boundary it crosses, name the
mechanism that addresses it, and record an owner.

## Verify
- [ ] Every matrix tactic was considered for the cluster.
- [ ] Each "mitigated" claim names a specific Kubernetes mechanism that is actually enabled.

## Checked
Confirmed 2026-11-09 against the Microsoft Threat Matrix for Kubernetes home page (tactics, technique names and disclaimer) and the Kubernetes Security concepts overview (read in full).
Removed as unconfirmed: the seven-boundary list, the stage-by-control table (the page text gives techniques without their tactic columns, so no technique was mapped to a tactic), kubectl auth can-i, IMDSv2 hop limit, Falco, Tetragon, Kyverno, Gatekeeper, kube-bench and kubescape references, the node pool and etcd platform threats, and the MITRE ATT&CK Containers source, which is an unreadable host.
Method: docs-checked 2026-11-09 against microsoft.github.io Threat-Matrix-for-Kubernetes and kubernetes.io docs concepts security
