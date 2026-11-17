---
id: computing-software.devops-ci-cd.dagger.secrets-providers
name: secrets-providers
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, secrets, secret-provider, vault, 1password, aws, env, security]
level: practitioner
status: docs-checked
description: "Pass secrets to Dagger functions as Secret arguments from env, file, cmd, Vault, 1Password or AWS Secrets Manager and Parameter Store providers."
sources: [https://docs.dagger.io/0.21/features/secrets, https://docs.dagger.io/0.21/cookbook/secrets]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger secrets and providers

Goal: give a function a credential without leaking it into logs, container filesystems or cache (Dagger 0.21 docs).

## Function side

Take a `Secret` argument and attach it with `WithSecretVariable` (Go):
```go
func (m *MyModule) GithubApi(ctx context.Context, token *dagger.Secret) (string, error) {
	return dag.Container().
		From("alpine:3.17").
		WithSecretVariable("GITHUB_API_TOKEN", token).
		WithExec([]string{"apk", "add", "curl"}).
		WithExec([]string{"sh", "-c", `curl "https://api.github.com/repos/dagger/dagger/issues" --header "Accept: application/vnd.github+json" --header "Authorization: Bearer $GITHUB_API_TOKEN"`}).
		Stdout(ctx)
}
```
Python: `token: dagger.Secret` and `.with_secret_variable("GITHUB_API_TOKEN", token)`. Dagger's safeguards keep the value out of plaintext logs, container filesystems and cache.

## Caller side: provider URIs

Pass the secret as an argument value with a provider scheme:
- `env://NAME` host environment variable; `file://` host file; `cmd://` output of a host command.
- Vault: `dagger call github-api --token=vault://credentials.github`
- 1Password (CLI must be authenticated, e.g. `op signin`): `--token=op://infra/github/credential`
- AWS Secrets Manager: `--token=aws+sm://prod/github/token`; JSON field: `aws+sm://prod/database/credentials?field=password`; query params `region`, `version`, `stage` (e.g. `?stage=AWSPREVIOUS`).
- AWS Parameter Store: `--api-key=aws+ps:///prod/api-key` (path starts with `/`; SecureString decrypted automatically).

AWS authentication uses the SDK default credential chain: env vars (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`), the shared credentials file, then IAM role credentials. Set the region with `AWS_REGION` or the `region` query parameter. The AWS provider only reads secrets.

## Gaps

The Secrets Integration page names the `env`, `file` and `cmd` providers but shows them only in videos; the `env://`, `file://` and `cmd://` URI forms above come from the cookbook secrets page, which is why it is also a source.

## Checked

2026-11-07

Read introduction/features/secrets.mdx in full (live slug /features/secrets; the cited /introduction/features/secrets URL is a file path that 404s, fixed in sources) plus its Go and Python snippets (PHP, TypeScript and Java tabs and the three videos not opened). Confirmed the provider list, the safeguards statement, the vault, op signin and 1Password examples, the AWS Secrets Manager and Parameter Store examples, query parameters, credential chain order, region setting, and the read-only note. The env/file/cmd URI forms are not spelled out in the page text; I confirmed them on cookbook/secrets (via the _use-secret-variable partial) and added that page to sources. Removed the sentence claiming the same URI forms work in .env defaults, which is not on any page I read for this skill.

Method: documentation only; no commands were run.
