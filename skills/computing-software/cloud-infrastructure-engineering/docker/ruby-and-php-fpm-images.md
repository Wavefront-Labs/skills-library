---
id: computing-software.cloud-infrastructure-engineering.docker.ruby-and-php-fpm-images
name: ruby-and-php-fpm-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, ruby-image, php-fpm-image, rails, laravel, bundler, composer, language-images]
level: practitioner
description: "Build Rails images with bundler deployment mode and jemalloc, and PHP-FPM images with docker-php-ext-install and pinned PECL."
sources: ["https://hub.docker.com/_/ruby", "https://hub.docker.com/_/php", "https://github.com/rails/rails/blob/main/railties/lib/rails/generators/rails/app/templates/Dockerfile.tt", "https://getcomposer.org/doc/articles/autoloader-optimization.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ruby and PHP-FPM images

## Ruby / Rails
The Rails generator template (`Dockerfile.tt`) is the reference shape. Three stages: `base`, a
throw-away `build`, and a final non-root stage.
```dockerfile
# syntax=docker/dockerfile:1
ARG RUBY_VERSION=3.3
FROM docker.io/library/ruby:$RUBY_VERSION-slim AS base
WORKDIR /rails
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y libjemalloc2 libpq5 && \
    ln -s /usr/lib/$(uname -m)-linux-gnu/libjemalloc.so.2 /usr/local/lib/libjemalloc.so && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development" \
    LD_PRELOAD="/usr/local/lib/libjemalloc.so"

FROM base AS build
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential git libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git
COPY . .
RUN bundle exec bootsnap precompile app/ lib/
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

FROM base
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash
USER 1000:1000
COPY --chown=rails:rails --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --chown=rails:rails --from=build /rails /rails
ENTRYPOINT ["/rails/bin/docker-entrypoint"]
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```
- jemalloc is preloaded "for reduced memory usage and latency" (template comment).
- `SECRET_KEY_BASE_DUMMY=1` lets assets precompile without `RAILS_MASTER_KEY`.
- Match the `RUBY_VERSION` build arg to the app's `.ruby-version`.
- Native gems need `-dev` headers and compilers only in the build stage.
- The package lists in the real template come from the generator and vary with the app (Node, Bun,
  database adapter); adapt this sketch rather than copying it blindly.

## PHP
The official `php` image provides `docker-php-ext-configure`, `docker-php-ext-install` and
`docker-php-ext-enable`. You must install an extension's system dependencies yourself.
```dockerfile
FROM php:8.3-fpm
RUN docker-php-ext-install -j"$(nproc)" pdo_mysql opcache
RUN pecl install redis-5.3.7 && docker-php-ext-enable redis
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
```
- Always pin an explicit PECL version: PECL does not check PHP compatibility when choosing a
  version. Install PECL extensions in series (`pecl install a && pecl install b`) so a failure is
  not skipped; `docker-php-ext-enable a b` can be one command.
- The image ships `php.ini-development` and `php.ini-production`; copy or move one to
  `$PHP_INI_DIR/php.ini`. Enabling OPcache is recommended for production.
- Run the FPM variants as an arbitrary user with `docker run --user`, for example `--user 1000:1000`.
- Composer: `composer install --optimize-autoloader` (or `dump-autoload -o`) builds a classmap;
  `-a` / `--classmap-authoritative` additionally stops the autoloader falling back to the filesystem.
  The Composer docs list the trade-offs of each level, so read them before enabling `-a`.

## Verify
`docker run --rm app php -m` lists loaded extensions; for Rails, `docker run --rm app ./bin/rails runner 'puts :ok'`.

## Checked
2026-11-09. Confirmed against the Rails `Dockerfile.tt` template (stages, bundler env vars, jemalloc symlink and LD_PRELOAD, bootsnap precompile, SECRET_KEY_BASE_DUMMY, thrust CMD, non-root uid 1000), the Docker Official Image `php` documentation (extension helper scripts, PECL pinning and serial install, php.ini-production, OPcache, `--user`) and the Composer autoloader-optimization page (`-o`, `-a`).
Removed as unsupported by those sources: "Rails 7.1+ generates this", `BUNDLE_WITHOUT="development:test"`, `useradd -r` and the chown of db/log/storage/tmp, FastCGI port 9000 and nginx `fastcgi_pass`, FrankenPHP, `opcache.validate_timestamps=0`, `pm.max_children` sizing, the STOPSIGNAL claim, the composer-image vendor stage and Alpine apk steps, the Composer platform-check gotcha and the Laravel writable-directories note.
Method: documentation only; no commands were run.
