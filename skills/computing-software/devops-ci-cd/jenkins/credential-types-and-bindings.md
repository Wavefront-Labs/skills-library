---
id: computing-software.devops-ci-cd.jenkins.credential-types-and-bindings
name: credential-types-and-bindings
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, credentials, credential-types, withcredentials, secret-text, secret-file, username-password, ssh-user-private-key, certificate-credential, sshagent, credentials-binding, environment-credentials-helper, groovy-interpolation, log-masking]
level: practitioner
status: docs-checked
description: "Pick the right Jenkins credential type and bind it safely: secret text/file, username-password, SSH key, certificate; withCredentials, sshagent, environment credentials() and masking limits."
sources: ["https://www.jenkins.io/doc/book/using/using-credentials/", "https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#handling-credentials", "https://github.com/jenkinsci/credentials-binding-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credential types and bindings

| Type | Store when | Bind with |
|---|---|---|
| Secret text | API token, webhook secret | `string(credentialsId: 'x', variable: 'TOKEN')` |
| Secret file | kubeconfig, GCP SA JSON, `.npmrc` | `file(credentialsId: 'x', variable: 'KUBECONFIG')` (variable holds a file path) |
| Username with password | registry login, basic auth | `usernamePassword(credentialsId: 'x', usernameVariable: 'U', passwordVariable: 'P')` |
| SSH Username with private key | git over SSH, deploy hosts | `sshUserPrivateKey(credentialsId: 'x', keyFileVariable: 'KEY', usernameVariable: 'U', passphraseVariable: 'PP')` (`usernameVariable` and `passphraseVariable` are optional) |
| Certificate (PKCS#12) | mTLS client cert | `certificate(credentialsId: 'x', keystoreVariable: 'KS', passwordVariable: 'KSP')` |
| Plugin types | GitHub App, AWS keys, Vault | the providing plugin documents its own binding or step |

## Binding
```groovy
withCredentials([usernamePassword(credentialsId: 'registry', usernameVariable: 'REG_USER', passwordVariable: 'REG_PASS')]) {
  sh 'echo "$REG_PASS" | docker login -u "$REG_USER" --password-stdin registry.example.com'
}
```
Declarative shortcut: `environment { REG = credentials('registry') }` supports secret text,
username and password, and secret file credentials. For username and password it sets `REG`
(`username:password`), `REG_USR` and `REG_PSW`. Other credential types need `withCredentials`.

## Rules
- **Single quotes in `sh`.** The Jenkinsfile docs show a double-quoted `sh` that interpolates
  `$TOKEN` in Groovy as WRONG, because process listings can disclose the value; use a
  single-quoted (or triple-single-quoted) script so the shell expands it, with `set +x` first.
- Masking only reduces the risk of accidental exposure (the log shows `****`); it does not stop
  a malicious Pipeline from capturing the value. Do not let untrusted Pipelines use trusted
  credentials.
- Narrow the scope: bind just around the step that needs it, not the whole pipeline.
- Use credential IDs that describe purpose (`prod-deploy-kubeconfig`), not owner.

## Gotchas
- Credential not found: check the ID and that the credential's store (system, a folder, or a
  user) is visible to the job.
- SSH host-key failures: add the host key to the known hosts instead of disabling checking.

## Verify
Run with a dummy credential containing a unique string and search the console log: only `****`
appears.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: credential types list (using-credentials page); `credentials()` helper scope and `_USR`/`_PSW` variables, `withCredentials` bindings and the single-quote guidance (Pipeline Jenkinsfile page); binding symbols `usernamePassword`, `string`, `file`, `certificate`, `sshUserPrivateKey` and their argument names (credentials-binding and ssh-credentials plugin source). Removed the unconfirmed secret-file lifetime, warning text, encoded-secret masking and permission-name claims.
Method: documentation only; no commands were run.
