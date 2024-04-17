from app.api.endpoints import (
    charity_project_router, donation_router, google_api_router, user_router
)
from fastapi import APIRouter

main_router = APIRouter()

DONATION_PREFIX = '/donation'
DONATION_TAGS = 'Donations'
CHARITY_PREFIX = '/charity_project'
CHARITY_TAGS = '/charity_project'
GOOGLE_PREFIX = '/google'
GOOGLE_TAGS = 'Google'


main_router.include_router(
    charity_project_router,
    prefix=CHARITY_PREFIX,
    tags=[CHARITY_TAGS]
)
main_router.include_router(
    donation_router,
    prefix=DONATION_PREFIX,
    tags=[DONATION_TAGS]
)
main_router.include_router(
    google_api_router,
    prefix=GOOGLE_PREFIX,
    tags=[GOOGLE_TAGS]
)
main_router.include_router(user_router)
