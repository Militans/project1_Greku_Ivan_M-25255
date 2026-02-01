def show_inventory(game_state: dict) -> None:
    """
    Выводит содержимое инвентаря игрока (ключ "player_inventory").

    :param game_state: Словарь состояния игры.
    :return: None
    """
    inventory = game_state["player_inventory"]

    if not inventory:
        print("Инвентарь пуст")
        return

    print("Инвентарь:")
    for item in inventory:
        print(f" - {item}")


def get_input(prompt: str = "> ") -> str:
    """
    Считывает ввод пользователя.

    При KeyboardInterrupt или EOFError печатает сообщение и возвращает "quit".

    :param prompt: Строка приглашения ко вводу.
    :return: Введённая команда (без пробелов по краям) или "quit".
    """
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: dict, direction: str) -> None:
    """
    Перемещает игрока в указанном направлении, если выход существует.

    Если в текущей комнате есть выход direction, обновляет:
    - game_state["current_room"]
    - game_state["steps_taken"]

    Затем печатает описание новой комнаты через utils.describe_current_room().
    Если выхода нет - печатает сообщение об ошибке.

    :param game_state: Словарь состояния игры.
    :param direction: Направление движения (north/south/east/west).
    :return: None
    """
    from .constants import ROOMS
    from .utils import describe_current_room, random_event

    current_room = game_state["current_room"]
    room = ROOMS[current_room]
    exits = room["exits"]

    next_room = exits.get(direction)
    if not next_room:
        print("Нельзя пойти в этом направлении.")
        return

    if next_room == "treasure_room":
        inventory: list[str] = game_state["player_inventory"]
        if "rusty_key" in inventory:
            print(
                "Вы используете найденный ключ, чтобы открыть путь в комнату "
                "сокровищ."
            )
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state["current_room"] = next_room
    game_state["steps_taken"] += 1
    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    """
    Команда для перемещения предмета из комнаты в инвентарь игрока.

    :param game_state: Словарь состояния игры.
    :param item_name: Название предмета.
    :return: None
    """
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    from .constants import ROOMS

    current_room = game_state["current_room"]
    room = ROOMS[current_room]
    items = room["items"]

    if item_name not in items:
        print("Такого предмета здесь нет.")
        return

    items.remove(item_name)
    game_state["player_inventory"].append(item_name)
    print(f"Вы подняли: {item_name}")


def use_item(game_state: dict, item_name: str) -> None:
    """
    Использование предмета, имеющегося у игрока
    :param game_state:
    :param item_name:
    :return:
    """
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case "torch":
            print("Вы зажигаете факел. Вокруг становится заметно светлее.")
        case "sword":
            print("Вы берёте меч в руку. Вы чувствуете уверенность и защиту.")
        case "bronze_box":
            if "rusty_key" not in inventory:
                inventory.append("rusty_key")
                print("Вы открываете бронзовую шкатулку и находите внутри rusty_key!")
            else:
                print("Шкатулка уже пуста - rusty_key у вас.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")

