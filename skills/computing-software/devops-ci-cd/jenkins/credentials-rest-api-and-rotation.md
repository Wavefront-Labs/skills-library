---
id: computing-software.devops-ci-cd.jenkins.credentials-rest-api-and-rotation
name: credentials-rest-api-and-rotation
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, credentials, credentials-api, credentials-rest-api, credential-rotation, config-xml, jenkins-cli, api-token, crumb, credentials-usage-tracking, fingerprints, secret-rotation]
level: advanced
status: docs-checked
description: "Create, update and rotate Jenkins credentials by API: REST config.xml endpoints, jenkins-cli credential commands, usage tracking to find consumers, and zero-downtime rotation."
sources: ["https://github.com/jenkinsci/credentials-plugin/blob/master/docs/user.adoc", "https://www.jenkins.io/doc/book/security/csrf-protection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credentials API and rotation

## REST endpoints (Credentials plugin)
Base for the global store:
`$JENKINS/credentials/store/system/domain/_/` ; for a folder:
`$JENKINS/job/<folder>/credentials/store/folder/domain/_/`.

```bash
AUTH="admin:$JENKINS_API_TOKEN"          # API-token requests are exempt from CSRF protection
# create
curl -sf -u "$AUTH" -H 'Content-Type: application/xml' \
  -X POST "$JENKINS/credentials/store/system/domain/_/createCredentials" --data-binary @- <<'XML'
<org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl>
  <scope>GLOBAL</scope><id>sonar-token</id><description>Sonar</description>
  <secret>NEW_VALUE</secret>
</org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl>
XML
# read (the secret comes back as <secret-redacted/>)
curl -sf -u "$AUTH" "$JENKINS/credentials/store/system/domain/_/credential/sonar-token/config.xml"
# update in place (keeps the ID, so jobs keep working)
curl -sf -u "$AUTH" -H 'Content-Type: application/xml' -X POST \
  "$JENKINS/credentials/store/system/domain/_/credential/sonar-token/config.xml" --data-binary @new.xml
# delete
curl -sf -u "$AUTH" -X DELETE "$JENKINS/credentials/store/system/domain/_/credential/sonar-token/config.xml"
```
Class names: `UsernamePasswordCredentialsImpl` (com.cloudbees.plugins.credentials.impl),
`BasicSSHUserPrivateKey` (com.cloudbees.jenkins.plugins.sshcredentials.impl). Read an existing
one's `config.xml` to copy the exact shape. The secret is sent in the clear so Jenkins can
encrypt it before storing it.

## CLI
```bash
java -jar jenkins-cli.jar -s "$JENKINS" -auth @creds list-credentials system::system::jenkins
java -jar jenkins-cli.jar -s "$JENKINS" -auth @creds update-credentials-by-xml \
  system::system::jenkins _ sonar-token < new.xml
```
(`create-credentials-by-xml`, `get-credentials-as-xml`, `delete-credentials` and `delete-credentials-domain` exist too; the folder store id form is `folder::item::/example-folder`.)

## Rotation procedure
1. **Find consumers**: the credential details page shows usage tracking, which depends on the
   consuming plugins cooperating and is not definitive. Also search Jenkinsfiles and JCasC for
   the ID.
2. Issue the new secret at the provider while the old still works (dual-validity window).
3. Update the Jenkins credential **in place** (same ID).
4. Trigger a canary job that uses it; then revoke the old secret at the provider.
5. If JCasC manages the credential, rotate at the secret source and reload JCasC
   instead; API edits would be reverted on next reload.

## Gotchas
- Requests that authenticate with a password or session need a crumb (`/crumbIssuer/api/json`);
  API-token requests are exempt.
- Secrets sent in XML land in your shell history/CI logs if you inline them; use files or
  stdin.
- External credentials stores are typically read-only (the Credentials plugin docs); rotate in
  the provider.

## Verify
`get-credentials-as-xml` shows the new `<description>`/username, the canary build
succeeds, and calls with the old secret now fail at the provider.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the Credentials plugin user guide: `createCredentials` and per-credential `config.xml` URLs (GET, POST, DELETE), the `_` global domain, `<secret-redacted/>` on read, store ids (`system::system::jenkins`, `folder::item::/path`), CLI commands `create-credentials-by-xml`, `update-credentials-by-xml`, `delete-credentials`, usage-tracking caveat, API-token CSRF exemption. Fixed the delete example (HTTP DELETE on `config.xml`, not POST to `doDelete`) and removed the unconfirmed `FileCredentialsImpl` note.
Method: documentation only; no commands were run.
