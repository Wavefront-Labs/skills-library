---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-seal-and-apply-workflow
name: sealed-secrets-seal-and-apply-workflow
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, kubeseal, workflow, dry-run, namespace, kubectl, seal-secret]
level: intro
status: docs-checked
description: "Create a Secret locally with kubectl --dry-run, seal it with kubeseal, apply the SealedSecret and rely on name and namespace matching the resulting Secret."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets seal and apply workflow

Basic loop:

```bash
echo -n bar | kubectl create secret generic mysecret --dry-run=client --from-file=foo=/dev/stdin -o json >mysecret.json
kubeseal -f mysecret.json -w mysealedsecret.json
kubectl create -f mysealedsecret.json
kubectl get secret mysecret
```

The `--dry-run=client` matters: the Secret is just a local file, never sent to the cluster. After sealing, `mysealedsecret.json` is safe to commit or share.

Points to remember:
- The SealedSecret and the Secret must have the same namespace and name (in the default strict scope). This is deliberate protection against other cluster users reusing your sealed secrets.
- `kubeseal` determines the namespace from the input Secret, then an explicit `--namespace` argument, then the `kubectl` default namespace, in that order of precedence as the README lists them.
- Labels, annotations and the like on the original Secret are preserved on the Secret but not automatically reflected in the SealedSecret; use `spec.template` for that.
- Several Secrets can go in one file: separate YAML documents with `---`, or supply extra single objects in JSON.
- There is no user authentication in the scheme. Any user can create a SealedSecret containing any Secret they like as long as name and namespace match, so protect the apply path with RBAC and your deployment workflow.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Usage, FAQ on multiple secrets, SealedSecrets as templates.
Confirmed: the command loop, same namespace and name requirement, namespace precedence, labels/annotations not reflected, multi-document files, no user authentication.
Removed: nothing.
Method: documentation only; no commands were run.
