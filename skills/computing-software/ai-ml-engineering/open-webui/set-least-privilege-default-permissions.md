---
id: computing-software.ai-ml-engineering.open-webui.set-least-privilege-default-permissions
name: set-least-privilege-default-permissions
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [rbac, permissions, least-privilege, default-permissions, tools-access, open-webui]
level: practitioner
status: docs-checked
description: "Configure Open WebUI default and group permissions across workspace, sharing, chat, features and settings, starting from least privilege."
sources:
  - https://docs.openwebui.com/features/authentication-access/rbac/permissions
  - https://docs.openwebui.com/features/authentication-access/rbac/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: lock the baseline down, then grant features through groups.

## Model
Permissions are additive: effective = Global Defaults + all groups (parents included). If any source says True, the user has it; there is no deny. To remove a feature, disable it in Default Permissions AND every group that grants it. Admins are exempt from every permission.

## Steps
1. Admin Panel > Users > Groups > **Default Permissions**: switch on only what every user needs.
2. Create groups ("Creators", "Power Users") and toggle extra permissions on there.
3. Add users to the group to promote them.
4. Create an "Administrators" group so new admin-relevant permissions can be granted in one place.

## Five categories (exact toggles worth knowing)
- Workspace: Models Access (parent of Import/Export Models, Hidden Models), Knowledge Access, Prompts Access, Tools Access, Skills Access (+Import/Export children). Children need their parent.
- Sharing: per-type parent (Models Sharing, Knowledge Sharing, ...) plus the matching Public Sharing; Chats Public Sharing vs Chats Open Sharing (only the latter exposes a link to people without an account, off by default); Allow Sharing With Users/Groups (on by default; env `USER_PERMISSIONS_ACCESS_GRANTS_ALLOW_USERS` / `_GROUPS`). A disallowed audience returns 403.
- Chat: Allow Chat Controls (parent of Valves, System Prompt, Params), File Upload, Web Upload, Chat Delete, Chat Edit, Chat Share, Chat Export, Chat Import, Multiple Models, Temporary Chat (parent of Side Chat and Enforce Temporary Chat). Allow Chat Params only hides the panel; users can still send parameters through the API.
- Features: API Keys, Notes, Channels, Folders, Web Search, Image Generation, Code Interpreter, Direct Tool Servers (also needs `ENABLE_DIRECT_INTEGRATIONS`), Memories, Automations, Calendar, User Webhooks (off by default).
- Settings: Interface Settings Access hides the Interface page only.

## Env defaults
Prefix `USER_PERMISSIONS_` (e.g. `USER_PERMISSIONS_CHAT_FILE_UPLOAD=True`, `USER_PERMISSIONS_CHAT_DELETE`, `USER_PERMISSIONS_CHAT_TEMPORARY_ENFORCED`, `USER_PERMISSIONS_FEATURES_CHANNELS`, `USER_PERMISSIONS_WORKSPACE_MODELS_HIDDEN`). These are initial defaults; the UI is the recommended manager.

## Gotchas
- **Tools Access is root-equivalent**: Tools and Functions run arbitrary Python on the server. Grant only to people you would trust with a shell. It is hidden when `ENABLE_PLUGINS` or `ENABLE_TOOLS` is false.
- Instance-wide toggles (for example Notes Sharing, API Keys, Web Search, Direct Tool Servers) only show while the feature is on globally; hidden toggles keep their saved value.
- API key creation needs the global API Keys switch AND `features.api_keys` for non-admins.
- After upgrading from older releases, recheck Tools Public Sharing and Notes Public Sharing in Default Permissions; values saved by the old UI are not rolled back.
- RBAC does not replace provider-side least privilege: use inference-scoped keys for LiteLLM/OpenRouter connections, not master keys.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/authentication-access/rbac/permissions and the RBAC index. Corrected the list of instance-wide toggles to the ones the page names.
Method: documentation only; no commands were run.
