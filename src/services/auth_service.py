from uuid import UUID

from src.repositories.user_repo import UserRepository
from src.schemas.auth import (
    RegisterRequest, 
    AuthResponse, 
    UserResponse, 
    LoginRequest, 
    RefreshRequest, 
    TokenPairResponse,
)
from src.utils.errors import InvalidCredentials, UserAlreadyExists, InvalidJWT
from src.core.security import (
    hash_password,
    create_access_token,
    verify_dummy_password,
    verify_password,
    create_refresh_token,
    hash_refresh_token,
    decode_refresh_token,
    verify_refresh_token_hash,
)
from src.models.user import User
from src.repositories.refresh_repo import RefreshTokenRepo
from datetime import datetime, UTC

class AuthService:

    def __init__(self, user_repo: UserRepository, ref_token_repo: RefreshTokenRepo):
        self.user_repo = user_repo
        self.ref_token_repo = ref_token_repo


    async def _give_tokens(self, user: User) -> AuthResponse:

        access_token = create_access_token(user_id=user.id)

        ref_tok_data = create_refresh_token(user_id=user.id)

        await self.ref_token_repo.save_ref_token(
            ref_tok_data.jti, 
            user_id=user.id, 
            token_hash=hash_refresh_token(ref_tok_data.token),
            expires_at=ref_tok_data.expires_at,
            )

        return AuthResponse(
            access_token=access_token,
            refresh_token=ref_tok_data.token,
            token_type="bearer",
            user = UserResponse.model_validate(user)
        )


    async def register(self, request: RegisterRequest) -> AuthResponse:

        existing_user = await self.user_repo.get_by_email(str(request.email))

        if existing_user:
            raise UserAlreadyExists()
        
        user = await self.user_repo.create(
            username=request.username,
            email=str(request.email),
            password_hash=hash_password(request.password),
        )

        return await self._give_tokens(user)
    

    async def login(self, request: LoginRequest) -> AuthResponse:
        
        existing_user = await self.user_repo.get_by_email(str(request.email))

        if existing_user is None:
            verify_dummy_password(request.password)
        
        if not verify_password(request.password, existing_user.password_hash):
            raise InvalidCredentials()
        
        return await self._give_tokens(existing_user)


    async def refresh(self, refresh_token: str) -> TokenPairResponse:

        refresh_data = decode_refresh_token(refresh_token)

        db_ref_token = await self.ref_token_repo.get_by_jti_for_update(refresh_data.jti)

        if db_ref_token is None:
            raise InvalidJWT()

        if (
            db_ref_token.user_id != refresh_data.user_id
            or not verify_refresh_token_hash(
                refresh_token,
                db_ref_token.token_hash,
            )
            or db_ref_token.revoked_at is not None
        ):
            raise InvalidJWT() # уязвимость гонки токенов 

        await self.ref_token_repo.revoke(db_ref_token, datetime.now(UTC))

        new_ref_tok_data = create_refresh_token(db_ref_token.user_id)

        await self.ref_token_repo.save_ref_token(
            new_ref_tok_data.jti,
            db_ref_token.user_id,
            hash_refresh_token(new_ref_tok_data.token),
            expires_at=new_ref_tok_data.expires_at,
        )

        return TokenPairResponse(
            access_token=create_access_token(db_ref_token.user_id),
            refresh_token=new_ref_tok_data.token,
        )



    async def logout(self, refresh_token: str) -> None:
        payload = decode_refresh_token(refresh_token)

        db_ref_tok = await self.ref_token_repo.get_by_jti_for_update(jti=payload.jti)

        if db_ref_tok is None:
            raise InvalidJWT()

        if (payload.user_id != db_ref_tok.user_id
            or not verify_refresh_token_hash(refresh_token, db_ref_tok.token_hash)
            or db_ref_tok.revoked_at is not None
        ):
            raise InvalidJWT()

        await self.ref_token_repo.revoke(refresh_token=db_ref_tok, revoked_at=datetime.now(UTC))


    async def logout_all(self, user_id: UUID) -> None:

        await self.ref_token_repo.revoke_all_by_user_id(user_id=user_id, revoked_at=datetime.now(UTC))



