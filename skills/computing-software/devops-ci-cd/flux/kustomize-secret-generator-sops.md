---
id: computing-software.devops-ci-cd.flux.kustomize-secret-generator-sops
name: kustomize-secret-generator-sops
category: computing-software
field: devops-ci-cd
product: flux
tags: [sops, secretgenerator, kustomize, encrypted-files, env]
level: advanced
status: docs-checked
description: "Store SOPS-encrypted files as Secrets through the Kustomize secretGenerator and have kustomize-controller decrypt them."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SOPS-encrypted data can be committed as a file and turned into a Secret by Kustomize `secretGenerator`. kustomize-controller scans the values of generated Secrets and decrypts any that are SOPS encrypted before applying.

```console
$ echo "my-secret-token" | sops -e /dev/stdin > token.encrypted
$ cat <<EOF > kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

secretGenerator:
 - name: token
   files:
   - token=token.encrypted
EOF
```

Commit and push `token.encrypted` and `kustomization.yaml`.

For files in `.json`, `.yaml`, `.ini` or `.env` format, give SOPS the input type when encrypting:

```sh
sops -e --input-type=json config.json > config.json.encrypted
sops -e --input-type=yaml config.yaml > config.yaml.encrypted
sops -e --input-type=dotenv --output-type=dotenv config.env > config.env.encrypted
```

For a JSON config the generated key must end in `.json` (`config.json=config.json.encrypted`). For dotenv files use the `envs` directive (`envs: [config.env.encrypted]`). For Docker config files, encrypt with `--input-type=json --output-type=json` and use `type: kubernetes.io/dockerconfigjson` with the key `.dockerconfigjson`.

## Checked

2026-11-08. partial read of https://github.com/fluxcd/kustomize-controller/blob/main/docs/spec/v1/kustomizations.md: only the Kustomize secretGenerator section.

Removed or corrected: the content-hash suffix claim and the closing advice, and the separate decryption-requirement sentence, none of which is in the secretGenerator section.

Method: documentation only; no commands were run.
