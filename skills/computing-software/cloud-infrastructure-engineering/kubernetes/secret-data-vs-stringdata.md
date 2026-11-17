---
id: computing-software.cloud-infrastructure-engineering.kubernetes.secret-data-vs-stringdata
name: secret-data-vs-stringdata
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, secret, stringdata, base64-decode, kubectl-create-secret]
level: practitioner
status: docs-checked
description: "Write and read Secrets correctly: data (base64) vs stringData (plain), decoding values, trailing newline traps, and why base64 is not encryption."
sources: ["https://kubernetes.io/docs/concepts/configuration/secret/", "https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-config-file/", "https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-kubectl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret data vs stringData

```yaml
apiVersion: v1
kind: Secret
metadata: {name: db}
type: Opaque
data:
  username: YXBw              # base64 of "app"
stringData:
  password: "s3cr3t!"         # plain; API server encodes it into data on write
```
- `stringData` is a convenience field: the string is encoded for you when the Secret is created or updated, and reads return the encoded values, not the plaintext you provided.
- If a key is in both, `stringData` wins.

## Encoding without traps
```bash
echo -n 'app' | base64          # -n: no trailing newline
printf %s 'app' | base64
```
`echo 'app' | base64` encodes `app\n`; the app then fails auth with a password that looks right.
Newlines are not valid inside the base64 strings: on Linux add `-w 0` (or pipe through `tr -d '\n'`); on macOS avoid the `-b` option.

## Reading
```bash
kubectl get secret db -o jsonpath='{.data.password}' | base64 --decode
```

## Creating without YAML
```bash
kubectl create secret generic db --from-literal=username=app --from-file=password=./pw.txt
```
`--from-file` keeps the file's trailing newline if it has one: `printf %s` into the file.

## Security reminders
- Base64 is encoding, not encryption; anyone allowed to `get` Secrets can read them.
- The Kubernetes docs note that `stringData` does not work well with server-side apply; client-side `kubectl apply` records the applied configuration in the `kubectl.kubernetes.io/last-applied-configuration` annotation.

## Checked
Checked 2026-10-24 against the Secret page and the Managing Secrets using a configuration file and using kubectl tasks (website main, v1.37): stringData is encoded on create or update and not returned in plaintext, stringData wins over data for the same key, `echo -n` and file newline warning, `base64 -w 0` and macOS `-b` note, `--from-file` and `--from-literal`, the server-side apply note, the last-applied annotation. Removed the unconfirmed base64-validity claim, 76-character wrap, go-template and jq decoders, and tool recommendations.
Method: documentation only; no commands were run.
