"""Программа для расшифровки json файла и добавления значений в таблици."""
import sqlite3
import json
import jsonschema

DB = sqlite3.connect("data.db")
SQL = DB.cursor()


def create_tables() -> None:
    """Создание таблиц с данными."""
    SQL.execute(""" CREATE TABLE IF NOT EXISTS goods(
    id integer PRIMARY KEY AUTOINCREMENT,
    name varchar(250) NOT NULL,
    package_height float NOT NULL,
    package_width float NOT NULL
    ) """)

    SQL.execute(""" CREATE TABLE IF NOT EXISTS shops_goods(
    id integer PRIMARY KEY AUTOINCREMENT,
    id_good int NOT NULL,
    location varchar(250) NOT NULL,
    amount int NOT NULL,
    FOREIGN KEY (id_good) REFERENCES goods(id)
    ) """)
    DB.commit()


def load_json(name: str) -> dict:
    """Приведение json файла к типу dict."""
    with open(name, "r", encoding="utf-8") as file_json:
        file_json_dict = json.load(file_json)
        return file_json_dict


def validation_check(file: dict, schema: dict) -> bool:
    """Валидация json файла по загруженной схеме."""
    try:
        jsonschema.validate(file, schema)
        print("Correct")
    except jsonschema.exceptions.ValidationError:
        print("Validation error")
        return False
    return True


def get_data_from_json_and_input_to_db(input_json_file: dict) -> None:
    """Добавление данных в созданные таблицы."""
    id = input_json_file["id"]
    name = input_json_file["name"]
    width = input_json_file["package_params"]["width"]
    height = input_json_file["package_params"]["height"]

    SQL.execute(f""" SELECT * FROM goods WHERE id = {id} """)
    if SQL.fetchone() is None:
        SQL.execute(""" INSERT INTO goods (id, name, package_height, package_width)
                VALUES (?, ?, ?, ?)
                """, (id, name, width, height))
        DB.commit()
    else:
        SQL.execute(f""" UPDATE goods SET id = {id}, name = '{name}',
        package_height = {height}, package_width = {width} """)
        DB.commit()

    SQL.execute(f""" SELECT * FROM shops_goods WHERE id_good = {id} """)
    if SQL.fetchone() is None:
        for i in range(len(input_json_file["location_and_quantity"])):
            location = input_json_file["location_and_quantity"][i]["location"]
            quantity = input_json_file["location_and_quantity"][i]["amount"]
            SQL.execute(""" INSERT INTO shops_goods (id_good, location, amount)
                                        VALUES (?, ?, ?)
                                        """, (id, location, quantity))
            DB.commit()
    else:
        for i in range(len(input_json_file["location_and_quantity"])):
            location = input_json_file["location_and_quantity"][i]["location"]
            quantity = input_json_file["location_and_quantity"][i]["amount"]
            SQL.execute(f""" UPDATE shops_goods SET id_good = {id}, location = '{location}',
            amount = '{quantity}' WHERE id = {id+i} """)
            DB.commit()


def main(name_input_json_file: str, name_json_schema: str) -> None:
    """Основная функция, запускающая последовательность действий."""
    create_tables()
    input_json_file = load_json(name_input_json_file)
    json_schema = load_json(name_json_schema)
    validation_check(input_json_file, json_schema)
    get_data_from_json_and_input_to_db(input_json_file)


main("json_file.json", "goods.schema.json")
