---
id: computing-software.cloud-infrastructure-engineering.cert-manager.configuring-components
name: configuring-components
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [controllerconfiguration, webhookconfiguration, feature-gates, extraargs, config-file, flags]
level: practitioner
status: docs-checked
description: "Configure cert-manager controller, webhook and cainjector through config files, Helm extraArgs and feature gates, and know flag precedence."
sources:
  - https://cert-manager.io/docs/installation/configuring-components/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Precedence: CLI flags override the configuration file. Pass a file with `--config`; in the Helm chart use the `config` value (controller) and `webhook.config` (webhook).

Extra CLI arguments in Helm: `extraArgs`, `webhook.extraArgs`, `cainjector.extraArgs`, `acmesolver.extraArgs`.

Controller file: `apiVersion: controller.config.cert-manager.io/v1alpha1`, `kind: ControllerConfiguration`. Keys shown: `logging.verbosity`, `logging.format`, `leaderElectionConfig.namespace`, `kubernetesAPIQPS`, `kubernetesAPIBurst`, `numberOfConcurrentWorkers`, `gatewayAPI.enabled`, `featureGates`.

Webhook file: `apiVersion: webhook.config.cert-manager.io/v1alpha1`, `kind: WebhookConfiguration`. Keys shown: `logging`, `securePort`, `healthzPort`, `featureGates`.

The sample values on the page are illustrative, not defaults.

Feature gates are set per component with `--feature-gates` or the `featureGates` key; controller, webhook and cainjector each have their own set. Alpha gates are off by default and must be enabled; beta gates are on and can be disabled. Gates named in the examples include AdditionalCertificateOutputFormats, LiteralCertificateSubject, OtherNames, ServerSideApply and UseCertificateRequestBasicConstraints. The page points to separate controller, webhook and cainjector feature gate pages for the full lists.

## Checked

2026-11-03: Confirmed against the Configuring Components page: CLI flags take precedence over the config file, `--config`, Helm `config` and `webhook.config`, the `extraArgs` values for four components, the ControllerConfiguration and WebhookConfiguration apiVersion/kind and keys shown, the examples being illustrative only, and alpha (off by default) versus beta (on by default) feature gates with per-component sets. Removed: the `features.go` source pointer and the note on error behaviour (neither is on this page); the page points to per-component feature gate pages instead.

Method: documentation only; no commands were run.
