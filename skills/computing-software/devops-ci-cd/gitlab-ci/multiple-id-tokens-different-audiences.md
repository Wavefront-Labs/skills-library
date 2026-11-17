---
id: computing-software.devops-ci-cd.gitlab-ci.multiple-id-tokens-different-audiences
name: multiple-id-tokens-different-audiences
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, multiple-id-tokens, id-tokens, gitlab-oidc]
level: practitioner
status: docs-checked
description: "Define several GitLab id_tokens in one job, each with its own aud, to authenticate to Vault, AWS and Sigstore separately without reusing a token across trust domains."
sources: ["https://docs.gitlab.com/ci/yaml/#id_tokens", "https://docs.gitlab.com/ci/secrets/id_token_authentication/", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple id_tokens with different audiences

```yaml
deploy:
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
    ID_TOKEN_2:
      aud:
        - https://gcp.example.com
        - https://aws.example.com
    SIGSTORE_ID_TOKEN:
      aud: sigstore
  script:
    - command_to_authenticate_with_vault $VAULT_ID_TOKEN
    - command_to_authenticate_with_cloud $ID_TOKEN_2
```

## Why separate tokens
- Third-party services can be configured to reject tokens whose `aud` does not match their bound audience. Giving each service its own token reduces the number of services a token can authenticate with, and so the damage if one is compromised.
- `aud` can be an array, but a token with several audiences is accepted by each of them; prefer one audience per consumer.

## Details
- `aud` is required and supports a single string, an array of strings, or CI/CD variables (for example `aud: $VAULT_ADDR`).
- `id_tokens` set on a job replaces `default:id_tokens`; the two are not merged.
- The token expires at the job timeout if one is set, otherwise after 5 minutes.
- Use the claims (`project_path`, `ref`, `ref_protected`, `environment`, `pipeline_source`) in each relying party's conditions.

## Verify
- [ ] Decode each token in a throwaway job (`cut -d '.' -f2 | base64 -d`) and confirm the `aud` claims differ. Never print real tokens in shared logs.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md and doc/ci/secrets/id_token_authentication.md: several named tokens per job each with their own `aud`, `aud` as string, array or CI/CD variable, job-level `id_tokens` taking precedence over `default:id_tokens` with no merge, the docs' rationale (services reject tokens whose `aud` does not match, which limits the damage of a leaked token), token expiry (job timeout if set, otherwise 5 minutes), and the Sigstore `aud: sigstore` example. Removed the Vault, AWS and cosign commands, the masking claim, the two-hour lifetime and the replay scenario, which the GitLab pages do not state.

Method: documentation only; no commands were run.
