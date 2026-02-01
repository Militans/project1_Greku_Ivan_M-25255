import math

from .constants import ROOMS
from .player_actions import get_input


def pseudo_random(seed: int, modulo: int) -> int:
    """
    Псевдослучайное число в диапазоне [0, modulo).
    :param seed: Число-источник (steps_taken).
    :param modulo: Верхняя граница диапазона (exclusive).
    :return: Целое число в [0, modulo)
    """
    if modulo <= 0:
        return 0

    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(math.floor(frac * modulo))


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


def show_help(commands: dict[str, str]) -> None:
    """
    Инструкция для применения команд

    :return: None
    """
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")


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

        normalized = answer.strip().lower()
        correct = str(puzzle[1]).strip().lower()

        alternatives = {
            "10": {"10", "десять"},
            "4": {"4", "четыре"},
        }
        acceptable = alternatives.get(correct, {correct})

        if normalized not in acceptable:
            print("Неверно. Попробуйте снова.")
            if cur_room == "trap_room":
                trigger_trap(game_state)
            return

        print("Правильно!")
        room["puzzle"] = None
        inventory = game_state["player_inventory"]

        if cur_room == "library":
            if "treasure_key" not in inventory:
                inventory.append("treasure_key")
                print("Вы получаете награду: treasure_key (добавлено в инвентарь).")
            return

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

    print("Сундук заперт.")
    choice = get_input("Ввести код? (да/нет) ").strip().lower()
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


def trigger_trap(game_state: dict) -> None:
    """
    Срабатывание ловушки.

    :param game_state: Словарь состояния игры.
    :return: None
    """
    print("Ловушка активирована! Пол стал дрожать...")

    inventory: list[str] = game_state["player_inventory"]
    seed = int(game_state.get("steps_taken", 0))

    if inventory:
        idx = pseudo_random(seed, len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}")
        return

    roll = pseudo_random(seed, 10)
    if roll < 3:
        print("Ловушка нанесла смертельный удар. Вы проиграли!")
        game_state["game_over"] = True
        return

    print("Вы чудом уцелели и выбрались из ловушки!")


def random_event(game_state: dict) -> None:
    """
    Случайные события после перемещения (низкая вероятность).
    :param game_state:
    :return: None
    """
    seed = int(game_state.get("steps_taken", 0))
    if pseudo_random(seed, 10) != 0:
        return

    event_type = pseudo_random(seed + 1, 3)
    current_room = game_state["current_room"]
    room = ROOMS[current_room]
    inventory: list[str] = game_state["player_inventory"]

    match event_type:
        case 0:
            print("Вы замечаете на полу монетку.")
            room["items"].append("coin")
        case 1:
            print("Вы слышите шорох где-то рядом...")
            if "sword" in inventory:
                print("Вы достаёте меч и отпугиваете существо.")
        case 2:
            if current_room == "trap_room" and "torch" not in inventory:
                print("Темно и опасно... вы наступили не туда!")
                trigger_trap(game_state)
        case _:
            return
