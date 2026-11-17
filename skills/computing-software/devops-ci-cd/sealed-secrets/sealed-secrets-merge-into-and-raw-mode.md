---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-merge-into-and-raw-mode
name: sealed-secrets-merge-into-and-raw-mode
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, kubeseal, merge-into, raw, update-secret, stdin, editor-integration]
level: practitioner
status: docs-checked
description: "Add or update single items in an existing SealedSecret with kubeseal --merge-into, or encrypt a bare value with --raw while matching scope, name and namespace."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets merge into and raw mode

Updating without the old plaintext: you can paste a newly encrypted item into an existing SealedSecret, or let `kubeseal` do it:

```bash
echo -n bar | kubectl create secret generic mysecret --dry-run=client --from-file=foo=/dev/stdin -o json \
  | kubeseal > mysealedsecret.json
echo -n baz | kubectl create secret generic mysecret --dry-run=client --from-file=bar=/dev/stdin -o json \
  | kubeseal --merge-into mysealedsecret.json
```

New items must be sealed with a compatible name and namespace for the SealedSecret's scope.

Raw mode (marked experimental) avoids the temporary Secret: `kubeseal --raw` encrypts one value to stdout and you embed it in the resource yourself. It is also a building block for editor integrations. You are responsible for consistency of scope, namespace and name.

```bash
echo -n foo | kubeseal --raw --namespace bar --name mysecret          # strict
echo -n foo | kubeseal --raw --namespace bar --scope namespace-wide
echo -n foo | kubeseal --raw --scope cluster-wide
```

For `namespace-wide` and `cluster-wide`, also add the matching annotation to the SealedSecret metadata (`sealedsecrets.bitnami.com/namespace-wide: "true"` or `sealedsecrets.bitnami.com/cluster-wide: "true"`), otherwise the missing annotation means strict scope.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Update existing secrets, Raw mode, Scopes.
Confirmed: `--merge-into` example, `--raw` with `--namespace`, `--name`, `--scope`, experimental label, the two scope annotations.
Removed: the claim that decryption fails when the annotation is missing (the README only says no annotation means strict).
Method: documentation only; no commands were run.
