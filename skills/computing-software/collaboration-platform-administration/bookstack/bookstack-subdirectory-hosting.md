---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-subdirectory-hosting
name: bookstack-subdirectory-hosting
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, subdirectory, sub-path, apache-alias, nginx-proxy, app-url, reverse-proxy]
level: advanced
status: docs-checked
description: "Serve BookStack from a URL sub-path with an Apache Alias or an nginx proxy to a local server block, with the APP_URL rule and web-root security caveats."
sources: ["https://www.bookstackapp.com/docs/admin/subdirectory-setup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack in a subdirectory

Install BookStack outside any web root (for example under `/var/www/bookstack`), and make sure it is reachable by no other route. Never place it inside another site's web root.

Apache: `a2enmod rewrite`; in the site's VirtualHost add an `Alias /bookstack /var/www/bookstack/public`; add a `<Directory>` for `public` with `RewriteEngine on`, a 301 redirect for trailing slashes on non-directory paths, and a rule sending other non-file requests to `index.php`; add a `<Directory>` for the install root with `Require all denied`; restart Apache.

Nginx: add a separate server block on a local port (the docs use 8080 on localhost) with `root` at the `public` folder, `try_files` falling back to `index.php`, and PHP passed to php-fpm (adjust the socket for your PHP version). In the existing site add `location /bookstack/ { proxy_pass http://localhost:8080/; proxy_redirect off; }`. The trailing slashes matter. Check with `nginx -t`.

For both, set `APP_URL` in `.env` to the base URL including the sub-path with no trailing slash (for example `https://example.com/bookstack`); the Alias or location path must match it. Docker users are advised to use a reverse proxy instead.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/subdirectory-setup/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
