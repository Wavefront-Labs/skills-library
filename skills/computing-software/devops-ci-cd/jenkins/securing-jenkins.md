---
id: computing-software.devops-ci-cd.jenkins.securing-jenkins
name: securing-jenkins
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jenkins-security, jenkins-hardening, authorization-strategy, matrix-authorization, project-based-matrix, role-strategy, role-based-authorization, security-realm, ldap, saml, oidc-login, csrf-crumb, crumb-issuer, agent-to-controller-security, controller-isolation, script-security, groovy-sandbox, in-process-script-approval, markup-formatter, content-security-policy, api-tokens, reverse-proxy-tls, audit-trail-plugin, security-advisories, cve-monitoring, credentials-masking, build-authorization]
level: advanced
status: docs-checked
description: "Harden a Jenkins controller: IdP security realm, matrix or role-strategy authorisation, zero controller executors, agent-to-controller control, CSRF/CSP, script approval."
sources: ["https://www.jenkins.io/doc/book/security/", "https://www.jenkins.io/doc/book/security/controller-isolation/", "https://www.jenkins.io/doc/book/security/access-control/", "https://www.jenkins.io/doc/book/managing/script-approval/", "https://www.jenkins.io/security/advisories/", "https://plugins.jenkins.io/role-strategy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Securing Jenkins

**Goal:** a controller where a compromised job, agent or plugin cannot become
"admin of everything that deploys". Jenkins is a remote-code-execution service by design;
security is about *who* can define code and *where* it runs.

## 1. Authentication (security realm)
Manage Jenkins -> Security -> Security Realm: prefer your corporate identity provider (LDAP,
SAML or OpenID Connect plugins) over the built-in user database, and make sure group
information reaches Jenkins so authorisation can use groups. Disable self sign-up. Keep a
break-glass admin account whose credential is in a vault. Check the chosen plugin's page for its
JCasC keys.

## 2. Authorisation
- **Matrix Authorization Strategy**: global and project-based matrices; give Anonymous nothing
  and authenticated users only what they need.
- **Role-based Strategy** (`role-strategy`): global roles (Overall, Agent, Job, Run, View, SCM
  permissions), item roles for jobs, pipelines and folders, and agent roles, assigned to users
  and groups.
- Treat `Overall/Administer`, script console access, plugin management, agent configuration and
  credential update as admin-equivalent. Prefer multibranch jobs whose pipeline code lives in
  SCM and goes through review.
- **Build authorization** (`authorize-project` plugin): run builds as a chosen user instead of
  SYSTEM. Scope credentials to folders so one team's jobs cannot see another's secrets.

## 3. Controller isolation
Do not build on the built-in node: builds there have the same file-system access as the Jenkins
process. Manage Jenkins -> Nodes -> Built-In Node -> Configure, set executors to 0, and provide
agents or clouds instead (the Job Restrictions plugin can also restrict which jobs run where).

## 4. Agent -> controller access control
This system is always enabled since Jenkins 2.326 and prevents a compromised agent from sending
malicious commands to the controller. The docs strongly recommend never disabling it.

## 5. Script security
- Pipeline Groovy runs in the sandbox; unsafe signatures need approval in *In-process Script
  Approval*. Do not bulk-approve; move privileged calls into a reviewed trusted shared library
  (trusted libraries run outside the sandbox, so guard their repository).
- Untrusted contributors (forks) must not be able to change what runs with elevated
  privileges; set the trust policy on the branch source accordingly.
- Restrict the script console to administrators.

## 6. Web hardening
- Keep CSRF protection on (crumb issuer). API clients can send the crumb or use API tokens.
- Use a safe markup formatter, not raw HTML, and leave Jenkins' Content Security Policy at its
  restrictive default.
- Terminate TLS at a reverse proxy and keep the Jenkins URL and forwarding headers correct.

## 7. Credentials hygiene
Scope credentials to folders and avoid System scope for job use. Prefer short-lived credentials
from a secrets manager. `withCredentials` masks the secret in logs, but Groovy string
interpolation of a secret into an `sh` script can leak it; use single-quoted scripts and let the
shell expand the variable.

## 8. Patch and audit
Follow the Jenkins security advisories (www.jenkins.io/security/advisories), update core and
plugins on a regular window, test on a staging controller, and send audit events to your SIEM.

## Verify
- [ ] Anonymous user sees the login page only; non-admins cannot open the script console or management pages.
- [ ] Built-in node has 0 executors; no job label targets it.
- [ ] A job in folder A cannot use a credential scoped to folder B.
- [ ] Script approval queue is empty of blanket approvals; untrusted PR builds run without libraries.
- [ ] Security advisory banner is clean after the last update window.

## Checked
2026-11-02. Confirmed against the Jenkins controller-isolation, CSRF protection and access-control handbook pages and the Role Strategy plugin page: built-in node executors set to 0 and why, Agent to Controller Access Control always enabled since 2.326, role-strategy global/item/agent roles, crumb-based CSRF protection. Removed: JCasC OIDC snippet and plugin ids other than role-strategy and authorize-project, regex example roles, permission-equivalence list details, secrets file names, API-token and proxy flags, CLI and header claims.
Method: documentation only; no commands were run.
