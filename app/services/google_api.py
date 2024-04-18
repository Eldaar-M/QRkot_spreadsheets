from datetime import datetime
from copy import deepcopy

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_ROW_COUNT = 100
SPREADSHEET_COLUMN_COUNT = 11


SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет от {now_date_time}',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=SPREADSHEET_ROW_COUNT,
            columnCount=SPREADSHEET_COLUMN_COUNT,
        )
    ))]
)

TABLE_HEADER = [
    ['Отчёт от', ],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
MANY_ROWS_ERROR = (
    'Превышен лимит строк: {value}' +
    f'Максимально: {SPREADSHEET_ROW_COUNT}'
)
SPREADSHEET_COLUMN_COUNT = (
    'Превышен лимит столбцов: {value}' +
    f'Максимально: {SPREADSHEET_COLUMN_COUNT}'
)


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body: dict = SPREADSHEET_BODY
) -> str:
    spreadsheet_body_copy = deepcopy(spreadsheet_body)
    spreadsheet_body_copy['properties']['title'].format(
        now_date_time=datetime.now().strftime(FORMAT)
    )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body_copy)
    )
    spreadsheet_id = response['spreadsheetId']
    spreadsheet_url = response['spreadsheetUrl']
    return spreadsheet_id, spreadsheet_url


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        closed_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_header = deepcopy(TABLE_HEADER)
    table_values = [
        *table_header[0].append(datetime.now().strftime(FORMAT)),
        *[list(map(
            str, [
                project['name'],
                project['close_date '] - project['create_date '],
                project['description']
            ])) for project in closed_projects],
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    row_count = len(table_values)
    column_count = max(map(len, table_values))

    if SPREADSHEET_ROW_COUNT < row_count:
        raise ValueError(MANY_ROWS_ERROR.format(
            value=row_count
        ))
    if SPREADSHEET_COLUMN_COUNT < column_count:
        raise ValueError(MANY_ROWS_ERROR.format(
            value=column_count
        ))
    response = await wrapper_services.as_service_account( # noqa
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{row_count}C{column_count}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
