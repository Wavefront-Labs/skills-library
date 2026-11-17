---
id: computing-software.devops-ci-cd.dagger.function-arguments-secrets
name: function-arguments-secrets
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, functions, arguments, secrets, 1password, vault, gcp-secret-manager]
level: practitioner
status: docs-checked
description: "Accept a Secret argument in a Dagger Function and supply it from env, file, cmd, 1Password, Vault or GCP Secret Manager providers; note caching behavior."
sources: [https://docs.dagger.io/0.21/extending/arguments, https://docs.dagger.io/0.21/cookbook/secrets]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Secret arguments and providers

Goal: use a credential in a Function without exposing it in plaintext logs or writing it into container filesystems (Dagger 0.21 docs).

## Function side

Declare the argument as the `Secret` type and attach it with `withSecretVariable`:

```go
func (m *MyModule) GithubApi(ctx context.Context, token *dagger.Secret) (string, error) {
	return dag.Container().From("alpine:3.17").
		WithSecretVariable("GITHUB_API_TOKEN", token).
		WithExec([]string{"apk", "add", "curl"}).
		WithExec([]string{"sh", "-c", `curl "https://api.github.com/repos/dagger/dagger/issues" --header "Accept: application/vnd.github+json" --header "Authorization: Bearer $GITHUB_API_TOKEN"`}).
		Stdout(ctx)
}
```

Python: `token: Annotated[dagger.Secret, Doc("GitHub API token")]` with `.with_secret_variable(...)`. TypeScript: `token: Secret`.

## Caller side (CLI)

```shell
dagger call github-api --token=env://GITHUB_API_TOKEN      # host env var
dagger call github-api --token=file://./github.txt          # host file
dagger call github-api --token=cmd://"gh auth token"        # host command output
dagger call github-api --token=op://infra/github/credential # 1Password
dagger call github-api --token=vault://infra/github.credential
dagger call github-api --token=gcp://github-token
```

Dagger Shell form: `github-api env://GITHUB_API_TOKEN`.

### Provider setup stated by the page

- **1Password**: create a service account and set `OP_SERVICE_ACCOUNT_TOKEN`; without it, the official `op` CLI is used if installed. Reference format `op://VAULT-NAME/ITEM-NAME/[SECTION-NAME/]FIELD-NAME`.
- **Vault**: set `VAULT_ADDR`; token auth via `VAULT_TOKEN`, or AppRole via `VAULT_APPROLE_ROLE_ID` and `VAULT_APPROLE_SECRET_ID` (optionally `VAULT_APPROLE_MOUNT_PATH`, default `approle`). KvV2 scheme `vault://PATH/TO/SECRET.ITEM`; if KvV2 is not mounted at `/secret`, set `VAULT_PATH_PREFIX`.
- **Google Cloud Secret Manager**: Application Default Credentials (set `GOOGLE_APPLICATION_CREDENTIALS`, or `gcloud auth application-default login`, or workload identity/metadata service). Project from `GCP_PROJECT_ID` (fallbacks `GOOGLE_CLOUD_PROJECT`, `GCLOUD_PROJECT`). Paths: `gcp://my-secret`, `gcp://my-secret/versions/2`, `gcp://projects/my-project/secrets/my-secret`, and `gcp://my-secret?ttl=5m` for TTL caching.
- AWS Secrets Manager / Parameter Store are named as supported in the intro; the detail lives in the Secrets Integration docs, not on this page.

## Gotcha: caching

Layer cache entries for operations that include a Secret are keyed on its plaintext value. Same plaintext in two runs may hit the cache; different plaintext will not.

## Checked

2026-11-07

Read extending/modules/arguments.mdx in full (live slug /extending/arguments; the old /extending/modules/arguments URL returned 404, fixed in sources). Confirmed the Secret argument section, host env/file/cmd providers, 1Password (OP_SERVICE_ACCOUNT_TOKEN, op CLI fallback, reference format), Vault (VAULT_ADDR, VAULT_TOKEN, AppRole variables, VAULT_APPROLE_MOUNT_PATH default approle, VAULT_PATH_PREFIX), GCP (ADC options, GCP_PROJECT_ID and fallbacks, the four path forms) and the Caching paragraph. Opened the Go, Python and TypeScript secret-variable snippet files of the cookbook and matched the skill's Go example and Python annotation; the PHP and Java tabs were not opened. No claims removed.

Method: documentation only; no commands were run.
