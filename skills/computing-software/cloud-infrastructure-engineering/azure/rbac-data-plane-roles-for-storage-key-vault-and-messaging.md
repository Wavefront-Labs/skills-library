---
id: computing-software.cloud-infrastructure-engineering.azure.rbac-data-plane-roles-for-storage-key-vault-and-messaging
name: rbac-data-plane-roles-for-storage-key-vault-and-messaging
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-rbac, data-actions, data-plane-roles, storage-data-roles, storage-blob-data-contributor, storage-queue-data-contributor, key-vault-secrets-user, key-vault-crypto-user, service-bus-data-sender, event-hubs-data-receiver, cosmos-db-data-contributor, app-configuration-data-reader, least-privilege, managed-identity]
level: practitioner
status: draft
description: "Pick the right built-in data-plane RBAC role per service (Storage, Key Vault, Service Bus/Event Hubs, Cosmos DB, App Configuration) and assign at the narrowest scope with Entra-only auth."
sources: ["Microsoft Learn - Azure built-in roles (Storage, Key Vault, Messaging, Databases sections)", "Microsoft Learn - Authorize access to blobs using Microsoft Entra ID", "Microsoft Learn - Provide access to Key Vault keys, certificates, and secrets with Azure RBAC", "Microsoft Learn - Authenticate with Microsoft Entra ID to access Service Bus/Event Hubs", "Microsoft Learn - Configure role-based access control with Microsoft Entra ID for Azure Cosmos DB"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data-plane RBAC roles — Owner on the resource is not access to the data

**Goal:** every app, pipeline and human reaches data with an Entra identity and a role that
contains only the `DataActions` needed, scoped to the container/queue/secret level where the
service allows it; keys and connection strings are disabled or unused.

## 1. The cheat sheet
| Service | Read | Write | Admin / notes |
|---|---|---|---|
| Blob | Storage Blob Data Reader | Storage Blob Data Contributor | Storage Blob Data Owner (POSIX ACLs on ADLS); scope to container `.../blobServices/default/containers/<c>` |
| Queue | Storage Queue Data Reader / Message Processor (peek+delete) | Storage Queue Data Message Sender / Contributor | scope to queue |
| Table | Storage Table Data Reader | Storage Table Data Contributor | — |
| Files (SMB over REST) | Storage File Data SMB Share Reader | … Contributor / Elevated Contributor (NTFS) | Storage File Data Privileged Reader/Contributor for REST |
| Key Vault (RBAC model) | Key Vault Secrets User, Certificate User, Crypto User (sign/encrypt) | Key Vault Secrets/Certificates/Crypto Officer | Key Vault Administrator (all data), Reader (metadata only); scope to a single secret `/secrets/<n>` |
| Service Bus | Azure Service Bus Data Receiver | Data Sender | Data Owner; scope to queue/topic/subscription |
| Event Hubs | Azure Event Hubs Data Receiver | Data Sender | Data Owner; scope to hub or consumer group |
| Cosmos DB (NoSQL) | Cosmos DB Built-in Data Reader (`00000000-0000-0000-0000-000000000001`) | Built-in Data Contributor (`…0002`) | Cosmos has its **own** RBAC API (`az cosmosdb sql role assignment`), not Azure RBAC |
| App Configuration | App Configuration Data Reader | App Configuration Data Owner | — |
| SignalR / Web PubSub | SignalR App Server, SignalR REST API Reader | … Owner | — |
| Managed Grafana | Grafana Viewer | Grafana Editor | Grafana Admin |
| Azure Maps | Azure Maps Data Reader | Data Contributor | — |

## 2. Assign at the narrowest scope
```bash
# blob container scope, managed identity of a Function
az role assignment create --assignee-object-id <MI-PRINCIPAL-ID> --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/<SUB>/resourceGroups/<RG>/providers/Microsoft.Storage/storageAccounts/<SA>/blobServices/default/containers/uploads"
# a single Key Vault secret
az role assignment create --assignee-object-id <MI-PRINCIPAL-ID> --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" --scope "/subscriptions/<SUB>/resourceGroups/<RG>/providers/Microsoft.KeyVault/vaults/<KV>/secrets/db-password"
# Cosmos DB native data RBAC (not az role assignment!)
az cosmosdb sql role assignment create -a <COSMOS> -g <RG> --role-definition-id 00000000-0000-0000-0000-000000000002 \
  --principal-id <MI-PRINCIPAL-ID> --scope "/dbs/orders/colls/items"
```
Bicep: `Microsoft.Authorization/roleAssignments` with `scope: container` (symbolic reference
to the child resource) and `principalType: 'ServicePrincipal'` for identities.

## 3. Enforce Entra-only
- Storage: `az storage account update --allow-shared-key-access false` and
  `--allow-blob-public-access false`; Policy `Storage accounts should prevent shared key access`.
  Clients: `az storage blob ... --auth-mode login`, SDK `DefaultAzureCredential`.
- Key Vault: `az keyvault update --enable-rbac-authorization true` (migrate access policies first).
- Service Bus/Event Hubs: `az servicebus namespace update --disable-local-auth true`.
- Cosmos: `az cosmosdb update --disable-key-based-metadata-write-access true` and
  `properties.disableLocalAuth=true` via `az resource update`.
- App Configuration: `az appconfig update --disable-local-auth true`.

## 4. Humans
Give people `*Data Reader` on prod via PIM-eligible groups; Contributor-class data roles on
prod only time-bound. Portal "Storage browser" needs the data role too — subscription Reader
alone shows "You do not have permission to list data".

## Gotchas
- Control-plane roles with `listKeys` (Contributor, Storage Account Contributor) let a user fetch the keys and bypass data RBAC until shared-key access is disabled.
- `Storage Blob Data Owner` is needed for ADLS Gen2 ACL management; `Contributor` can't `setAccessControl`.
- Key Vault `Reader` does not read secrets; `Key Vault Reader` reads metadata only — people assign both and still get 403.
- Cosmos data RBAC assignments don't show in `az role assignment list`; audit them separately.
- Role propagation for data planes can take minutes; retries in app startup are warranted.
- Event Hubs consumer-group-scoped assignments require the `Data Receiver` role at the consumer group **or** above; sender scope at the hub.

## Verify
- [ ] `az storage blob list --account-name <SA> -c uploads --auth-mode login` works for the identity; fails from an identity without the role.
- [ ] `az storage account show --query allowSharedKeyAccess` is `false` on prod accounts; Key Vault `enableRbacAuthorization` true.
- [ ] No role assignment grants `*Data Owner`/Contributor at subscription scope to an app identity (`az role assignment list --all --query "[?contains(roleDefinitionName,'Data') && scope=='/subscriptions/<SUB>']"` empty).
