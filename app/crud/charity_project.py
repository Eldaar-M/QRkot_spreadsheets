from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_charity_project = await session.execute(
            select(self.model).where(
                self.model.name == charity_project_name
            )
        )
        db_charity_project = db_charity_project.scalars().first()
        return db_charity_project

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,

    ) -> list[CharityProject]:
        closed_projects = await session.execute(
            select(CharityProject)).where(
                CharityProject.fully_invested).order_by(
                extract('year', CharityProject.close_date) -
                extract('year', CharityProject.create_date),
                extract('month', CharityProject.close_date) -
                extract('month', CharityProject.create_date),
                extract('day', CharityProject.close_date) -
                extract('day', CharityProject.create_date),
        )
        closed_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
