"""Асинхронное веб-приложение по доставке."""
import asyncio
import random
import string
from typing import Dict, Any
import jsonschema
from aiohttp import web
import aiosqlite
from jsonschema import validate
from requests import Response, Request
from JsonSchema import SCHEMA


def delivery_generate(pool: str = string.ascii_lowercase + string.digits) -> Dict:
    """Функция генерации id для заказа."""
    k = random.randint(2, 5)
    token = "".join(random.choices(pool, k=k))
    delivery_dict = {1: "обрабатывается", 2: "выполняется", 3: "доставлено"}
    return {"id": token, "status": delivery_dict[random.randint(1, 3)]}


async def try_make_db() -> None:
    """Функция для создания БД."""
    async with aiosqlite.connect('test.db') as db:
        await db.execute('''
    CREATE TABLE IF NOT EXISTS delivery_data(
    id VARCHAR(5) NOT NULL PRIMARY KEY UNIQUE,
    status VARCHAR(25) NOT NULL)''')
        await db.commit()


def input_validation(input_json: dict, schema: dict = SCHEMA) -> Any:
    """Функция для валидации json."""
    try:
        validate(input_json, schema)
        return input_json
    except jsonschema.exceptions.ValidationError:
        print("Невалидный json, попробуйте использовать другой")


routes = web.RouteTableDef()


@routes.get('/')
async def my_get(request: Request) -> web.Response:
    """Функция метода get."""
    async with aiosqlite.connect("test.db") as db:
        get_list_of_delivery = []
        cursors = await db.execute("SELECT * FROM delivery_data")
        rows = await cursors.fetchall()
        for i in rows:
            temp_id = {"id": i[0]}
            temp_status = {"status": i[1]}
            temp_list = {**temp_id, **temp_status}
            get_list_of_delivery.append(temp_list)
    return web.Response(text=str(get_list_of_delivery))


@routes.post('/')
async def my_post(request: Request) -> web.Response:
    """Фукнция метода post."""
    dict1 = await request.json()
    if input_validation(dict1):
        id = dict1["id"]
        status = dict1["status"]
        async with aiosqlite.connect("test.db") as db:
            cursors = await db.execute("SELECT id FROM delivery_data WHERE id = ? ", (id,))
            rows = await cursors.fetchone()
            try:
                if rows[0] == id:
                    await db.execute("UPDATE delivery_data SET status = ? WHERE id = ?", (status, id))
                await db.commit()
            except TypeError:
                await db.execute("INSERT INTO delivery_data (id,status) VALUES(?,?)",
                                 (id, status))
                await db.commit()
    return web.Response(text="Успешно добавлено")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(try_make_db())
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)
    asyncio.get_event_loop().close()
