# Transfer notes — 2026-09-17

Current project snapshot for moving to another machine.

## Authorization work already included

- `Principal` and token-only authentication dependency are present.
- `ProjectAccessResolver` builds `ProjectAccessContext` from project ownership/current membership.
- `Permission` defines project/member/document actions.
- `ROLE_PERMISSIONS` maps `ProjectRole` to permissions.
- `ProjectScope` carries the current project boundary.
- `AuthorizationDecision` carries the granted permission + scope.
- `ProjectAuthorizer` combines ReBAC context + RBAC permission and always returns a project-scoped decision.

## Next authorization step

Implement the repository-side policy layer (`apply_policies` / `apply_policy`) so an `AuthorizationDecision` can add row-level constraints to SQL statements. Do not bypass `ProjectScope` for `ProjectRole.ADMIN`: project admins are scoped to their current project.

## Setup on the new machine

1. Copy `.env.example` to `.env` and fill local secrets/DB settings.
2. Install `uv` if needed.
3. Run `uv sync`.
4. Apply migrations as appropriate for the local database.
5. Run `uv run pytest -v`.

The archive intentionally does not include a real `.env` or local secrets.
