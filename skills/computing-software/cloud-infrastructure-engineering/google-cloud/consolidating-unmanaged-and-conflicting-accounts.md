---
id: computing-software.cloud-infrastructure-engineering.google-cloud.consolidating-unmanaged-and-conflicting-accounts
name: consolidating-unmanaged-and-conflicting-accounts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-identity, unmanaged-accounts, conflicting-accounts, transfer-tool, account-migration]
level: practitioner
status: docs-checked
description: "Find consumer Google accounts using your corporate domain, migrate them into Cloud Identity with the transfer tool, and avoid conflicting accounts during federation."
sources: ["https://cloud.google.com/architecture/identity/assessing-existing-user-accounts", "https://cloud.google.com/architecture/identity/migrating-consumer-accounts", "https://support.google.com/a/answer/6178640"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consolidating unmanaged and conflicting accounts

Before an organization existed, staff often created **consumer** Google accounts with their work
email (`alice@example.com`). Once you add and verify the domain in Cloud Identity or Workspace, such
accounts become **unmanaged**: the user notices nothing, but you do not control them.

## Find them
Verifying a domain starts a search for consumer accounts using it; they surface in the Admin console
**transfer tool for unmanaged users** within about 12 hours. You need a Super Admin role to use it.
Cross-check IAM:
```bash
gcloud asset search-all-iam-policies --scope=organizations/<ORG> \
  --query="policy:example.com" --format="value(resource,policy.bindings.members)"
```

## Migrate (preferred)
1. Send an account transfer request from the tool (accounts start as "Not yet invited"); the user
   consents and the account becomes managed.
2. Do this before creating the same user via a federation connector or manually. If the user does not
   consent and you create the account anyway, the result is a **conflicting account**: one consumer and
   one managed account on the same identity. Only the consumer account keeps the original data; the
   managed account is effectively new.
3. A user may rename the address to an unverified domain, which turns it back into a consumer account
   that can no longer be transferred.

## Evict instead
Creating a conflicting account is a deliberate way to evict an unwanted consumer account. At sign-in the
user gets a choice between the managed and consumer account; choosing the consumer one prompts a rename,
and "Do this later" puts the account in an Evicted state with a temporary `gtempaccount.com` address until renamed.

## Gotchas
- SSO or provisioning from an external IdP can create conflicting accounts unintentionally.
- Gmail addresses (`@gmail.com`) have no affiliation with your domain, so they cannot be found
  systematically; only reviewing access control policies reveals them.

## Verify
- [ ] Transfer tool list is empty or every entry has a decision.
- [ ] No IAM bindings reference `gtempaccount.com` identities.

## Checked
2026-10-28. Confirmed on "Assessing existing user accounts" and "Migrating consumer accounts": unmanaged accounts
after verification, 12-hour discovery, Super Admin requirement, transfer request states, conflicting-account
behaviour, eviction and `gtempaccount.com`, Gmail limitation, IdP-caused conflicts. gcloud command passed
check_commands. Removed (not on the pages): Drive/projects/IAM preserved on transfer, OU and 2SV advice, Domain
Restricted Sharing, Policy Analyzer and billing-ownership claims, and the exact rename format of the temporary address.
Method: documentation only; no commands were run.
