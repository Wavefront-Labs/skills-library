---
id: computing-software.data-engineering.apache-kafka.managed-kafka-iam-auth
name: managed-kafka-iam-auth
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-security, msk-iam, aws-msk, confluent-cloud, api-keys, service-accounts, rbac, iam-policy, managed-kafka]
level: advanced
status: docs-checked
description: "Authenticate to managed Kafka: Amazon MSK IAM auth (client library, IAM policy actions per topic/group) and Confluent Cloud service accounts with API keys and RBAC role bindings."
sources:
  - https://docs.aws.amazon.com/msk/latest/developerguide/iam-access-control.html
  - https://github.com/aws/aws-msk-iam-auth
  - https://docs.confluent.io/cloud/current/security/authenticate/workload-identities/service-accounts/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM and API-key auth for managed Kafka

**Goal:** connect workloads to Amazon MSK or Confluent Cloud with per-service identities and least-privilege permissions, without static passwords where possible.

## Amazon MSK with IAM
Client (Java) adds `software.amazon.msk:aws-msk-iam-auth`:
```properties
bootstrap.servers=b-1.<cluster>.kafka.<region>.amazonaws.com:9098
security.protocol=SASL_SSL
sasl.mechanism=AWS_MSK_IAM
sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;
sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler
```
Credentials come from the default AWS chain (IRSA/EKS Pod Identity, instance role). Python: `aws-msk-iam-sasl-signer-python` with confluent-kafka's `oauth_cb` (`sasl.mechanism=OAUTHBEARER`).

IAM policy (scoped to cluster/topic/group ARNs):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": ["kafka-cluster:Connect", "kafka-cluster:DescribeCluster"],
     "Resource": "arn:aws:kafka:<region>:<acct>:cluster/<name>/<uuid>"},
    {"Effect": "Allow", "Action": ["kafka-cluster:DescribeTopic", "kafka-cluster:ReadData"],
     "Resource": "arn:aws:kafka:<region>:<acct>:topic/<name>/<uuid>/orders.*"},
    {"Effect": "Allow", "Action": ["kafka-cluster:AlterGroup", "kafka-cluster:DescribeGroup"],
     "Resource": "arn:aws:kafka:<region>:<acct>:group/<name>/<uuid>/billing-*"}
  ]
}
```
Producers need `kafka-cluster:WriteData` (+ `WriteDataIdempotently` on the cluster for idempotent producers). IAM port is 9098 (public access 9198). IAM auth and Kafka ACLs are separate systems: IAM clients are authorised by IAM policy only.

## Confluent Cloud
- Create a **service account** per workload; create an **API key** owned by it scoped to the cluster.
```bash
confluent iam service-account create billing-svc --description "billing consumer"
confluent api-key create --resource <lkc-id> --service-account <sa-id>
confluent iam rbac role-binding create --principal User:<sa-id> --role DeveloperRead \
  --resource Topic:orders. --prefix --kafka-cluster <lkc-id> --environment <env-id>
confluent iam rbac role-binding create --principal User:<sa-id> --role DeveloperRead \
  --resource Group:billing- --prefix --kafka-cluster <lkc-id> --environment <env-id>
```
Client: `SASL_SSL`, `PLAIN`, username = API key, password = API secret.
- Rotate keys by creating a second key, deploying it, then deleting the old one.

## Gotchas
- MSK: Kafka ACLs have no effect on IAM identities, and `allow.everyone.if.no.acl.found` is ignored; use IAM policies only.
- Confluent Cloud: ACLs and role bindings attach to the service account; check both when access is denied.

## Checked
2026-10-28. Confirmed: IAM actions (`Connect`, `DescribeCluster`, `DescribeTopic`, `ReadData`, `WriteData`, `WriteDataIdempotently`, `AlterGroup`, `DescribeGroup`), ports 9098 and 9198 (public access), ACLs having no effect on IAM identities (Amazon MSK developer guide); `software.amazon.msk:aws-msk-iam-auth`, `IAMLoginModule`, `IAMClientCallbackHandler`, `AWS_MSK_IAM` (aws-msk-iam-auth README); the Python signer library (aws-msk-iam-sasl-signer-python README); Confluent CLI `service-account create`, `api-key create`, `iam rbac role-binding create` flags (CLI reference); `PLAIN` with API key for Confluent Cloud clients (Confluent Python client docs). Removed: clock-skew, Describe-action, propagation delay and OIDC identity pool claims.
Method: documentation only; no commands were run.

## Verify
- [ ] Workload connects using its role/service account only; no shared admin credentials in app config.
- [ ] Access to an unlisted topic is denied.
- [ ] Key/role rotation tested without downtime.
