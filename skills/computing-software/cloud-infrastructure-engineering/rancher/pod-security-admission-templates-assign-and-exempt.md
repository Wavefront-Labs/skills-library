---
id: computing-software.cloud-infrastructure-engineering.rancher.pod-security-admission-templates-assign-and-exempt
name: pod-security-admission-templates-assign-and-exempt
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [psa, pod-security-admission, rancher-restricted, rancher-privileged, exemptions, namespaces, cluster-templates]
level: advanced
status: docs-checked
description: "Apply Rancher PSA configuration templates (rancher-privileged, rancher-restricted) to downstream clusters, edit them safely, and exempt required Rancher namespaces."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/psa-config-templates
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/pod-security-standards
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pod Security Standards (PSS) define security levels and Pod Security Admission (PSA) enforces them. Both were on by default from Kubernetes v1.23 and replace Pod Security Policies from v1.25. Rancher adds **PSA configuration templates**, a custom resource available from Rancher v2.7.2.

Two templates ship by default:

- `rancher-privileged`: the most permissive; restricts nothing and allows known privilege escalations. It has no exemptions.
- `rancher-restricted`: heavily restricted, following current pod hardening practice. You must make namespace-level exemptions for Rancher's own components.

The shipped policies are a compromise between security and convenience. For something stricter, write your own, and the page says that if Rancher's policies are preferred you need admission controllers blocking creation in the exempted namespaces.

Assign a template when creating a downstream cluster (**Cluster: Create > Basics > Security > Pod Security Admission Configuration Template**) or later via the cluster's **Edit Config**.

Admins manage templates under **Advanced > Pod Security Admissions**. Caution: editing a template in use changes every cluster assigned to it. To let a non-admin manage templates, bind a role granting all verbs on `management.cattle.io/podsecurityadmissionconfigurationtemplates`; such a user can then change restriction levels on all clusters using that template, even ones they have no access to.

On clusters enforcing a restrictive policy, namespaces such as `calico-system`, `cattle-fleet-system`, `cattle-monitoring-system` and `cattle-logging-system` must be exempted or Rancher system pods may not run; the page has the full list.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Pod Security Admission Configuration Templates; Pod Security Standards & Pod Security Admission. Nothing removed.

Method: documentation only; no commands were run.
