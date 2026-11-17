---
id: computing-software.web-development.wordpress.admin-ajax-handlers
name: admin-ajax-handlers
category: computing-software
field: web-development
product: wordpress
tags: [admin-ajax, wp-ajax, wordpress-ajax, nonces, wordpress]
level: practitioner
status: docs-checked
description: "Writing admin-ajax.php handlers safely: wp_ajax and nopriv hooks, nonces and capability checks, wp_send_json responses, and when to use the REST API instead."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-admin/admin-ajax.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/pluggable.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/functions.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/functions.wp-scripts.php
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# admin-ajax handlers

## 1. Handler
```php
add_action( 'wp_ajax_acme_save_note', 'acme_save_note' );          // logged-in users
// add_action( 'wp_ajax_nopriv_acme_save_note', ... );              // only if visitors may call it
function acme_save_note() {
    check_ajax_referer( 'acme_note', 'nonce' );                     // wp_die( -1, 403 ) on failure (default $stop = true)
    $post_id = absint( $_POST['post_id'] ?? 0 );
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        wp_send_json_error( [ 'message' => __( 'Not allowed', 'acme' ) ], 403 );
    }
    $note = sanitize_textarea_field( wp_unslash( $_POST['note'] ?? '' ) );
    update_post_meta( $post_id, '_acme_note', $note );
    wp_send_json_success( [ 'saved' => true ] );                    // sends JSON and calls wp_die()
}
```
- Nonces prove intent (CSRF), not permission: always pair with `current_user_can()` for the specific object.
- `wp_unslash()` before sanitising (WordPress adds slashes to superglobals).
- `nopriv` handlers are public endpoints: validate everything and never expose private data.

## 2. JavaScript side
```php
wp_enqueue_script( 'acme-notes', plugins_url( 'notes.js', __FILE__ ), [], '1.0', true );
wp_localize_script( 'acme-notes', 'acmeNotes', [ 'ajaxUrl' => admin_url( 'admin-ajax.php' ), 'nonce' => wp_create_nonce( 'acme_note' ) ] );
// or wp_add_inline_script( 'acme-notes', 'const acmeNotes = ' . wp_json_encode( [...] ), 'before' );
```
```js
const body = new URLSearchParams({ action: "acme_save_note", nonce: acmeNotes.nonce, post_id, note });
const res = await fetch(acmeNotes.ajaxUrl, { method: "POST", body, credentials: "same-origin" });
const json = await res.json();     // { success: true, data: {...} }
```
The `action` parameter selects the hook (`wp_ajax_{action}` for logged-in users, `wp_ajax_nopriv_{action}` for visitors); `admin-ajax.php` answers `0` with HTTP 400 when no handler is registered for the action.

## 3. Performance
`admin-ajax.php` loads WordPress and the admin includes (`wp-admin/includes/admin.php`) on every call and sends no-cache headers: avoid it for frequent front-end requests (polling, search-as-you-type on high-traffic sites). The Heartbeat API also runs through admin-ajax (`wp_ajax_heartbeat`).

## 4. Prefer the REST API for new code
`register_rest_route()` gives proper HTTP methods and status codes, argument validation via `args`, and a `permission_callback`. Use admin-ajax mainly for legacy compatibility.

## Verify
- [ ] Requests without a valid nonce or capability fail with 403; responses use wp_send_json_*; public nopriv handlers validated; new endpoints use REST.

## Checked

2026-10-25: against wordpress-develop trunk source (`admin-ajax.php`, `pluggable.php`, `functions.php`, `functions.wp-scripts.php`; last commit 2026-10-25). Confirmed: `check_ajax_referer( $action, $query_arg, $stop )` dies with `-1` and 403, `wp_ajax_`/`wp_ajax_nopriv_` dispatch and the 400 response for unknown actions, `wp_send_json_success`/`wp_send_json_error` signatures with status code, `wp_ajax_heartbeat`, `wp_add_inline_script` position argument. Removed unconfirmed claims about `api-fetch` nonce handling, REST cacheability, Heartbeat throttling and rate limiting.

Method: documentation only; no commands were run.
