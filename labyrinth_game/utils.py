from .constants import ROOMS
from .player_actions import get_input


def describe_current_room(game_state: dict) -> None:
    """
    Печатает описание текущей комнаты.
    Выводит:
    - заголовок вида "== ROOMNAME ==" (верхний регистр)
    - описание комнаты
    - список предметов, если есть
    - список выходов
    - подсказку про загадку, если puzzle не None

    :param game_state: Словарь состояния игры (ключ "current_room" обязателен).
    :return: None
    """
    current_room = game_state["current_room"]
    room = ROOMS[current_room]

    print(f"\n== {current_room.upper()} ==")
    print(room["description"])

    items = room["items"]
    if items:
        print("Заметные предметы:")
        for item in items:
            print(f" - {item}")

    exits = room["exits"]
    print("Выходы:")
    for direction in exits:
        print(f" - {direction}")

    if room["puzzle"] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")



def show_help() -> None:
    """
    Инструкция для применения команд

    :return: None
    """
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")


def solve_puzzle(game_state: dict) -> None:
    """
    Решает загадку в текущей комнате.

    Если puzzle нет - сообщает об этом. Иначе задаёт вопрос, принимает ответ через
    get_input("Ваш ответ: "). При правильном ответе убирает puzzle из комнаты и выдаёт
    награду (например, "treasure_key" в player_inventory).
    При ошибке просит попробовать снова.

    :param game_state: Словарь состояния игры.
    :return: None
    """
    cur_room = game_state["current_room"]
    room = ROOMS[cur_room]
    puzzle = room["puzzle"]
    if puzzle is None:
        print("Загадок здесь нет.")
        return
    else:
        print(puzzle[0])
        answer = get_input("Ваш ответ: ")
        if answer in {"quit", "exit"}:
            game_state["game_over"] = True
            return
        if answer.strip().lower() != puzzle[1].strip().lower():
            print("Неверно. Попробуйте снова.")
            return
        else:
            print("Правильно!")
            room["puzzle"] = None
            inventory = game_state["player_inventory"]
            if cur_room == "library":
                if "treasure_key" not in inventory:
                    inventory.append("treasure_key")
                    print("Вы получаете награду: treasure_key (добавлено в инвентарь).")
                    return
            else:
                inventory.append("gem")
                return


def attempt_open_treasure(game_state: dict) -> None:
    """
    Пытается открыть сундук в комнате сокровищ.

    Если есть "treasure_key" - открывает сундук, убирает "treasure_chest" из комнаты,
    печатает победу и ставит game_over=True. Если ключа нет - предлагает ввести код и
    сверяет его с ответом puzzle комнаты.

    :param game_state: Словарь состояния игры.
    :return: None
    """
    cur_room = game_state["current_room"]
    room = ROOMS[cur_room]
    items = room["items"]
    if "treasure_chest" not in items:
        print("Сундука здесь нет.")
        return
    inventory = game_state["player_inventory"]
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        inventory.remove("treasure_key")
        items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    choice = get_input("Сундук заперт. Ввести код? (да/нет) ").strip().lower()
    if choice == "quit":
        game_state["game_over"] = True
        return
    if choice not in {"да", "д", "yes", "y"}:
        print("Вы отступаете от сундука.")
        return

    correct_answer = str(room["puzzle"][1]).strip().lower()
    answer = get_input("Код: ").strip().lower()
    if answer in {"quit", "exit"}:
        game_state["game_over"] = True
        return
    if answer == correct_answer:
        print("Код верный. Замок щёлкает. Сундук открыт!")
        items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    print("Неверный код.")
