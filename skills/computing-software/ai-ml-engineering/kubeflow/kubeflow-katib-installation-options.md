---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-installation-options
name: kubeflow-katib-installation-options
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [installation-options, leader-election, katib-postgres, external-db, cert-manager, openshift]
level: practitioner
status: docs-checked
description: "Choose a Katib control plane variant: leader election for HA, PostgreSQL, external MySQL, cert-manager certificates or OpenShift, each a kustomize path."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/installation-options.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib installation options

All variants are applied with `kubectl apply -k "github.com/kubeflow/katib.git/manifests/v1beta1/installs/<variant>?ref=master"`.

| Variant (`installs/` path) | Use it when |
|---|---|
| Default standalone install | Follow the Katib installation guide |
| `katib-leader-election` | You need `katib-controller` highly available (production SLAs) through leader election |
| `katib-standalone-postgres` | You want PostgreSQL instead of MySQL |
| `katib-external-db` | You want your own MySQL instance instead of `katib-mysql` |
| `katib-cert-manager` | You want cert-manager, not the built-in certificate generator, to provision webhook certificates |
| `katib-openshift` | OpenShift 4.4 or newer; the OpenShift service controller provisions webhook certificates |

For the external DB variant, edit `secrets.env` in the `katib-external-db` install directory with your MySQL values for the `katib-db-manager` environment variables.

For the cert-manager variant, cert-manager must already be deployed on the cluster before applying Katib.

After choosing a variant, set environment variables for the Katib components as needed (see the env variables skill).

## Checked

Confirmed each variant path, the PostgreSQL, external MySQL, cert-manager and OpenShift 4.4+ behaviour and the secrets.env step. Removed the default variant path name, the one-active-controller wording and the katib-config advice because the page does not state them.

Method: docs-checked 2026-11-09 against the raw kubeflow/website Katib installation-options.md page, read in full.
