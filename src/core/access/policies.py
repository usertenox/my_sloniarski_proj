from enum import StrEnum


class Policies(StrEnum):
    OWN_ONLY = "own_only"
    NOT_DELETED = "not_deleted"