---
id: computing-software.web-development.wordpress.custom-rest-endpoints-and-authentication
name: custom-rest-endpoints-and-authentication
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, register-rest-route, application-passwords, rest-api, permission-callback, wp-rest-request, php, web-development, wordpress-apis]
level: practitioner
status: docs-checked
description: "Building custom WordPress REST endpoints: register_rest_route with args schema and permission_callback, responses and errors, cookie nonce vs application passwords auth."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/rest-api.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/rest-api/class-wp-rest-server.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/user.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-application-passwords.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/rest-api/endpoints/class-wp-rest-users-controller.php
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom REST endpoints and authentication

**Goal:** endpoints with validated input, explicit authorisation and the right auth method per client.

## 1. Register
```php
add_action( 'rest_api_init', function () {
    register_rest_route( 'acme/v1', '/events/(?P<id>\d+)/rsvp', [
        'methods'             => WP_REST_Server::CREATABLE,          // POST
        'callback'            => 'acme_rsvp',
        'permission_callback' => fn( WP_REST_Request $r ) => is_user_logged_in() && current_user_can( 'read_post', (int) $r['id'] ),
        'args'                => [
            'id'     => [ 'type' => 'integer', 'required' => true ],
            'guests' => [ 'type' => 'integer', 'minimum' => 0, 'maximum' => 5, 'default' => 0 ],
            'note'   => [ 'type' => 'string', 'maxLength' => 500, 'sanitize_callback' => 'sanitize_textarea_field' ],
        ],
    ] );
} );

function acme_rsvp( WP_REST_Request $request ) {
    $event = get_post( $request['id'] );
    if ( ! $event || 'event' !== $event->post_type ) {
        return new WP_Error( 'acme_not_found', __( 'Event not found.', 'acme' ), [ 'status' => 404 ] );
    }
    $rsvp = acme_create_rsvp( $event->ID, get_current_user_id(), $request['guests'], $request['note'] );
    return new WP_REST_Response( [ 'id' => $rsvp->id, 'guests' => $rsvp->guests ], 201 );
}
```
- `permission_callback` is required: since WordPress 5.5.0 core raises a `_doing_it_wrong()` notice when it is missing; use `'__return_true'` only for public data.
- `args` with JSON-schema keywords are validated automatically (`rest_validate_request_arg`), returning 400 with details.
- Namespace with vendor + version (`acme/v1`); don't add routes under `wp/v2`.

## 2. Authentication options
| Client | Method |
|---|---|
| JS on the same WP site | cookie + a `wp_rest` nonce sent as the `X-WP-Nonce` header (`wp_create_nonce( 'wp_rest' )`) |
| Server-to-server, scripts, mobile | Application Passwords (WP 5.6+), available on sites using SSL or a `local` environment type (HTTP Basic auth with the user name and the generated password) |
| Third-party apps acting for users | an OAuth plugin (not part of core) |
Without a valid nonce, cookie-authenticated requests are treated as logged out (core resets the current user to 0) or rejected with `rest_cookie_invalid_nonce` (403). Application passwords authenticate API requests only (REST and XML-RPC by default), not wp-admin logins.

## 3. Responses
Return arrays/`WP_REST_Response`/`WP_Error`; never `echo`+`exit`. Set headers with `$response->header( 'Name', 'value' )`. Add a `schema` callback to a route for discoverability.

## 4. Extending core objects
`register_rest_field( 'post', 'acme_rating', [ 'get_callback' => ..., 'schema' => [...] ] )` adds fields to core responses; avoid expensive callbacks, which run for every item in a collection.

## 5. Exposure review
List routes with `GET /wp-json/`. Review what the users endpoint exposes: it lists users who have published posts in REST-enabled post types without authentication.

## Verify
- [ ] Unauthenticated and subscriber requests to protected routes return 401/403.
- [ ] Invalid args return 400 with a `rest_invalid_param` error.
- [ ] Application password requests work on an SSL site.

## Checked

2026-10-25: against wordpress-develop trunk source (`rest-api.php`, `class-wp-rest-server.php`, `user.php`, `class-wp-application-passwords.php`, users controller; last commit 2026-10-25). Confirmed: `WP_REST_Server::CREATABLE` is POST, `permission_callback` notice since 5.5.0, `rest_validate_request_arg`, cookie nonce handling (`rest_cookie_check_errors`, `rest_cookie_invalid_nonce` 403, `X-WP-Nonce`/`wp_rest`), Application Passwords since 5.6.0 and the SSL-or-local requirement, API-only use, users endpoint published-posts rule. Removed unconfirmed claims about `api-fetch`, the curl line, `wp rest route list`, the `_fields` param advice and OPTIONS schema output.

Method: documentation only; no commands were run.
