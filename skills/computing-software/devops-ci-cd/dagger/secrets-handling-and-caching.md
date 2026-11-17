---
id: computing-software.devops-ci-cd.dagger.secrets-handling-and-caching
name: secrets-handling-and-caching
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, secrets, secret-providers, cache-key, dockerfile-secrets, 1password, vault, aws]
level: practitioner
status: docs-checked
description: "Pass secrets into Dagger Functions from env, file, command, 1Password, Vault or AWS, mount them in containers and Dockerfile builds, and set a secret cacheKey."
sources: [https://docs.dagger.io/0.21/extending/secrets, https://docs.dagger.io/0.21/cookbook/secrets]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secrets in Dagger Functions

Goal: use passwords and tokens without leaking them to logs, container filesystems or the cache. Dagger 0.21 docs.

## Take a Secret argument
```go
func (m *MyModule) GithubApi(ctx context.Context, token *dagger.Secret) (string, error) {
	return dag.Container().From("alpine:3.17").
		WithSecretVariable("GITHUB_API_TOKEN", token).
		WithExec([]string{"apk", "add", "curl"}).
		WithExec([]string{"sh", "-c", `curl "https://api.github.com/repos/dagger/dagger/issues" --header "Authorization: Bearer $GITHUB_API_TOKEN"`}).
		Stdout(ctx)
}
```
Core API without a module: `with-secret-variable MY_SECRET env://API_TOKEN`.

## Providers (CLI value syntax)
- Environment: `--token=env://GITHUB_API_TOKEN`
- File: `--token=file://./github.txt`
- Command output: `--token=cmd://"gh auth token"`
- 1Password: `op://infra/github/credential` (with a service account set `OP_SERVICE_ACCOUNT_TOKEN`)
- Vault: `vault://credentials.github` (set `VAULT_ADDR` and `VAULT_TOKEN` or `VAULT_APPROLE_ROLE_ID`)
- AWS Secrets Manager `aws+sm://prod/github/token`, JSON field `aws+sm://prod/credentials?field=github_token`; Parameter Store `aws+ps://prod/github/token`. Needs AWS credentials (env vars, shared credentials file or IAM role) and `AWS_REGION`.

## Mount a file as a secret
```go
WithMountedSecret("/root/.config/gh/hosts.yml", ghCreds)
```
Called with `dagger call github-auth --gh-creds=file://$HOME/.config/gh/hosts.yml`.

## Secret in a Dockerfile build
Create a secret whose name equals the Dockerfile mount id, then pass it to `DockerBuild`:
```go
secretVal, err := secret.Plaintext(ctx)
buildSecret := dag.SetSecret("gh-secret", secretVal)
return source.DockerBuild(dagger.DirectoryDockerBuildOpts{Secrets: []*dagger.Secret{buildSecret}}), nil
```
The Dockerfile uses `RUN --mount=type=secret,id=gh-secret ... $(cat /run/secrets/gh-secret)`; the secret appears at `/run/secrets/SECRET-ID`. Run `dagger call build --source=. --secret=env://GITHUB_API_TOKEN`.

## Caching behaviour
By default layer cache entries for operations using a secret key off its plaintext: same plaintext shares cache, different plaintext does not (even with the same `env://` reference). For rotating secrets that should still share cache, set `cacheKey`: `--token=env://GITHUB_API_TOKEN?cacheKey=my-cache-key` or in Dagger Shell `$(secret env://GITHUB_API_TOKEN --cache-key my-cache-key)`.

## Security
- Secrets are scrubbed from logs and output streams.
- Do not write secret plaintext to a file; the page warns it could then be stored in the Dagger cache.
- Secrets are scoped to the defining module; share across modules only by passing a reference through constructor or function arguments.

Related: function-caching-policies (SetSecret limits persistent function caching).

## Checked

2026-11-07

Read extending/modules/secrets.mdx (live slug /extending/secrets) and cookbook/secrets.mdx (live slug /cookbook/secrets) in full; both cited URLs match the live slugs. The cookbook page imports three partials (_use-secret-variable, _mount-files-as-secret, _dockerfile-build) and the Go snippets secret-variable, secret-file and secret-dockerfile, which I read in full while checking secret-type-sources; the extending page's own Go, Python, TypeScript and PHP snippet tabs (snippets/secrets/*) were not opened. Confirmed the with-secret-variable example, provider list and syntax, prerequisites, the mounted secret and Dockerfile build examples, the default plaintext-based caching, the cacheKey syntax for both CLI and Dagger Shell, and the three security bullets. Softened 'Never write secret plaintext' to the page's 'should not' wording. The cross-reference about SetSecret and function caching comes from another page.

Method: documentation only; no commands were run.
