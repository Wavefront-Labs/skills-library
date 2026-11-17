---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-profile-contributors
name: kubeflow-profile-contributors
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [contributors, rolebinding, authorizationpolicy, kubeflow-userid, manage-contributors]
level: practitioner
status: docs-checked
description: "Add contributors to a Kubeflow profile via the dashboard (edit only) or manually with the RoleBinding and AuthorizationPolicy pair that grants view or edit."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/central-dash/profiles.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Profile contributors

Contributors exist only by the presence of specific RoleBinding and AuthorizationPolicy resources in the profile namespace.

Dashboard method: the profile owner uses Manage Contributors, in the Contributors to your namespace field. This only grants edit access. For view access use the manual method.

Manual method, for each contributor create both:

1. A RoleBinding named `user-<EMAIL>-clusterrole-<ROLE>` with annotations `role` and `user`, `roleRef` to ClusterRole `kubeflow-<ROLE>`, subject kind `User` named by the exact (case-sensitive) email. In names, the email is lowercased with special characters replaced by `-`; ROLE is `edit` or `view`.

2. An Istio AuthorizationPolicy (`security.istio.io/v1beta1`) of the same name and annotations. Its rule allows principals:
   - `cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account` (required for notebooks)
   - `cluster.local/ns/kubeflow/sa/ml-pipeline-ui` (required for pipelines)

   with a condition on `request.headers[kubeflow-userid]` whose value is the contributor email.

Both resources go in the profile namespace. The page gives the principal templates `cluster.local/ns/<ISTIO_GATEWAY_NAMESPACE>/sa/<ISTIO_GATEWAY_SERVICE_ACCOUNT>` and `cluster.local/ns/<KUBEFLOW_NAMESPACE>/sa/<KFP_UI_SERVICE_ACCOUNT>`, so substitute your own namespaces and ServiceAccount names if Kubeflow or the Istio gateway is deployed elsewhere.

## Checked

2026-11-08. Confirmed against the Profiles and Namespaces page (Manage Profile Contributors section): the dashboard limitation, RoleBinding and AuthorizationPolicy structure, annotations, name rules and principals. Removed an unsupported sentence about deleting the resources.
Method: docs-only read of cited pages, 2026-11-08
