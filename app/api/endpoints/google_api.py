from http import HTTPStatus
from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    spreadsheets_create, set_user_permissions, spreadsheets_update_value
)


SPREADSHEETS_UPDATE_ERROR = 'Ошибка при обновлении документа: {error}'

router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """Только для суперюзеров."""
    closed_projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id, spreadsheet_url = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            closed_projects,
            wrapper_services
        )
    except ValueError as error:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            SPREADSHEETS_UPDATE_ERROR.format(error=error)
        )
    return spreadsheet_url
