---
id: computing-software.devops-ci-cd.github-actions.managing-secrets-with-gh-cli-and-rest-api
name: managing-secrets-with-gh-cli-and-rest-api
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, gh-secret-set, secrets-api, libsodium, sealed-box, secret-automation]
level: practitioner
status: docs-checked
description: "Script secret provisioning: gh secret set/list/delete for repos, envs, orgs and Dependabot, and the REST API flow with the public key and a libsodium sealed box."
sources: ["https://cli.github.com/manual/gh_secret_set", "https://docs.github.com/en/rest/guides/encrypting-secrets-for-the-rest-api"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing secrets with `gh secret` and the REST API

## 1. gh CLI (does the encryption for you)
```bash
gh secret set NPM_TOKEN -R org/repo < token.txt          # stdin avoids shell history
gh secret set DB_URL --env staging --body "$DB_URL"
gh secret set -f .env.ci                                  # dotenv file: secret names and values
gh secret set SNYK_TOKEN --app dependabot                 # actions, agents, codespaces or dependabot
gh secret list -R org/repo --json name,updatedAt
gh secret delete OLD_TOKEN -R org/repo
```
Rotation across many repos:
```bash
gh repo list my-org --limit 500 --json name -q '.[].name' |
  while read r; do gh secret set REGISTRY_TOKEN -R "my-org/$r" --body "$NEW" && echo "$r ok"; done
```
(If it is the same value everywhere, make it one organisation secret instead.)

## 2. Raw REST API (for tools without gh)
The REST secret endpoints require the value encrypted with libsodium (a sealed box) using a Base64 public key you
fetch from the API; the docs say to look at the `encrypted_value` parameter of the endpoint you use to find the
matching public-key endpoint. From the gh source, the key endpoints are
`GET /repos/{owner}/{repo}/{app}/secrets/public-key` (app `actions` or `dependabot`),
`GET /repos/{owner}/{repo}/environments/{env}/secrets/public-key` and
`GET /orgs/{org}/{app}/secrets/public-key`; the create call sends `encrypted_value` and `key_id`
(organisation secrets also `visibility` and `selected_repository_ids`).
GitHub's documented Python example (PyNaCl):
```python
from base64 import b64encode
from nacl import encoding, public
def encrypt(public_key: str, secret_value: str) -> str:
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")
```
GitHub also documents Node.js (libsodium-wrappers, `crypto_box_seal`) and C# examples.

## 3. Gotchas
- Keys differ per repository, environment, organisation and application, so fetch the key from the endpoint that
  matches the secret you create.
- `gh secret set` reads the value from stdin when `--body` is omitted; prefer stdin or `-f` over `--body`, which can
  end up in shell history. `--no-store` prints the encrypted, Base64 value instead of storing it.
- Check the REST documentation for the token permission an endpoint needs.

## Verify
- [ ] `gh secret list` shows a fresh `updatedAt` on every target.
- [ ] A canary workflow using the secret succeeds after rotation.

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23 and cli/cli source (gh v2.103.2).
- gh secret set/list/delete flags (--env, --org, --user, --app actions|agents|codespaces|dependabot, --body, stdin, -f dotenv, --no-store, list --json fields name, visibility, updatedAt): confirmed in cli/cli pkg/cmd/secret source (gh v2.103.2).
- libsodium sealed-box requirement, public-key retrieval via the endpoint named in the encrypted_value docs, and the PyNaCl, Node.js and C# examples: confirmed in the encrypting-secrets-for-the-rest-api guide; endpoint paths for public keys and the encrypted_value, key_id, visibility and selected_repository_ids body fields: confirmed in the gh source.
- Removed unconfirmed claims: 422 behaviour on wrong keys and the token scope requirements.

Method: documentation only; no commands were run.
