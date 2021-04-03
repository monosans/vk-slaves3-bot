## **vk-slaves3-bot - бот для игры ["ВРабстве 3.0"](https://vk.com/app7790408) ВКонтакте.**

Наша [группа ВКонтакте](https://vk.com/club203543653), в ней публикуются новости и другая полезная информация, также через группу есть возможность войти в беседу.

**Лучшая благодарность - звёздочка на GitHub и "спасибо" в [ЛС в ВК](https://vk.com/id607137534).**

**Если хотите отблагодарить материально, пишите в [ЛС](https://vk.com/id607137534).**

## Установка на Windows

- Устанавливаем [Python](https://www.python.org/downloads/windows) (Для Windows 7 нужен [Python 3.8](https://python.org/ftp/python/3.8.8/python-3.8.8.exe)). Во время установки обязательно ставим галочку `Add Python to PATH (Добавить Python в PATH)`
- [Скачиваем архив с ботом](https://github.com/monosans/vk-slaves3-bot/archive/refs/heads/main.zip).
- Распаковываем архив.
- Редактируем файл `config.json` через любой текстовый редактор:
  - authorization:
    - Открываем [игру](https://vk.com/app7790408)
    - Нажимаем `F12` (Для Chromium браузеров)
    - Перезагружаем страницу горячей клавишей `F5`
    - В появившейся панели выбираем вкладку `Network`
    - Находим кнопку `Filter` (в виде воронки)
    - В появившемся поле пишем `me`
    - В панели появится поле `me`, нажимаем по нему
    - Появится еще одна панель, выбираем в ней вкладку `Headers`
    - Ищем поле `authorization`
    - Копируем его значение (начинается c **Bearer**, **Bearer** копировать тоже нужно)
    - Вставляем скопированный текст в значение `authorization` в `config.json` между кавычками
  - buy_slaves_mode - режим покупки рабов (0 - выкл, получать только бонус; 1 - покупать случайных рабов; 2 - покупать рабов у игроков из топа; 3 - покупать рабов у людей из списка `"buy_from_ids"`)
  - buy_from_ids - ID людей через запятую, у которых вы хотите скупать рабов при `"mode": 3`. ID можно получить через [сайт](https://regvk.com/id).
  - min_price - минимальная цена для покупки раба. Значения выше 20 приведут к более долгому поиску рабов.
  - max_price - максимальная цена для покупки раба.
  - min_delay - минимальная задержка между одинаковыми операциями в секундах. Значения ниже 3.34 скорее всего приведут к блокировке.
  - max_delay - максимальная задержка между одинаковыми операциями в секундах. Чем ниже, тем выше вероятность получения блокировки.

Запуск: `start.bat`. Если после запуска ничего не происходит или выходит ошибка, связанная с Python или pip:

- Откройте `cmd`
- Напишите `python -V`
- Вывод должен соответстовать виду: `Python версия`. При этом версия должна быть выше **3.7.X**.
- Если вывод не соотвествует виду, нужно переустановить [Python](https://www.python.org/downloads/windows). Во время установки нужно обязательно поставить галочку `Add Python to Path (Добавить Python в PATH)`

## Установка на Termux (Android)

- Устанавливаем Termux, желательно с [F-Droid](https://f-droid.org/repo/com.termux_108.apk), т.к. в Google Play разработчик его больше не обновляет.
- Запускаем Termux.
- Пишем по порядку:
  - cd
  - pkg install -y git python
  - git clone https://github.com/monosans/vk-slaves3-bot
- Редактируем файл `config.json` командой `nano vk-slaves3-bot/config.json` по инструкции для Windows. Для удобства редактирования можете скачать Hacker's Keyboard в Google Play, в ней в горизонтальном положении есть стрелочки для управления курсором. Чтобы получить `authorization` с телефона, можно использовать [приложение F12](https://play.google.com/store/apps/details?id=com.asfmapps.f12).
- Когда файл отредактирован, для сохранения нажмите Ctrl-O, Enter, Ctrl-X.

Запуск: `sh vk-slaves3-bot/launch.sh`

## Переустановка в Termux

Ввести команды по порядку:

```
cd
rm -rf vk-slaves3-bot
```

После этого заново установить по инструкции.
