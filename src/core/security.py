from datetime import UTC, datetime, timedelta
from typing import NoReturn
import hmac
import hashlib
from pwdlib import PasswordHash
from collections.abc import Mapping

import jwt
from jwt.exceptions import InvalidTokenError

from src.core.config import settings
from src.utils.errors import InvalidCredentials, InvalidJWT
from src.core.enums import ProjectRole
from src.core.access.permissions import Permissions
from src.core.access.policies import Policies

from uuid import UUID, uuid4
from enum import StrEnum
from dataclasses import dataclass


@dataclass(frozen=True)
class RefreshTokenData:
    token: str
    jti: UUID
    expires_at: datetime


@dataclass(frozen=True)
class DecodedRefreshPayload:
    jti: UUID
    user_id: UUID


class TokenType(StrEnum): # наследование гарантирует, что каждый элемент - строка
    ACCESS = "access"
    REFRESH = "refresh"


password_hash = PasswordHash.recommended() # Argon2 - долгий алгоритм для пароля

DUMMY_PASSWORD_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4"
    "$Q0GSQhetDkrX4go74UuOCg"
    "$lBCP8jNj8Mh8GaSklZWOXKTZoKwZoEb0qKtZkL2sVZ4"
)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def verify_dummy_password(password: str) -> NoReturn:
    verify_password(password, DUMMY_PASSWORD_HASH)
    raise InvalidCredentials()


def create_access_token(
        user_id: UUID,
        project_id: UUID | None = None,
        is_owner: bool = False,
        role: ProjectRole | None = None,
        permissions: frozenset[Permissions] = frozenset(),
        policies: Mapping[Permissions, tuple[Policies, ...]] | None = None,
    ) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    
    payload = {
        "sub": str(user_id), 
        "exp": expires_at,
        "type": TokenType.ACCESS.value,
        "project_id": str(project_id) if project_id else None,

        "is_owner": is_owner,
        "role": role.value if role else None,

        # не дописал
    }
# pyjwt сам преобразует datetime в JWT NumericDate — Unix timestamp
# То есть ты передаёшь:
# datetime
# а внутри JWT оно станет числом:
# "exp": 1234567890

    return jwt.encode(
        payload, 
        settings.secret_key, 
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> UUID: # не переделал
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub", "type"]},
        ) # токен подписан известным ключом, но не гарантирует, что sub не скомпрометирован

        token_type = payload.get("type") 
        if token_type != TokenType.ACCESS.value:
            raise InvalidJWT()

        subject = payload.get("sub") # тут мб не строка и тогда придется ловить ошибку AttributeError или TypeError
        if subject is None or not isinstance(subject, str):
            raise InvalidJWT()

        return UUID(subject)

    except (InvalidTokenError, ValueError):
        raise InvalidJWT() 
    

def create_refresh_token(user_id: UUID) -> RefreshTokenData:
    expires_at = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)
    jti = uuid4()

    payload = {
        "sub": str(user_id),
        "type": TokenType.REFRESH.value,
        "jti": str(jti),
        "exp": expires_at,
    }

    refresh_token = jwt.encode(
        payload,
        key=settings.secret_key,
        algorithm=settings.algorithm,
    )

    return RefreshTokenData(
        token=refresh_token,
        jti=jti,
        expires_at=expires_at,
    )


def decode_refresh_token(token: str) -> DecodedRefreshPayload:

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub", "type", "jti"]}, # verify_exp в PyJWT уже включено
        )

        token_type = payload.get("type") 
        if token_type != TokenType.REFRESH.value:
            raise InvalidJWT()

        sub_uid = payload.get("sub")
        jti = payload.get('jti') 
        if (
            sub_uid is None or not isinstance(sub_uid, str) 
            or jti is None or not isinstance(jti, str)
        ):
            raise InvalidJWT()

        return DecodedRefreshPayload(
            jti=UUID(jti),
            user_id=UUID(sub_uid),
        )

    except (InvalidTokenError, ValueError):
        raise InvalidJWT()
    

def hash_refresh_token(token: str) -> str:
    return hmac.new(
        settings.secret_key.encode("utf-8"), # -> b"\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87" 
        # -> [208, 186, 208, 187, 209, 142, 209, 135]
        token.encode("utf-8"), 
        digestmod=hashlib.sha256
    ).hexdigest()


def verify_refresh_token_hash(token: str, token_hash: str) -> bool:
    return hmac.compare_digest(hash_refresh_token(token), token_hash)