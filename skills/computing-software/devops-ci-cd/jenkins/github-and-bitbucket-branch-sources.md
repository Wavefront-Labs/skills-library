---
id: computing-software.devops-ci-cd.jenkins.github-and-bitbucket-branch-sources
name: github-and-bitbucket-branch-sources
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, multibranch-pipeline, github-branch-source, bitbucket-branch-source, github-app-credentials, organization-folder, branch-source-plugin, webhooks, api-rate-limit, scm-api, checks-api, bitbucket-server, bitbucket-cloud]
level: practitioner
status: docs-checked
description: "Connect Jenkins multibranch and organization folders to GitHub or Bitbucket with GitHub App credentials and webhooks."
sources: ["https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/github-app-auth", "https://plugins.jenkins.io/github-branch-source/", "https://plugins.jenkins.io/cloudbees-bitbucket-branch-source/", "https://www.jenkins.io/doc/book/pipeline/multibranch/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub and Bitbucket branch sources

A branch source turns one repo (multibranch) or a whole org (organization folder) into
auto-created jobs per branch, PR and tag. Prefer the platform-specific source (GitHub or Bitbucket) over the generic *Git* source.

## GitHub (plugin: github-branch-source)
1. **Authenticate as a GitHub App, not a user token.** The CloudBees guide gives the reasons: a GitHub App's rate limit scales with organisation size, whereas a user token is limited to 5000 requests. Create the App with the repository permissions listed in that guide and install it on the org. Jenkins needs the private key converted to PKCS#8:
   `openssl pkcs8 -topk8 -inform PEM -outform PEM -in app.pem -out app-pkcs8.pem -nocrypt`.
   Add a credential of kind *GitHub App* (App ID plus the converted key).
2. New item -> *Organization Folder* (or *Multibranch Pipeline*) -> *GitHub* source,
   API endpoint (set it explicitly for GitHub Enterprise), owner, credential.
3. Webhook: set the App's webhook URL to `https://jenkins.example.com/github-webhook/`.

## Bitbucket (plugin: cloudbees-bitbucket-branch-source)
See the plugin page on plugins.jenkins.io for Bitbucket Cloud versus Server / Data Center setup, endpoints and webhook configuration.

## Failure modes
- Branches never build until a manual *Scan*: the webhook is not reaching Jenkins (check the delivery log on the GitHub side).
- A GitHub App private key that has not been converted to PKCS#8 will not work in Jenkins (see the openssl conversion above).

## Verify
*Scan Organization/Repository Now* log lists discovered branches/PRs with no 401/403;
push a commit and confirm a build starts and a commit status appears.

## Checked
2026-10-28. Confirmed on the CloudBees GitHub App guide: a GitHub App's rate limit scales with organisation size while a user token is limited to 5000 requests; the `openssl pkcs8 -topk8 ... -nocrypt` key conversion; webhook URL form `https://<jenkins-host>/github-webhook/`; GitHub Enterprise needs the API URL set.
Removed (not confirmed): the exact App permission list, GHE `/api/v3` path, the "Manage hooks" and rate-limit strategy options, the Job DSL snippet, all Bitbucket endpoint, token and webhook specifics (`bitbucket-scmsource-hook/notify`), and the failure-mode messages and rate limiter text.

Method: documentation only; no commands were run.
