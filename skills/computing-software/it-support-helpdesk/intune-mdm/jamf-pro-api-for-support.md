---
id: computing-software.it-support-helpdesk.intune-mdm.jamf-pro-api-for-support
name: jamf-pro-api-for-support
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, jamf-pro-api, jamf-pro, api-clients, bearer-token, client-credentials, api-roles]
level: advanced
status: docs-checked
description: "Authenticate to the Jamf Pro API from support scripts: API roles and clients, client credentials vs bearer tokens, token lifetime and keep-alive, HTTP methods and response codes."
sources:
  - "https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview"
  - "https://developer.jamf.com/jamf-pro/docs/client-credentials"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jamf-pro-api-for-support

Support teams script Jamf for lookups and bulk actions. This skill covers access and authentication; endpoint-specific calls come from the built-in API reference.

## Where the API lives
- The base URL is `/api` on each Jamf Pro instance; documentation and "Try it out" are built in at `/api/doc`.
- API authentication does not support SSO.
- Both the Jamf Pro API and the Classic API accept Client Credentials authorization since Jamf Pro 10.49.0.

## Preferred: API roles and clients (client credentials)
1. Create an API Role: a collection of privileges defining which endpoints a client may use. Create an API Client and assign one or more roles (privileges are cumulative). Roles and clients can also be managed through the api-roles and api-integrations endpoints; api-role-privileges lists available privileges.
2. Client credentials give access only to Jamf Pro APIs, protecting administrator credentials and the Jamf Pro UI.
3. A client ID and client secret cannot call endpoints directly; exchange them for a short-lived access token (the "Obtain an access token using an API Client" endpoint), which works on both Classic and Jamf Pro APIs.
4. Adding or removing a role on an existing client needs the client secret rotated to take effect. Adding or removing a privilege on a role takes effect immediately for newly generated tokens.
5. Jamf provides Postman collections for both APIs (environment variables client_id, client_secret, and baseUrl for the Jamf Pro API or url for Classic; the two names and values differ).

## Alternative: bearer token with a user account
- Send a POST with basic authentication to `/v1/auth/token`; the response has a token and an expiry. Send `Authorization: Bearer TOKEN_VALUE` on later requests.
- Tokens expire after 20 minutes by default; POST to `/v1/auth/keep-alive` with a valid token to get a new one (the previous token is invalidated).
- Privileges map to HTTP methods: Create, Read, Update and Delete correspond to POST, GET, PUT and DELETE. Check "Privileges and Deprecations" for each operation.

## HTTP methods and codes
- POST creates objects or issues actions (JSON body required). GET retrieves (many endpoints support query parameters for search, sort, filter). PUT overwrites the fields in the body and sets omitted fields to null. PATCH updates selected fields. DELETE removes.
- Most endpoints use JSON; the Accept header indicates data types, and some endpoints support others.
- Codes: 200, 201, 202 (accepted, not complete), 204 (deleted); 400 bad request (check body); 401 authentication failed; 403 insufficient permissions; 404 wrong path; 409 conflict; 412 precondition failed; 413 payload too large; 414 URI too long; 500 retry or contact support; 503 unavailable.

## Good practice
Use read-only clients for reporting and separate clients for commands rather than administrator credentials, and store the client secret in a vault. Test destructive actions on a test device.

## Verify
A token request succeeds, a GET against a known record returns it, and the client's role shows only the privileges the script needs.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Jamf Pro API overview and Client Credentials pages (both read in full). The Jamf learn.jamf.com page was a stub and was dropped. Removed because the pages do not state them: the example curl calls, the `/api/oauth/token` path and 60-second token lifetime, inventory RSQL filters, the MDM command payload, Classic API paths and XML default, rate-limit advice and the Jamf Cloud basic-auth deprecation claim.
