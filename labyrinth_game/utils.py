from .constants import ROOMS


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
