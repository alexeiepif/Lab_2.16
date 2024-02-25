#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Решить индивидуальное задание лабораторной работы 2.6,
# оформив каждую команду в виде отдельной функции.

import bisect
import re
import sys
import json
from jsonschema import validate, ValidationError


def get_route():
    """
    Запросить данные о маршруте.
    """
    start = input("Введите начальный пункт: ")
    end = input("Введите конечный пункт: ")
    count = int(input("Введите номер маршрута: "))

    return {
        "начальный пункт": start,
        "конечный пункт": end,
        "номер маршрута": count,
    }


def display_routes(routes):
    """
    Отобразить список маршрутов.
    """
    if routes:
        line = "+-{}-+-{}-+-{}-+".format("-" * 30, "-" * 20, "-" * 8)
        print(line)
        print("| {:^30} | {:^20} | {:^8} |".format("Начало", "Конец", "Номер"))
        print(line)
        for route in routes:
            print(
                "| {:<30} | {:<20} | {:>8} |".format(
                    route.get("начальный пункт", ""),
                    route.get("конечный пункт", ""),
                    route.get("номер маршрута", ""),
                )
            )
        print(line)
    else:
        print("Список маршрутов пуст.")


def select_routes(routes, name_punct):
    """
    Выбрать маршруты с заданным пунктом отправления или прибытия.
    """
    selected = []
    for route in routes:
        if (
            route["начальный пункт"].lower() == name_punct
            or route["конечный пункт"].lower() == name_punct
        ):
            selected.append(route)

    return selected


def save_routes(file_name, routes):
    """
    Сохранить все маршруты в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w") as file_out:
        # Записать данные из словаря в формат JSON и сохранить их
        # в открытый файл.
        json.dump(routes, file_out, ensure_ascii=False, indent=4)


def load_routes(file_name):
    """
    Загрузить все маршруты из файла JSON.
    """
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "начальный пункт": {"type": "string"},
                "конечный пункт": {"type": "string"},
                "номер маршрута": {"type": "integer"},
            },
            "required": ["начальный пункт", "конечный пункт", "номер маршрута"],
        },
    }
    # Открыть файл с заданным именем и прочитать его содержимое.
    with open(file_name, "r") as file_in:
        data = json.load(file_in)  # Прочитать данные из файла

    try:
        # Валидация
        validate(instance=data, schema=schema)
        print("JSON валиден по схеме.")
    except ValidationError as e:
        print(f"Ошибка валидации: {e.message}")
    return data


def main():
    """
    Главная функция программы.
    """
    routes = []
    while True:
        command = input(">>> ").lower()

        match command:
            case "exit":
                break

            case "add":
                route = get_route()
                if route not in routes:
                    bisect.insort(
                        routes,
                        route,
                        key=lambda item: item.get("номер маршрута"),
                    )
                else:
                    print("Данный маршрут уже добавлен.")

            case "list":
                display_routes(routes)

            case _ if (m := re.match(r"(select|save|load) (.+)", command)):
                match m.group(1):
                    case "select":
                        name_punct = m.group(2)
                        selected = select_routes(routes, name_punct)
                        display_routes(selected)
                    case "save":
                        file_name = m.group(2)
                        save_routes(file_name, routes)
                    case "load":
                        file_name = m.group(2)
                        routes = load_routes(file_name)

            case "help":
                print("Список команд:\n")
                print("add - добавить маршрут;")
                print("list - вывести список маршрутов;")
                print(
                    "select <название пункта> - "
                    + "запросить маршруты, которые начинаются\n"
                    + "или заканчиваются в данном пункте;"
                )
                print("help - отобразить справку;")
                print("load  <filename> - загрузить данные из файла;")
                print("save  <filename> - сохранить данные в файл;")
                print("exit - завершить работу с программой.")

            case _:
                print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == "__main__":
    main()
