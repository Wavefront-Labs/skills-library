---
id: computing-software.devops-ci-cd.jenkins.external-credential-providers-vault-aws
name: external-credential-providers-vault-aws
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, hashicorp-vault-plugin, aws-secrets-manager-credentials-provider, credentials]
level: advanced
status: docs-checked
description: "Source Jenkins credentials from HashiCorp Vault (withVault) or AWS Secrets Manager (credentials provider) instead of storing them in JENKINS_HOME."
sources: ["https://github.com/jenkinsci/hashicorp-vault-plugin", "https://github.com/jenkinsci/aws-secrets-manager-credentials-provider-plugin/blob/master/docs/README.md", "https://github.com/jenkinsci/kubernetes-credentials-provider-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External credential providers (Vault and AWS Secrets Manager)

## HashiCorp Vault plugin
Configure (JCasC):
```yaml
unclassified:
  hashicorpVault:
    configuration:
      vaultUrl: https://vault.example.com
      vaultCredentialId: vault-approle      # AppRole credential (role_id + secret_id)
      engineVersion: 2
```
Use:
```groovy
withVault(vaultSecrets: [[path: 'secret/ci/app', secretValues: [
    [envVar: 'DB_PASSWORD', vaultKey: 'db_password']]]]) {
  sh './migrate.sh'          // secrets are generally masked in the build log
}
```
Auth options documented by the plugin include AppRole (recommended by HashiCorp for servers and automated workflows such as Jenkins), Vault Kubernetes credentials (role plus the pod's JWT), tokens and GitHub tokens.

## AWS Secrets Manager credentials provider
Secrets tagged in AWS appear as read-only Jenkins credentials (id = secret name):
- Tag `jenkins:credentials:type` = `string` | `usernamePassword` | `sshUserPrivateKey` | `file` | `certificate`
- `jenkins:credentials:username` for username types.
The controller's IAM identity needs `secretsmanager:ListSecrets` and `secretsmanager:GetSecretValue`.
The plugin gives a read-only view of Secrets Manager; use the credentials with `credentials()` or
`withCredentials` as normal, and see the plugin's Filters documentation to limit which secrets are listed.

## Choosing
| Need | Option |
|---|---|
| Existing Vault, dynamic DB creds | Vault plugin (`withVault`) |
| AWS shop, static secrets, standard bindings | AWS SM provider |
| Kubernetes controller | Kubernetes Credentials Provider plugin (credentials from Kubernetes Secrets) |

## Gotchas
- Providers are read-only from Jenkins; rotate in the source system.
- The AWS provider caches the credential list (metadata, not values) for 5 minutes when caching is enabled; new secrets appear with delay.
- Masking is best effort; do not print secrets or transformed copies of them.

## Verify
- [ ] The credentials page shows the provider's entries and a job that uses one prints `****`.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: Vault plugin README (`withVault` with `vaultSecrets`, `path`, `secretValues`, `envVar`, `vaultKey`, `engineVersion`, JCasC `hashicorpVault` with `vaultUrl` and `vaultCredentialId`, AppRole and Kubernetes credentials, build-log masking); AWS Secrets Manager credentials provider docs (tags `jenkins:credentials:type` values `string`, `usernamePassword`, `sshUserPrivateKey`, `file`, `certificate`, `jenkins:credentials:username`, IAM actions `secretsmanager:ListSecrets` and `GetSecretValue`, read-only view, 5-minute list cache). Removed the secret_id TTL advice and the unconfirmed masking and store-name claims.
Method: documentation only; no commands were run.
