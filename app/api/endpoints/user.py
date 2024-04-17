from http import HTTPStatus

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate
from fastapi import APIRouter, HTTPException


AUTH = 'auth'
DELETE_USER_PHRASE = "Удаление пользователей запрещено!"
USERS = 'users'


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f'/{AUTH}/jwt',
    tags=[AUTH],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=f'/{AUTH}',
    tags=[AUTH],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=f'/{USERS}',
    tags=[USERS],
)


@router.delete(
    f'/{USERS}/{id}',
    tags=[USERS],
    deprecated=True
)
def delete_user(id: str):
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail=DELETE_USER_PHRASE
    )
