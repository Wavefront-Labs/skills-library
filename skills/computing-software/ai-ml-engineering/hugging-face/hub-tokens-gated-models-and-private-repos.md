---
id: computing-software.ai-ml-engineering.hugging-face.hub-tokens-gated-models-and-private-repos
name: hub-tokens-gated-models-and-private-repos
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, gated-models, hf-token, private-repos, fine-grained-tokens, access-control]
level: practitioner
status: gated
description: "Access gated and private Hugging Face repos: request access, fine-grained vs read/write tokens, HF_TOKEN in CI and containers, org permissions, and common 401/403 errors."
sources:
  - https://huggingface.co/docs/hub/security-tokens
  - https://huggingface.co/docs/hub/models-gated
  - https://huggingface.co/docs/huggingface_hub/quick-start#authentication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tokens, gated models and private repos

## Gated models (Llama, Gemma, some Mistral releases)
1. Log in on the website, open the model page, accept the licence / fill the form. Approval may be instant or manual.
2. Use a token from the same account. Access is per user (or per org if requested through the org); a teammate's approval doesn't cover you.
3. Errors: `401 Unauthorized` = no/invalid token (checked: `hf_hub_download` on a gated repo without a token raises `GatedRepoError` with a 401); `403 Forbidden` = token valid but access not granted, or a fine-grained token lacking the gated-repo permission (gated: unconfirmed, source is paywalled or blocked). Reproducing the 403 needs a logged-in account that has not been granted access, which was not available.

## Tokens
- **Fine-grained** (recommended): scope to specific repos/orgs and permissions (read, write, "read access to public gated repos you can access", inference). Create per application.
- **Read**: read everything you can access. **Write**: push too. Avoid write tokens on servers that only download.
- Set once: `hf auth login` (older `huggingface-cli login`) stores the token in `$HF_HOME/token` (default `~/.cache/huggingface/token`; checked via `huggingface_hub.constants.HF_TOKEN_PATH`). In code: `login(token=...)` or pass `token=` to `from_pretrained`/`hf_hub_download`.
- Env var `HF_TOKEN` overrides the stored token (documented in the huggingface_hub environment-variable reference); use it in CI and containers (from the secret store, never committed or baked into images).

## Private repos and orgs
```python
from huggingface_hub import create_repo, HfApi
create_repo("org/internal-model", private=True, repo_type="model")
HfApi().upload_folder(repo_id="org/internal-model", folder_path="out/", commit_message="v1.2")
```
Org roles (per the Hub docs): `no_access`, `read`, `contributor` (write only to repos the user created), `write`, `admin`. Resource groups restrict repos to teams and are part of the Team & Enterprise plans per the docs. Org-level SSO and token policies are plan-dependent (gated: unconfirmed, source is paywalled or blocked); check the organization settings page for your plan.

## Hosting your own gated model
In the model card YAML:
```yaml
extra_gated_prompt: "You agree to use this model only for research."
extra_gated_fields: {Company: text, Country: country, "I agree to the terms": checkbox}
```
Then enable gating (automatic or manual approval, per the Hub docs on gated models) in repo settings; manage requests via the UI or `HfApi().list_pending_access_requests()` (the method exists in huggingface_hub 2.2.0; calling it needs a repo you own, which was not tested). The documented extra field types include `text`, `checkbox` and `country`.

## Security practice
- Rotate tokens on staff changes; revoke leaked ones immediately (automatic revocation of leaked tokens by the Hub or GitHub is not described in the Hub token docs: gated: unconfirmed, source is paywalled or blocked).
- One token per service, so revocation is targeted.
- Don't log request headers or print tokens in notebooks that get shared.

## Verify
`hf auth whoami` (older `huggingface-cli whoami`; without a login it prints `Not logged in`) shows the expected account/orgs; `HfApi().model_info("meta-llama/...", token=...)` succeeds; a download in CI works with only `HF_TOKEN` set.
