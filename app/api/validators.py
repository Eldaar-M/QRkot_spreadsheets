from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate
from fastapi import HTTPException


PROJECT_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_ID_EXISTS = 'Проекта с указанным id не существует!'
EDIT_DELTE_CLOSED_PROJECT = 'Нельзя удалять или редактировать закрытый проект!'
FULL_AMOUNT_VALUE = 'Нелья установить значение full_amount меньше уже вложенной суммы.'
DELETE_INVESTMENTS = 'В проект были внесены средства, не подлежит удалению!'


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name,
        session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_EXISTS
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id,
        session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_ID_EXISTS
        )
    return charity_project


def check_charity_project_close_date(
        charity_project: CharityProject,
) -> CharityProject:
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=EDIT_DELTE_CLOSED_PROJECT
        )


async def check_charity_project_before_edit(
        project_id: int,
        charity_project_in: CharityProjectUpdate,
        session: AsyncSession
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        project_id=project_id,
        session=session
    )
    new_full_amount = charity_project_in.full_amount
    if (new_full_amount and
            charity_project.invested_amount > new_full_amount):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FULL_AMOUNT_VALUE
        )
    check_charity_project_close_date(
        charity_project=charity_project
    )
    await check_name_duplicate(
        charity_project_name=charity_project_in.name,
        session=session
    )
    return charity_project


def charity_project_fully_invested(
        charity_project: CharityProject
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=EDIT_DELTE_CLOSED_PROJECT
        )


async def check_charity_project_before_delete(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        project_id=project_id,
        session=session
    )

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=DELETE_INVESTMENTS
        )
    charity_project_fully_invested(charity_project)

    return charity_project
