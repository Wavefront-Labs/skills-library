---
id: computing-software.cybersecurity-defensive.cloud-security.kubernetes-security-hardening
name: kubernetes-security-hardening
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-workload-protection, kubernetes-security-hardening, rbac, network-policies, api-server-access, etcd-encryption, audit-logging, cks, eks, aks, gke]
level: advanced
status: docs-checked
description: "Harden Kubernetes clusters using the upstream security checklist: unexposed API/kubelet/etcd, RBAC, Pod Security Standards, network policies, secrets encryption, audit logs."
sources: ["https://kubernetes.io/docs/concepts/security/security-checklist/", "https://kubernetes.io/docs/concepts/security/rbac-good-practices/", "https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://kubernetes.io/docs/concepts/services-networking/network-policies/", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes security hardening

**Goal:** a cluster where one compromised pod or credential does not become control of the
cluster or the cloud account. The upstream Security Checklist is the backbone; managed services
(EKS, AKS, GKE) expose the same controls through their own settings, so check each vendor's docs.

## Control plane and network
- The Kubernetes API, kubelet API and etcd must not be exposed publicly on the Internet.
- Restrict kubelet API access: the default authentication and authorization settings (no `--config`
  file) are overly permissive.
- etcd: limit access and use mutual TLS with a certificate authority unique to etcd.
- Filter pod access to the cloud metadata API (169.254.169.254) if it is not needed.
- CNI plugins must support network policies; NetworkPolicy objects need such a plugin to have effect.
  Not all CNI plugins encrypt in transit; a service mesh can add it.

## RBAC
- Follow the RBAC Good Practices page; review access periodically (the checklist says no more than 24
  months apart).
- Risky permissions to review: `escalate`, `bind`, `impersonate`, `nodes/proxy`, write access to
  `mutatingwebhookconfigurations`; the right to create Pods or Pod-managing resources gives direct
  access to schedulable nodes unless admission restricts it.
- Do not mount service account tokens into pods that do not need them: set
  `automountServiceAccountToken: false` on the service account or the pod. Use Bound Service Accounts
  (v1.22 and above) for time-bound tokens.

## Workloads
- Apply a Pod Security Standards policy (privileged, baseline, restricted) to every namespace and
  enforce it via Pod Security admission (modes: warn, audit, enforce) or a webhook.
- Set memory and CPU limits; CPU limits throttle and can affect autoscaling.
- Enable Seccomp and AppArmor or SELinux on nodes that support them.
- Reference images by sha256 digest rather than tag, or verify signatures at deploy time via admission.

## Data and logging
- Configure encryption at rest for the Secret API (EncryptionConfiguration; wildcard resource matching
  needs v1.27+). Store secrets in Secrets, not ConfigMaps.
- Enable API server audit logging and protect audit logs from general access.

## Gotchas
- Admission controllers extend the API server and need securing themselves.

## Verify
- [ ] API, kubelet and etcd are unreachable from the Internet.
- [ ] Every namespace has an enforced Pod Security level.

## Checked
2026-11-01. Confirmed on the Kubernetes Security Checklist, RBAC Good Practices, Pod Security Standards,
Network Policies, encrypt-data and audit pages: all items above. Removed (not stated on those pages): cloud
IdP integration specifics, `--disable-local-accounts`, `kubectl auth can-i` and `rbac-tool` usage, specific
CNI names, the 14-month support window, IMDS hop limit, kube-bench/Kubescape and Falco references, and
the "default deny" recommendation.
Method: documentation only; no commands were run.
