---
id: computing-software.web-development.react.server-functions-security
name: server-functions-security
category: computing-software
field: web-development
product: react
tags: [server-functions-security, server-actions, use-server, input-validation, authorization, react-server-components]
level: advanced
status: docs-checked
description: "Securing React Server Functions/Actions: they are public endpoints, so validate input, authorise inside each action, avoid leaking data via closures/returns, limits and patching."
sources:
  - https://react.dev/reference/rsc/use-server#security
  - https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components
  - https://nextjs.org/docs/app/guides/data-security
  - https://nextjs.org/docs/app/guides/server-actions
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/serverActions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server Functions security

A `"use server"` function becomes an HTTP endpoint the client can call with **any arguments**, at any time, from outside your UI. Hiding the button that calls it protects nothing.

## 1. Validate every argument
```ts
"use server";
import { z } from "zod";
const Input = z.object({ postId: z.uuid(), title: z.string().min(1).max(200) });

export async function renameDraft(raw: unknown) {
  const session = await auth();                         // authenticate inside the action
  if (!session) throw new Error("Unauthorized");
  const { postId, title } = Input.parse(raw);           // never trust TS types at runtime
  const post = await db.post.findUnique({ where: { id: postId } });
  if (!post || post.authorId !== session.user.id) throw new Error("Not found");   // authorise per object
  await db.post.update({ where: { id: postId }, data: { title } });
  revalidatePath(`/posts/${postId}`);
  return { ok: true };                                  // return minimal data
}
```
FormData-based actions: parse `formData.get(...)` with the same schema.

## 2. Centralise checks
Put authorisation in a data access layer (`getPostForEdit(user, id)`) used by both pages and actions, so an action cannot skip a check the page performed.

## 3. Data leakage
- Inline server functions in Server Components close over variables; Next.js encrypts captured values before sending them to the client (set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` to a stable key for multi-instance deployments), but do not capture secrets or whole records. Pass ids and re-fetch.
- Return values and thrown error messages are sent to the client; return DTOs, log details server-side.
- Use `server-only` and the experimental taint APIs (`experimental_taintObjectReference`, `experimental_taintUniqueValue`) as an extra layer against accidental serialisation of sensitive objects; still filter data in your data access layer.

## 4. Platform protections and limits
- Next.js compares the `Origin` header host to the app's own host (`x-forwarded-host` or `host`) for Server Actions as CSRF defence; if a proxy forwards a different host, add it to `serverActions.allowedOrigins` rather than disabling checks.
- Body size limit (Next `serverActions.bodySizeLimit`, default 1 MB); add rate limiting for expensive or sensitive actions.
- Next.js uses encrypted, non-deterministic action IDs and removes unused actions from client bundles, but treat every exported action as reachable by a direct POST request.

## 5. Patch the RSC stack
Server Components and Actions deserialise client-supplied payloads; CVE-2025-55182 (unauthenticated remote code execution, CVSS 10.0, disclosed 2025-12-03) affected `react-server-dom-webpack`, `-parcel` and `-turbopack` 19.0 to 19.2.0 and was fixed in 19.0.1, 19.1.2 and 19.2.1. Track security advisories for `react-server-dom-*` and your framework, and upgrade promptly.

## Verify
- [ ] A test calls each action directly (outside the UI) as anonymous and as another user and gets rejected; invalid payloads return validation errors, not 500s with stack traces.

## Checked

Checked 2026-10-25 against the React docs (use-server page, Dec 2025 security post), the Next.js docs (16.4.3: data-security, server-actions and serverActions config pages) and the zod 4 docs. Confirmed: Server Function arguments are fully client-controlled and must be validated and authorised inside each function; Server Functions are exposed endpoints; Next.js `allowedOrigins` matches the `Origin` host against `x-forwarded-host` or `host`; `bodySizeLimit` defaults to 1MB; encrypted action IDs, dead code elimination and closure-variable encryption; taint APIs are experimental; `import "server-only"`; CVE-2025-55182 and its fixed versions; top-level `z.uuid()`. Replaced the "action ids are not secrets" and "tree-shaken" wording with the Next.js documentation's wording and dropped the Next.js blog source.

Method: documentation only; no commands were run.
