#!/usr/bin/env python3
from .player_actions import get_input, show_inventory, move_player, take_item, use_item
from .utils import describe_current_room


def process_command(game_state: dict, command: str) -> None:
    """

    :param game_state:
    :param command:
    :return:
    """
    line = command.strip().split()
    cur_command = line[0]
    args = line[1:] if len(line) else ""
    pass



def main():
    print("Добро пожаловать в Лабиринт сокровищ!")

    game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
    }

    describe_current_room(game_state)

    while True:
        get_input()

if __name__ == "__main__":
    main()
