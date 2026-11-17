---
id: computing-software.devops-ci-cd.jenkins.jcasc-secret-sources-and-credentials
name: jcasc-secret-sources-and-credentials
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jcasc, configuration-as-code, jcasc-credentials, jcasc-secret-source, secrets-directory, kubernetes-secrets, vault, aws-secrets-manager, variable-interpolation, base64-secret-file, credentials-as-code, escaping-dollar]
level: advanced
status: docs-checked
description: "Declare Jenkins credentials in JCasC without committing secrets: ${VAR} secret sources (env, mounted files, Vault, AWS), file/base64 helpers, escaping and rotation by reload."
sources: ["https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/secrets.adoc", "https://github.com/jenkinsci/configuration-as-code-plugin/tree/master/demos/credentials", "https://plugins.jenkins.io/configuration-as-code/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JCasC secret sources and credentials

JCasC YAML lives in git; secrets must not. Reference them as `${NAME}` and let a
**secret source** resolve them at load time.

## Credentials block
```yaml
credentials:
  system:
    domainCredentials:
      - credentials:
          - string:
              scope: GLOBAL
              id: "slack-token"
              secret: "${SLACK_TOKEN}"
          - usernamePassword:
              scope: GLOBAL
              id: "registry"
              username: "ci-bot"
              password: "${REGISTRY_PASSWORD}"
          - basicSSHUserPrivateKey:
              scope: SYSTEM
              id: "agent-ssh"
              username: "jenkins"
              privateKeySource:
                directEntry:
                  privateKey: "${readFile:/run/secrets/agent_ssh_key}"
          - file:
              scope: GLOBAL
              id: "gcp-sa"
              fileName: "sa.json"
              secretBytes: "${base64:${readFile:/run/secrets/gcp_sa.json}}"
```

## Secret sources
The SecretSource extension point resolves `${KEY}`; sources listed in the docs: AWS Secrets Manager, AWS Systems
Manager Parameter Store, Azure KeyVault, Docker secrets, environment variables, HashiCorp Vault, Kubernetes secrets.
1. **Files** (Docker/Kubernetes secrets): a file `/run/secrets/<KEY>` becomes `${KEY}`; override the base folder
   with env `SECRETS`. Mount a Kubernetes Secret as a file under `/run/secrets/`. A `.properties` file at
   `/run/secrets/secrets.properties` is also read (`SECRETS_FILE` changes the path).
2. **Environment variables**: supported but not recommended for secrets, since admins and jobs on the controller can read them.
3. **HashiCorp Vault** (Vault plugin 2.4.0+): requires `CASC_VAULT_URL` and `CASC_VAULT_PATHS` plus auth via
   `CASC_VAULT_USER`/`CASC_VAULT_PW`, `CASC_VAULT_TOKEN`, or `CASC_VAULT_APPROLE`/`CASC_VAULT_APPROLE_SECRET`.
   `CASC_VAULT_ENGINE_VERSION` defaults to kv v2; set `1` for v1. `CASC_VAULT_FILE` loads these from a properties file.
4. **Credential provider plugins** (Kubernetes Credentials Provider, AWS Secrets Manager Credentials Provider, Azure
   KeyVault) supply credentials by ID, so you need not define them in JCasC. Fields backed by `hudson.util.Secret`
   (for example proxy and SMTP passwords) cannot take a credential ID.

Helpers: `${readFile:path}` (alias `${file:path}`), `${base64:...}`, `${decodeBase64:...}`, `${readFileBase64:path}`
(alias `${fileBase64:path}`), `${json:key:${...}}`, `${trim:...}` (removes trailing whitespace; `readFile` keeps it),
`${NAME:-default}`. Helpers nest.

## Escaping
A literal `${...}` (e.g. a Groovy snippet in a Job DSL script inside JCasC) must be
written `^${...}`; JCasC removes the leading `^`. The escape applies to all JCasC values, not only secrets.

## Rotation
Update the secret at the source (K8s Secret, Vault), then reload JCasC (see
`computing-software.devops-ci-cd.jenkins.reloading-jcasc-configuration`). Environment variables are fixed at
process start, so changing them needs a restart.

## Gotchas
- By default an unresolved variable becomes an empty string plus a log warning, so a typo or a remote secrets
  outage can overwrite credentials with empty values on reload. Set `CASC_STRICT_SECRET_RESOLUTION=true`
  (or `-Dcasc.strict.secret.resolution=true`) so a reload with an unresolved secret that has no `:-` default
  aborts and keeps the previous configuration.
- Encrypted values (`{AQAAAB...}`) use the instance's own secret key and are not portable between Jenkins instances.
- `secretBytes` for file credentials needs base64 content (`${readFileBase64:path}` or `${base64:${readFile:path}}`).

## Verify
Restart/reload, then *Manage Jenkins -> Credentials* shows the IDs; a test job using each
binding succeeds; the JCasC log has no unresolved-variable warnings.

## Checked
2026-10-31. Confirmed against the JCasC "Handling Secrets" page, the credentials demo and the plugin page: secret sources, file location and `SECRETS`, Vault variables and engine default, helper list, `^` escaping, strict resolution, `secretBytes`. Removed: resolution-order claim, Helm chart value names, `configuration-as-code-secret-ssm`, kubelet sync timing, error-message strings, overwrite-on-reload and View Configuration claims.
Method: documentation only; no commands were run.
