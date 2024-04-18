# Проект QRKot — Благотворительный фонд поддержки котиков
## Технологии

- Python
- FastAPI

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:Eldaar-M/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
## Как запустить проект:
Примените миграции:
```
alembic upgrade head
```
В коревой директории проекта введите:
```
uvicorn app.main:app --reload
```
## API:
[Swagger](http://127.0.0.1:8000/swagger)

[ReDoc](http://127.0.0.1:8000/redoc)
### Автор 
[Эльдар Магомедов](https://github.com/Eldaar-M)