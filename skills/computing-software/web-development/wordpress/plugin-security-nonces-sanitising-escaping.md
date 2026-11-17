---
id: computing-software.web-development.wordpress.plugin-security-nonces-sanitising-escaping
name: plugin-security-nonces-sanitising-escaping
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, wp-nonces, wordpress-escaping, sanitization, capabilities, wpdb-prepare, plugin-security, php, web-development]
level: practitioner
status: docs-checked
description: "Securing WordPress plugin code: capability checks, nonces for CSRF, sanitising input, escaping output late, $wpdb->prepare, and REST/AJAX permission callbacks."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/pluggable.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wpdb.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/rest-api.php
  - https://developer.wordpress.org/apis/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nonces, sanitising, escaping and capabilities

**Goal:** every request handler checks who, checks intent, cleans input and escapes output - the four checks reviewers look for.

## 1. Capability (who)
```php
if ( ! current_user_can( 'edit_post', $post_id ) ) {
    wp_die( esc_html__( 'Not allowed.', 'acme' ), 403 );
}
```
Check capabilities, not roles (`current_user_can( 'administrator' )` is wrong). Use meta capabilities with object ids (`edit_post`, `delete_user`) so ownership rules apply. `is_admin()` only means "an admin screen is loading", not "user is an admin".

## 2. Nonce (intent / CSRF)
```php
// form
wp_nonce_field( 'acme_save_' . $post_id, 'acme_nonce' );
// handler
if ( ! isset( $_POST['acme_nonce'] ) || ! wp_verify_nonce( sanitize_key( wp_unslash( $_POST['acme_nonce'] ) ), 'acme_save_' . $post_id ) ) {
    wp_die( 'Invalid request', 400 );
}
// admin-post / links
check_admin_referer( 'acme_delete_' . $id );
// AJAX
check_ajax_referer( 'acme_ajax', 'nonce' );
```
Nonces are tied to user and action and (by default) valid for between 12 and 24 hours (filter `nonce_life`); they are not authentication and don't replace capability checks. REST requests use the `X-WP-Nonce` header with the `wp_rest` action for cookie auth.

## 3. Sanitise input (on the way in)
```php
$title = sanitize_text_field( wp_unslash( $_POST['title'] ?? '' ) );
$email = sanitize_email( wp_unslash( $_POST['email'] ?? '' ) );
$url   = esc_url_raw( wp_unslash( $_POST['url'] ?? '' ) );
$id    = absint( $_GET['id'] ?? 0 );
$html  = wp_kses_post( wp_unslash( $_POST['bio'] ?? '' ) );
$key   = sanitize_key( $_POST['mode'] ?? '' );
if ( ! in_array( $key, [ 'grid', 'list' ], true ) ) { $key = 'grid'; }   // validate against allow-list
```
`wp_unslash` first: WordPress adds slashes to the request superglobals.

## 4. Escape output (late, at echo time)
```php
<h2><?php echo esc_html( $title ); ?></h2>
<a href="<?php echo esc_url( $url ); ?>" title="<?php echo esc_attr( $label ); ?>">
<script>const cfg = <?php echo wp_json_encode( $data ); ?>;</script>
<?php echo wp_kses_post( $bio ); ?>
<?php esc_html_e( 'Saved', 'acme' ); ?>
```
Escape even "trusted" DB values - they may have been stored by another path.

## 5. SQL
```php
$rows = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->prefix}acme_logs WHERE user_id = %d AND status = %s LIMIT %d", $uid, $status, 50 ) );
$like = '%' . $wpdb->esc_like( $term ) . '%';
```
Table and column names were not placeholders before the `%i` identifier placeholder (WordPress 6.2); allow-list identifiers you build into SQL, or use `%i`.

## 6. REST and AJAX
`register_rest_route` must set a `permission_callback` (since 5.5.0 a missing one raises a `_doing_it_wrong()` notice; `'__return_true'` only for genuinely public data). `wp_ajax_nopriv_*` handlers are reachable by anyone.

## Verify
- [ ] Each handler tested as a subscriber and logged out: denied.
- [ ] Submitting without/with a stale nonce fails.

## Checked

2026-10-25: against wordpress-develop trunk source (`pluggable.php`, `class-wpdb.php`, `rest-api.php`; last commit 2026-10-25). Confirmed: nonce validity of 12 to 24 hours with the `nonce_life` filter, `check_ajax_referer` and `wp_verify_nonce` behaviour, `%i` identifier placeholder in `wpdb::prepare`, `permission_callback` notice since 5.5.0, `wp_rest` nonce for cookie REST auth. Removed the unconfirmed PHPCS sniff reference.

Method: documentation only; no commands were run.
