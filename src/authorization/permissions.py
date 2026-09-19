from enum import StrEnum


class Permission(StrEnum):
    PROJECT_READ = "project.read"
    PROJECT_UPDATE = "project.update"
    PROJECT_DELETE = "project.delete"

    MEMBER_READ = "member.read"
    MEMBER_ADD = "member.add"
    MEMBER_UPDATE_ROLE = "member.update_role"
    MEMBER_REMOVE = "member.remove"

    DOCUMENT_CREATE = "document.create"
    DOCUMENT_READ = "document.read"
    DOCUMENT_UPDATE = "document.update"
    DOCUMENT_DELETE = "document.delete"
