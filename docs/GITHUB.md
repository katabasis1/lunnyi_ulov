# Работа с GitHub

Репозиторий = папка `lunnyi_ulov/` (корень Godot-проекта). Ветка `main`, теги версий `v0.x.y`.

## Первая выгрузка (один раз)
1. Создай на GitHub пустой репозиторий, например `lunnyi-ulov` (до релиза лучше приватный). Без README и .gitignore — они уже есть.
2. Скачай из Pod `builds/lunnyi_ulov_latest.zip`, распакуй.
3. В терминале:
```
cd lunnyi_ulov
git init -b main
git add -A
git commit -m "[Э0.2] v0.0.2: план, правила, GitHub, тексты"
git remote add origin https://github.com/<логин>/lunnyi-ulov.git
git push -u origin main
git tag v0.0.2 && git push --tags
```

## Каждое обновление от агента
1. Скачай `builds/lunnyi_ulov_latest.zip`, распакуй поверх рабочей папки (с заменой).
2. Если в записи DEVLOG есть «Удалить файлы» — удали перечисленные.
3. Закоммить сообщением из DEVLOG:
```
git add -A
git commit -m "<сообщение из DEVLOG>"
git push
```
4. На вехах (`v0.<этап>.0`) — тег: `git tag v0.2.0 && git push --tags`.

## Если менял проект сам
Godot при открытии создаёт `.import` и `uid` — их тоже нужно коммитить. После своих изменений:
1. Закоммить и запушь.
2. На GitHub: Code → Download ZIP, положи архив в Pod `incoming/repo/`.
3. Агент синхронизирует рабочую копию в Pod и продолжит с неё.

## Прямой доступ агента
Если администратор workspace подключит GitHub к Dust, агент сможет сам читать репозиторий и делать коммиты. Тогда шаги выше не нужны.
