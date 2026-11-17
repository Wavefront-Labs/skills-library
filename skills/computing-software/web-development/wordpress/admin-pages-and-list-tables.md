---
id: computing-software.web-development.wordpress.admin-pages-and-list-tables
name: admin-pages-and-list-tables
category: computing-software
field: web-development
product: wordpress
tags: [add-menu-page, wp-list-table, admin-post, admin-enqueue-scripts, wordpress-admin, wordpress]
level: practitioner
status: docs-checked
description: "Building WordPress admin screens: add_menu_page/add_submenu_page, capability checks, admin-post form handlers and WP_List_Table."
sources:
  - https://developer.wordpress.org/plugins/administration-menus/top-level-menus/
  - https://developer.wordpress.org/reference/classes/wp_list_table/
  - https://developer.wordpress.org/reference/hooks/admin_post_action/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admin pages and list tables

## 1. Register the page
```php
add_action('admin_menu', function () {
  add_menu_page('Bookings', 'Bookings', 'manage_bookings', 'acme-bookings', 'acme_render_bookings', plugin_dir_url(__FILE__) . 'images/icon.png', 26);
  add_submenu_page('acme-bookings', 'Settings', 'Settings', 'manage_options', 'acme-bookings-settings', 'acme_render_settings');
});
function acme_render_bookings() {
  if (!current_user_can('manage_bookings')) wp_die(__('Sorry, you are not allowed to access this page.'));
  echo '<div class="wrap"><h1>' . esc_html__('Bookings', 'acme') . '</h1>';
  $table = new Acme_Bookings_Table(); $table->prepare_items();
  echo '<form method="get"><input type="hidden" name="page" value="acme-bookings">';
  $table->search_box(__('Search'), 'booking'); $table->display(); echo '</form></div>';
}
```

## 2. WP_List_Table
```php
class Acme_Bookings_Table extends WP_List_Table {
  public function get_columns() { return ['cb' => '<input type="checkbox">', 'name' => 'Name', 'date' => 'Date']; }
  protected function column_default($item, $col) { return esc_html($item[$col]); }
  protected function column_cb($item) { return sprintf('<input type="checkbox" name="ids[]" value="%d">', $item['id']); }
  protected function get_bulk_actions() { return ['cancel' => 'Cancel']; }
  public function prepare_items() {
    $per = 20; $page = $this->get_pagenum();
    [$rows, $total] = acme_query_bookings($_GET['s'] ?? '', $per, ($page - 1) * $per);
    $this->items = $rows;
    $this->_column_headers = [$this->get_columns(), [], []];
    $this->set_pagination_args(['total_items' => $total, 'per_page' => $per]);
  }
}
```
Bulk actions: verify the `bulk-{plural}` nonce (the table renders it with `wp_nonce_field('bulk-' . plural)`) and the user's capability before acting. The WP_List_Table reference notes that the class is marked private; check that note before relying on it.

## 3. Form handlers
```php
// admin_post_{action} fires for requests to wp-admin/admin-post.php?action=acme_save_booking
add_action('admin_post_acme_save_booking', function () {
  // verify the nonce and the user's capability, sanitise input, save, then redirect and exit
});
```
The form posts to `admin-post.php` with a hidden `action` field set to `acme_save_booking` (admin_post_{$action} reference).

## Verify
- [ ] Page hidden from and inaccessible to users without the capability; bulk actions reject missing nonces.

## Checked

2026-10-28. Confirmed from the WP_List_Table reference (`column_default`, `_column_headers`, `set_pagination_args`, `get_pagenum`, `search_box`, `bulk-` plural nonce, class marked private), the admin_post_{$action} reference (requests to `admin-post.php?action=...`) and the Top-Level Menus handbook (`add_menu_page`, `add_submenu_page`). Removed (not found): the `load-$hook` and `admin_enqueue_scripts` asset-loading code, `DataViews`, `action`/`action2` details, `admin_notices` markup, and the detailed form-handler body (nonce function names were not in the fetched pages, so the skill now only says to verify a nonce and capability).

Method: documentation only; no commands were run.
