---
id: computing-software.cybersecurity-defensive.application-security.leaked-secret-response
name: leaked-secret-response
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [secrets-scanning, leaked-secret-response, credential-rotation, git-history-rewrite, secret-revocation, incident-response]
level: advanced
status: docs-checked
description: "Respond to a leaked secret: assess risk, revoke with the provider, update services, check for unauthorised use, clean history and prevent recurrence."
sources: ["https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/remediating-a-leaked-secret"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leaked secret response

Treat any leaked secret as immediately compromised. Removing it from the code, pushing a new commit, or deleting and
recreating the repository does not stop it being exploited; revoking it does.

## Steps (GitHub remediation guide)
1. **Identify and gather context**: secret type and provider; repository, file and line; the owner (check
   `CODEOWNERS`; `git log -S` finds who committed it). A secret scanning alert gives most of this.
2. **Assess risk**: with scanning on, check the validity status (active, inactive or unknown; the provider is the most
   reliable source), the `public exposure` and `multiple leaks` labels and, for GitHub PATs, last use and scope. Without
   it: repository visibility, signs of recent use, how sensitive the file is (production script or admin key versus
   test file) and which services depend on the secret.
3. **Choose urgency**: automated scanners find public secrets in minutes and they can be exploited within hours. High
   risk (active, public, or a production credential) means revoke immediately and tell the owner, repository
   administrators and security leads. If downtime is a concern, first create a replacement with the same permissions,
   switch the application, then revoke the old one. Medium or low risk (inactive, private repository, test credential)
   can be planned with the owning team, but should still be remediated.
4. **Revoke** with the secret's provider (not just in the code), and generate a replacement if needed. GitHub
   automatically revokes GitHub PATs leaked in public repositories; for PATs in private repositories use Report leak on
   the alert; for supported partner patterns leaked publicly GitHub reports to the provider, who may revoke.
5. **Update affected services**: search code, issues and PRs (`org:YOUR-ORG "SECRET"` or `repo:YOUR-REPO "SECRET"`),
   check deploy keys, repository secrets and variables, and installed apps; update and test each service.
6. **Check for unauthorised access** while the secret was exposed: GitHub audit logs (including access-token events)
   and the provider's logs, for example AWS CloudTrail.
7. **Clean the repository**: the secret remains in commit history. Cleaning is destructive and may need force pushes,
   so weigh it with security leads against compliance obligations.
8. **Resolve the alert** as "Revoked" and document the incident, the steps taken and lessons learned.
9. **Prevent recurrence**: enable push protection (and personal push protection) with strict bypass controls, keep
   secrets in environment variables or a secrets store rather than code, rotate regularly, and train the team.

## Verify
The old credential fails authentication, logs for the whole exposure window were reviewed and recorded, and push
protection is on.

## Checked
Method: docs-checked 2026-11-09 against the GitHub "Remediating a leaked secret" tutorial (read in full). Removed
unconfirmed claims and sources not read: the AWS Security Incident Response Guide and OWASP Secrets Management Cheat
Sheet, the `aws iam` and CloudTrail commands, `git filter-repo` and BFG usage, GitHub Support purge advice, and
signing-key and shared-credential guidance.
