# Лабиринт сокровищ

Консольная игра на Python 3.11. Игрок исследует лабиринт комнат, собирает предметы,
решает загадки, сталкивается со случайными событиями и ловушками. Цель - открыть
сундук с сокровищами в комнате `treasure_room`.

## Требования

- Python 3.11
- Poetry 2.x

## Установка

Через Makefile:

```bash
make install
```

Или напрямую через Poetry:

```bash
poetry install
```

## Запуск

Через Makefile:

```bash
make project
```

Или напрямую через Poetry:

```bash
poetry run project
```

## Команды игры

- `look` - осмотреть текущую комнату
- `go <direction>` - перейти в направлении (`north/south/east/west`)
- `north`, `south`, `east`, `west` - перейти без команды `go`
- `take <item>` - поднять предмет
- `use <item>` - использовать предмет из инвентаря
- `inventory` - показать инвентарь
- `solve` - решить загадку в комнате / попытаться открыть сундук
- `help` - показать справку
- `quit` / `exit` - выйти из игры

## Демонстрация (asciinema)

Запись игрового процесса (от запуска до победы):

[![asciinema demo](https://asciinema.org/a/hdMRWk7Uzrf0DjKE.svg)](https://asciinema.org/a/hdMRWk7Uzrf0DjKE)



