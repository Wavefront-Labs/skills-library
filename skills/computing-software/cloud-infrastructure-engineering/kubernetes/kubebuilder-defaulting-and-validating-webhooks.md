---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubebuilder-defaulting-and-validating-webhooks
name: kubebuilder-defaulting-and-validating-webhooks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operators-controllers, kubebuilder-webhooks, admission-webhooks, controller-runtime, cert-manager]
level: practitioner
status: docs-checked
description: "Add defaulting and validating webhooks to a kubebuilder operator, implement the typed Defaulter and Validator, wire certificates and test with envtest."
sources: ["https://book.kubebuilder.io/cronjob-tutorial/webhook-implementation", "https://book.kubebuilder.io/cronjob-tutorial/running-webhook", "https://book.kubebuilder.io/cronjob-tutorial/running", "https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/webhook/admission"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defaulting and validating webhooks in kubebuilder

## Scaffold
```bash
kubebuilder create webhook --group data --version v1 --kind Database --defaulting --programmatic-validation
```
This scaffolds the webhook functions and registers the webhook with the manager in `main.go`
(the Kubebuilder CronJob tutorial puts the Go file under `internal/webhook/v1/`), plus manifests
under `config/webhook`. Custom paths are possible with `--defaulting-path` and `--validation-path`.

## Implement
In the current Kubebuilder CronJob tutorial the defaulter and validator are separate structs with
typed, context-taking methods, registered with `ctrl.NewWebhookManagedBy(mgr, &datav1.Database{})
.WithValidator(...).WithDefaulter(...).Complete()`. Older releases used `runtime.Object` arguments
(`CustomDefaulter`/`CustomValidator`); keep whatever signature your scaffold generated.
```go
// +kubebuilder:webhook:path=/mutate-data-example-com-v1-database,mutating=true,failurePolicy=fail,sideEffects=None,groups=data.example.com,resources=databases,verbs=create;update,versions=v1,name=mdatabase-v1.kb.io,admissionReviewVersions=v1
type DatabaseCustomDefaulter struct{}

func (d *DatabaseCustomDefaulter) Default(_ context.Context, db *datav1.Database) error {
    if db.Spec.Replicas == nil { r := int32(1); db.Spec.Replicas = &r }
    return nil
}

// +kubebuilder:webhook:path=/validate-data-example-com-v1-database,mutating=false,failurePolicy=fail,sideEffects=None,groups=data.example.com,resources=databases,verbs=create;update,versions=v1,name=vdatabase-v1.kb.io,admissionReviewVersions=v1
type DatabaseCustomValidator struct{}

func (v *DatabaseCustomValidator) ValidateUpdate(_ context.Context, oldDB, newDB *datav1.Database) (admission.Warnings, error) {
    if oldDB.Spec.Engine != newDB.Spec.Engine {
        return nil, field.Forbidden(field.NewPath("spec", "engine"), "engine is immutable")
    }
    return nil, nil
}
```
(Also `ValidateCreate` and `ValidateDelete`; the marker `verbs` list controls which operations the
generated configuration sends.) Prefer CRD schema and CEL rules for simple checks; use webhooks for
logic that needs code or lookups. The Kubebuilder docs state that validating webhooks run after all
mutating webhooks.

## Certificates
Enable the webhook and cert-manager sections in `config/default/kustomization.yaml` (the "Deploying
Admission Webhooks" page says the webhook-related resources and the webhook manager patch must be
uncommented); cert-manager issues the serving cert and its CA injector fills `caBundle`.
Locally, the Kubebuilder docs say you must generate certificates and place them where the webhook
server looks (by default `/tmp/k8s-webhook-server/serving-certs/tls.{crt,key}`), and recommend
disabling webhooks in the local code-run-test cycle with `make run RUN_ARGS=--webhook-port=-1`.

## Test
The scaffolded `webhook_suite_test.go` starts envtest with `WebhookInstallOptions`; write tests that
create invalid objects and expect errors.

## Verify
`kubectl apply` of an object changing `spec.engine` is rejected with the message above; a new object
without replicas comes back with `replicas: 1`.

## Checked
Checked 2026-10-24 against the Kubebuilder book source (CronJob tutorial: webhook implementation, markers,
`NewWebhookManagedBy`, running locally and `--webhook-port=-1`, deploying webhooks and cert-manager
kustomize sections; testdata project `internal/webhook/v1` and envtest `WebhookInstallOptions`) and
controller-runtime (`certDir` default under the temp dir).
Removed: the `ENABLE_WEBHOOKS=false` toggle, which the current tutorial replaces with `--webhook-port=-1`.
Method: documentation only; no commands were run.
