---
id: computing-software.web-development.rails.validations-and-errors
name: validations-and-errors
category: computing-software
field: web-development
product: rails
tags: [rails, rails-validations, active-model-errors, custom-validators, validation-contexts, ruby, web-development]
level: practitioner
status: docs-checked
description: "Validating Rails models: built-in validators, conditional and contextual validations, custom validators, errors API and i18n messages, and pairing with DB constraints."
sources:
  - https://guides.rubyonrails.org/active_record_validations.html
  - https://guides.rubyonrails.org/i18n.html#translations-for-active-record-models
  - https://api.rubyonrails.org/classes/ActiveModel/Errors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validations and errors

**Goal:** user-friendly validation errors at the model layer, with the database enforcing the same rules underneath.

## 1. Built-ins
```ruby
class User < ApplicationRecord
  normalizes :email, with: ->(e) { e.strip.downcase }
  validates :email, presence: true, uniqueness: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :name, length: { maximum: 100 }
  validates :age, numericality: { only_integer: true, greater_than_or_equal_to: 13 }, allow_nil: true
  validates :terms, acceptance: true, on: :create
  validates :role, inclusion: { in: %w[member admin] }
  validates :password, confirmation: true, length: { minimum: 12 }, if: :password_digest_changed?
end
```
`belongs_to` association presence is validated by default; use `optional: true` deliberately.

## 2. When validations run
`save`, `create`, `update`, `valid?` run them. The guide lists these as skipping validations: `decrement!`, `decrement_counter`, `increment!`, `increment_counter`, `insert`, `insert!`, `insert_all`, `insert_all!`, `toggle!`, `touch`, `touch_all`, `update_all`, `update_attribute`, `update_attribute!`, `update_column`, `update_columns`, `update_counters`, `upsert`, `upsert_all` and `save(validate: false)`. So validations alone can't guarantee integrity.

## 3. Database backing
The guide warns that `uniqueness` does not create a database constraint, so two connections can create two records with the same value; add a unique index (with `:scope`, a unique index on both columns). `ActiveRecord::RecordNotUnique` is what the database raises when the index is hit, so handle it:
```ruby
add_index :users, :email, unique: true
rescue ActiveRecord::RecordNotUnique
  user.errors.add(:email, :taken); render :new, status: :unprocessable_entity
```
Pair `presence` with `null: false`, inclusion with a check constraint or enum.

## 4. Custom validation
```ruby
validate :ends_after_start
def ends_after_start
  return if ends_at.blank? || starts_at.blank?
  errors.add(:ends_at, :after_start, message: "must be after the start time") if ends_at <= starts_at
end
# reusable: ActiveModel::EachValidator implements validate_each(record, attribute, value)
class EmailValidator < ActiveModel::EachValidator
  def validate_each(record, attribute, value)
    unless URI::MailTo::EMAIL_REGEXP.match?(value)
      record.errors.add attribute, (options[:message] || "is not an email")
    end
  end
end
validates :email, presence: true, email: true
```

## 5. Contexts
`validates :x, presence: true, on: :publish` then `article.valid?(:publish)` / `article.save(context: :publish)` for workflow-specific rules (draft vs published); the guide's example uses `valid?(:account_setup)` and `save(context: :account_setup)`.

## 6. Errors API
```ruby
user.errors.full_messages            # ["Email has already been taken"]
user.errors[:email]                  # ["has already been taken"]
user.errors.added?(:email, :taken)   # check by type in tests
user.errors.where(:email).map(&:type)   # error objects; where(:attr, :type) filters further
```
Translate in `config/locales/en.yml` under `activerecord.errors.models.user.attributes.email.taken` (the I18n guide's lookup is `activerecord.errors.models.[model_name].attributes.[attribute_name].[key]`). Re-render the form with `status: :unprocessable_entity` (422) as the Rails guides do.

## Verify
- [ ] Model specs cover each validation with valid and invalid cases (`errors.added?`).
- [ ] Every uniqueness validation has a unique index.
- [ ] Failed form submissions return 422 and show field errors.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Active Record validations and I18n guides and the v8.1.4 ActiveModel::Errors source. Confirmed: built-in validators and options (`presence`, `uniqueness`, `acceptance`, `confirmation`, `numericality` with `only_integer`/`greater_than_or_equal_to`, `inclusion`, `format` with `URI::MailTo::EMAIL_REGEXP`, `allow_nil`), `belongs_to` presence by default, the list of methods that skip validations, the uniqueness-needs-unique-index warning, `EachValidator#validate_each`, validation contexts with `valid?(:ctx)` and `save(context:)`, `errors.full_messages`, `errors[:attr]`, `errors.where(:attr, :type)` and the I18n error message lookup path. Removed the Rails 5 and 7.1 version gates and the custom URL validator (replaced with the guide's EachValidator example).

Method: documentation only; no commands were run.
