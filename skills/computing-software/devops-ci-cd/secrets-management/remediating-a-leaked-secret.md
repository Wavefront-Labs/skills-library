---
id: computing-software.devops-ci-cd.secrets-management.remediating-a-leaked-secret
name: remediating-a-leaked-secret
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, secret-scanning, secret-remediation, revoke-leaked, leaked-credentials, incident-response, git-filter-repo, bfg, credential-rotation, audit-logs, ci-log-cleanup, cached-views]
level: advanced
status: docs-checked
description: "Respond to a leaked credential: revoke and rotate first, then decide on history rewrite with git-filter-repo, GitHub Support cleanup and log retention."
sources: ["https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository", "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remediating a leaked secret

**Order matters: revoke or rotate first.** GitHub's guidance is explicit: if the sensitive data is a secret, the first step is to revoke or rotate it. Once revoked it can no longer be used for access, which may be sufficient, and rewriting history may not be warranted.

## 1. Contain (OWASP Secrets Management Cheat Sheet, incident response)
- **Revocation**: exposed keys get immediate revocation; the secret must be quickly de-authorisable and the revocation status identifiable.
- **Rotation**: a new secret must be creatable and deployable quickly, preferably through an automated process (repeatable, fewer errors, least privilege).
- **Deletion**: remove revoked or rotated secrets from the exposed system immediately, including those in code or logs. Squashing history to before the secret's introduction is possible but rewrites git history and breaks links to commits, so plan for the consequences. Secrets in logs need a process that preserves log integrity.
- **Logging**: responders need the lifecycle of the secret: who had access, when they used it, and when it was last rotated. Keep incident logging in one location accessible to the IR team.
- Prepare in advance: documentation of whom to alert, containment steps and what to log.

## 2. Rewrite history only if warranted (GitHub guidance)
Side effects: easy re-contamination if someone pushes an old clone; lost work on branches still carrying the data; changed commit hashes; branch protection must be lifted temporarily; closed pull request diff views break; open PR diffs and comments are invalidated (merge or close open PRs first); commit and tag signatures are lost; and the divergence shows others where the data was.

Procedure with `git-filter-repo` (version 2.47 or later for `--sensitive-data-removal`):
1. Clone the repository.
2. Run `git-filter-repo --sensitive-data-removal --invert-paths --path PATH` to remove a file from all refs (add `--path` for any other path the file used to have), or `--replace-text FILE` to replace listed text in non-binary files.
3. Check how many pull requests are affected (`refs/pull/*/head` entries in `.git/filter-repo/changed-refs`); the rewrite becomes irreversible once you move on.
4. `git push --force --mirror origin`. Pushes of `refs/pull/` refs fail because GitHub marks them read-only; other failures usually mean branch protection.
5. Contact GitHub Support with the repository, number of affected pull requests and the First Changed Commit(s) from git-filter-repo's output (and any orphaned LFS object note). Support dereferences or deletes affected PRs, runs server garbage collection, removes cached views and purges orphaned LFS objects. Support only helps where the risk cannot be mitigated by rotating credentials.
6. Forks keep the commit; ask fork owners to remove the data or delete the fork. Collaborators must re-clone or follow git-filter-repo's cleanup instructions, and must rebase rather than merge branches made from the old history.

## 3. Prevent recurrence (GitHub guidance)
Add untracked files to `.gitignore`; avoid hardcoded secrets and inject from a secret manager at runtime; use a pre-commit hook such as git-secrets or gitleaks; enable push protection.

## Checked
Method: docs-checked 2026-11-09 against the GitHub "Removing sensitive data from a repository" page (full) and the OWASP Secrets Management Cheat Sheet (sections 9.1 to 9.3 incident response read in full; auditing and rotation sections searched).
Removed as unconfirmed: provider-specific revoke commands (AWS CLI, CloudTrail queries), the claim that bots scrape public GitHub within minutes, BFG usage, GitLab job erase API and the GitLab remediation page (404), CI log and artifact deletion steps, npm and PyPI unpublish advice, and the shortened-lifetimes advice.
