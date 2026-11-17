---
id: computing-software.devops-ci-cd.dagger.secret-type-sources
name: secret-type-sources
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, secret, secrets, 1password, vault, aws-secrets-manager, dockerfile]
level: practitioner
status: docs-checked
description: "Pass secrets to Dagger Functions from env, file, command, 1Password, Vault or AWS, and mount them as variables, files or Dockerfile build secrets."
sources: [https://docs.dagger.io/0.21/getting-started/types/secret]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger Secret type and sources (Dagger 0.21 docs)

Goal: use credentials without exposing them in logs, container filesystems or the cache. `Secret` has `name` and `plaintext`.

## Use a secret variable (Go)

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

## URI schemes for the argument

```shell
dagger call github-api --token=env://GITHUB_API_TOKEN
dagger call github-api --token=file://./github.txt
dagger call github-api --token=cmd://"gh auth token"
dagger call github-api --token=op://infra/github/credential
dagger call github-api --token=vault://credentials.github
dagger call github-api --token=aws+sm://prod/github/token
dagger call github-api --token=aws+sm://prod/credentials?field=github_token
dagger call github-api --token=aws+ps://prod/github/token
```

Prerequisites per provider:
- 1Password service account: `OP_SERVICE_ACCOUNT_TOKEN` set.
- Vault: `VAULT_ADDR` plus `VAULT_TOKEN`, or `VAULT_APPROLE_ROLE_ID` for AppRole.
- AWS: credentials via `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`, `~/.aws/credentials` or an IAM role, and `AWS_REGION` set. `aws+sm` is Secrets Manager (JSON secrets: `?field=`), `aws+ps` is Parameter Store.

## Mount a file as a secret

```go
WithMountedSecret("/root/.config/gh/hosts.yml", ghCreds)
```

```shell
dagger call github-auth --gh-creds=file://$HOME/.config/gh/hosts.yml
```

## Secret in a Dockerfile build

Secrets appear at `/run/secrets/<id>` in the build. The secret's name must match the Dockerfile mount id:

```go
secretVal, err := secret.Plaintext(ctx)
buildSecret := dag.SetSecret("gh-secret", secretVal)
return source.DockerBuild(dagger.DirectoryDockerBuildOpts{Secrets: []*dagger.Secret{buildSecret}}), nil
```

Dockerfile: `RUN --mount=type=secret,id=gh-secret curl ... --header "Authorization: Bearer $(cat /run/secrets/gh-secret)"`. Run: `dagger call build --source=. --secret=env://GITHUB_API_TOKEN`.

Related: computing-software.devops-ci-cd.dagger.container-type-and-caching.

## Checked

2026-11-07

Read getting-started/types/secret.mdx in full (live slug /getting-started/types/secret matches the cited URL). The page only imports partials, so I also read partials/types/_secret.mdx and the three cookbook partials _use-secret-variable, _mount-files-as-secret and _dockerfile-build, plus the Go snippets secret-variable, secret-file and secret-dockerfile (Python and TypeScript snippets not opened). Confirmed the Secret description and name/plaintext fields, WithSecretVariable usage, every URI scheme example (env, file, cmd, op, vault, aws+sm with ?field=, aws+ps), the 1Password, Vault and AWS prerequisites, the mounted secret example and command, the Dockerfile build snippet, /run/secrets mount location, the Dockerfile mount line and the dagger call build command. No corrections needed.

Method: documentation only; no commands were run.
