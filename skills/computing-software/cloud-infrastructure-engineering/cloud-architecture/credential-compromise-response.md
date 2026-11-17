---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.credential-compromise-response
name: credential-compromise-response
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, detection-and-response, credential-compromise-response, leaked-access-key, exposed-secret, key-rotation, cloud-incident-response]
level: practitioner
status: draft
description: "Respond to a leaked cloud credential: contain (disable/revoke), scope via audit logs, eradicate persistence, rotate, recover and prevent recurrence."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html", "https://learn.microsoft.com/security/operations/incident-response-playbook-compromised-malicious-app", "https://cloud.google.com/iam/docs/keys-disable-enable"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Leaked credential response

## Contain (minutes)
1. **Disable, don't delete** (keeps evidence): AWS `aws iam update-access-key --status Inactive`;
   GCP disable the service account key; Entra: remove client secret / disable app, revoke user
   sessions (`Revoke-MgUserSignInSession`).
2. Revoke active sessions: AWS attach an inline deny policy with `aws:TokenIssueTime` condition
   (console "Revoke active sessions") for roles the key could assume.
3. If provider quarantined the key (AWS applies `AWSCompromisedKeyQuarantine` policy on detected
   public exposure), still treat as compromised.

## Scope
- Query audit logs (CloudTrail Lake/Athena, Activity Log, Cloud Audit Logs) for the key/principal
  from the earliest possible exposure time: source IPs, regions, actions.
- Look for persistence: new IAM users/keys/roles, trust policy changes, new federated apps, Lambda
  functions, instances (cryptomining), snapshots shared externally, disabled logging.

## Eradicate and recover
Remove persistence, rotate any other secrets the principal could read (Secrets Manager/Key Vault),
terminate attacker resources, restore changed configs from IaC, check billing for abuse.

## Post-incident
Root cause (committed to git? CI logs?), replace static key with workload identity, add secret
scanning (push protection), contact provider for billing adjustments if abused.

## Verify
- [ ] Timeline and scope documented; all persistence removed.
- [ ] Static credential replaced by federation.
