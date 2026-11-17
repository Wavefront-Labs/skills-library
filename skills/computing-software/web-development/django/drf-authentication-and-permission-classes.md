---
id: computing-software.web-development.django.drf-authentication-and-permission-classes
name: drf-authentication-and-permission-classes
category: computing-software
field: web-development
product: django
tags: [django, drf-permissions, drf-authentication, django-rest-framework, object-permissions, jwt, token-auth, python, web-development]
level: practitioner
status: docs-checked
description: "Securing DRF APIs: authentication classes (session, token, JWT), default permission settings, custom has_permission/has_object_permission, and queryset scoping."
sources:
  - https://www.django-rest-framework.org/api-guide/authentication/
  - https://www.django-rest-framework.org/api-guide/permissions/
  - https://django-rest-framework-simplejwt.readthedocs.io/
  - https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
  - https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DRF authentication and permission classes

**Goal:** every endpoint authenticated by default, with object-level authorisation that can't be bypassed.

## 1. Secure defaults
```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",     # same-site browser clients (enforces CSRF)
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # or TokenAuthentication for simple server clients
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}
```
The DRF default is `AllowAny` - forgetting `permission_classes` on a view exposes it. Set `IsAuthenticated` globally and opt out explicitly with `AllowAny`.

## 2. Authentication choices
- Session: browser SPA on the same site; CSRF token required for unsafe methods.
- `TokenAuthentication`: one static token per user, no expiry - fine for internal service clients; prefer `knox` or JWT for expiring tokens.
- SimpleJWT: short access token (`ACCESS_TOKEN_LIFETIME` defaults to 5 minutes) + refresh with rotation and blacklist (`ROTATE_REFRESH_TOKENS`, `BLACKLIST_AFTER_ROTATION`; the blacklist needs `rest_framework_simplejwt.token_blacklist` in `INSTALLED_APPS`).
Unauthenticated requests get 401 when the first auth class provides a `WWW-Authenticate` header, else 403.

## 3. Custom permissions
```python
class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner_id == request.user.id
```
`has_object_permission` runs only when the view calls `get_object()` / `check_object_permissions()` (generic views do on retrieve/update/destroy). It does **not** filter list endpoints and is not applied when creating objects.

## 4. Scope the queryset (the real fix for BOLA/IDOR)
```python
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```
Objects outside the queryset 404 automatically. Never accept `owner` from the request body (make it `read_only`).

## 5. Composition and per-action rules
Permissions combine with `&`, `|`, `~`: `permission_classes = [IsAuthenticated & (IsAdminUser | IsOwner)]`. Per action:
```python
def get_permissions(self):
    if self.action == "destroy": return [IsAdminUser()]
    return super().get_permissions()
```
`DjangoModelPermissions` maps HTTP methods to model perms (`add/change/delete`).

## Verify
- [ ] Test: user B requesting user A's object gets 404, and B's list excludes it.
- [ ] Every view without explicit permissions requires auth (hit endpoints anonymously in a test loop).
- [ ] JWT access tokens expire; refresh rotation works and old refresh tokens are rejected.

## Checked
Date: 2026-10-25. Documentation: Django REST framework docs source (encode/django-rest-framework main, commit of 2026-10-14: authentication, permissions, settings), SimpleJWT docs source (settings), OWASP API Security repository (BOLA page exists).
Confirmed: default `DEFAULT_PERMISSION_CLASSES` is `AllowAny`, 401 versus 403 depends on the first authentication class and `WWW-Authenticate`, SessionAuthentication CSRF requirement, TokenAuthentication versus Knox expiry, permission composition with `&`, `|`, `~`, `DjangoModelPermissions`, object permissions run through `get_object()` and are not applied on create, SimpleJWT rotation and blacklist settings and 5-minute default.
Corrected or removed: the "5-15 min" range (replaced by the documented default), the unsupported cookie-versus-localStorage advice, and the missing blacklist-app and create-time caveats.
Method: documentation only; no commands were run.
