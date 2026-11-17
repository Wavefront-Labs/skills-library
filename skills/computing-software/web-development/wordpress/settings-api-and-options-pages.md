---
id: computing-software.web-development.wordpress.settings-api-and-options-pages
name: settings-api-and-options-pages
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, settings-api, options-page, register-setting, sanitize-callback, add-options-page, php, web-development]
level: practitioner
status: docs-checked
description: "Building WordPress plugin settings screens with the Settings API: register_setting with sanitize callbacks, sections and fields, capability checks, autoload and REST exposure."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/option.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-admin/options.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-admin/options-head.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-admin/includes/plugin.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-admin/includes/template.php
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Settings API and options pages

**Goal:** a plugin settings page with nonce handling, validation and capability checks handled by core.

## 1. Register the setting
```php
add_action( 'admin_init', function () {
    register_setting( 'acme_settings', 'acme_options', [
        'type'              => 'object',
        'sanitize_callback' => 'acme_sanitize_options',
        'default'           => [ 'api_key' => '', 'per_page' => 10 ],
        'show_in_rest'      => false,
    ] );
    add_settings_section( 'acme_main', __( 'General', 'acme' ), '__return_false', 'acme' );
    add_settings_field( 'acme_per_page', __( 'Items per page', 'acme' ), 'acme_field_per_page', 'acme', 'acme_main',
        [ 'label_for' => 'acme_per_page' ] );
} );

function acme_sanitize_options( $input ) {
    $out = get_option( 'acme_options', [] );
    $out['per_page'] = min( 100, max( 1, absint( $input['per_page'] ?? 10 ) ) );
    $out['api_key']  = sanitize_text_field( $input['api_key'] ?? '' );
    if ( '' === $out['api_key'] ) {
        add_settings_error( 'acme_options', 'missing_key', __( 'API key is required.', 'acme' ) );
    }
    return $out;
}
```
Store related values in one array option rather than many options.

## 2. The page
```php
add_action( 'admin_menu', function () {
    add_options_page( __( 'Acme', 'acme' ), __( 'Acme', 'acme' ), 'manage_options', 'acme', 'acme_render_page' );
} );
function acme_render_page() {
    if ( ! current_user_can( 'manage_options' ) ) return;
    ?>
    <div class="wrap"><h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
      <form action="options.php" method="post">
        <?php settings_fields( 'acme_settings' );  // nonce + option_page + action
              do_settings_sections( 'acme' );
              submit_button(); ?>
      </form></div>
    <?php
}
function acme_field_per_page() {
    $o = get_option( 'acme_options' );
    printf( '<input type="number" id="acme_per_page" name="acme_options[per_page]" value="%d" min="1" max="100">', (int) $o['per_page'] );
}
```
Posting to `options.php` gives nonce verification (`settings_fields()` prints `option_page`, `action=update` and a `{group}-options` nonce), a capability check (filter `option_page_capability_{$option_page}` to change it) and sanitisation through the registered callback. Core prints `settings_errors()` on Settings sub-pages (`options-head.php`); call `settings_errors()` yourself on other pages.

## 3. Autoload
Options load on every request when autoloaded. Large or rarely used options: `add_option( 'acme_cache', $v, '', false )` or `update_option( $name, $v, false )`. Since WordPress 6.6.0, when `$autoload` is not specified, a value larger than 150000 bytes is saved with autoload off (filter `wp_max_autoloaded_option_size`).

## 4. Secrets
API keys in options are readable by any admin and in DB backups. Allow a `wp-config.php` constant override (`defined( 'ACME_API_KEY' ) ? ACME_API_KEY : $opt['api_key']`) and never echo the full key back.

## 5. REST and block editor
`show_in_rest` (true or an array with `schema`) exposes the setting through the REST API settings endpoint, which React-based settings pages can use.

## Verify
- [ ] Saving with an Editor-role account is refused.
- [ ] Out-of-range/malicious input is sanitised (try `<script>` and `-5`).
- [ ] Autoloaded plugin options are small.

## Checked

2026-10-25: against wordpress-develop trunk source (`option.php`, `options.php`, `options-head.php`, `wp-admin/includes/plugin.php`, `template.php`; last commit 2026-10-25). Confirmed: `register_setting` args (`type` values string/boolean/integer/number/array/object, `default`, `sanitize_callback`, `show_in_rest`), `settings_fields()` output, `option_page_capability_{$option_page}` filter, `options-head.php` calling `settings_errors()`, the 150000-byte autoload threshold from 6.6.0, `add_settings_field` `label_for` arg. Removed the unconfirmed `/wp/v2/settings` path, the SQL check and the one-row performance claim.

Method: documentation only; no commands were run.
