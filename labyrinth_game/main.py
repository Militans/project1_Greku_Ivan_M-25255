#!/usr/bin/env python3
from .constants import ROOMS
from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle


def process_command(game_state: dict, command: str) -> None:
    """
    Обрабатывает команду пользователя и вызывает нужное действие.

    Поддерживаемые команды:
    look, go <dir>, take <item>, use <item>, inventory, solve, help, quit/exit.

    :param game_state: Словарь состояния игры
    :param command: Команда, введенная пользователем
    :return: None
    """
    line = command.strip()
    if not line:
        return

    parts = line.split(maxsplit=1)
    cur_command = parts[0].lower()
    arg = parts[1].strip() if len(parts) == 2 else ""

    match cur_command:
        case "look":
            describe_current_room(game_state)
        case "go":
            if not arg:
                print("Куда идти? Пример: go north")
            else:
                move_player(game_state, arg.lower())
        case "take":
            if not arg:
                print("Что поднять? Пример: take torch")
            else:
                take_item(game_state, arg)
        case "use":
            if not arg:
                print("Что использовать? Пример: use torch")
            else:
                use_item(game_state, arg)
        case "inventory":
            show_inventory(game_state)
        case "help":
            show_help()
        case "solve":
            cur_room = game_state["current_room"]
            room_items = ROOMS[cur_room]["items"]
            if cur_room == "treasure_room" or "treasure_chest" in room_items:
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "quit" | "exit":
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда. Введите help, чтобы увидеть список команд.")
            show_help()


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")

    game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
    }

    describe_current_room(game_state)

    while not game_state["game_over"]:
        command_line = get_input("> ")
        process_command(game_state, command_line)


if __name__ == "__main__":
    main()
