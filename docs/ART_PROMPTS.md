# ART PROMPTS — промпты для финальной графики (ChatGPT)

Порядок работы с каждым графическим элементом — PLAN.md §2.5:
временный ассет от агента → промпт здесь → финал из ChatGPT в Pod `incoming/art/<ID>.png` → обработка `tools/art/` → замена по тому же пути.

Статусы: `временный` · `промпт выдан` · `финал получен` · `в игре`.

## Мастер-блок стиля (v0.1 — уточняется на Э0.4)
Добавляй в конец каждого промпта:

```
Style: detailed 16-bit pixel art with crisp hard-edged pixels, no anti-aliasing, no blur, no gradients between pixels.
Limited palette: deep cobalt blue, navy, teal, desaturated moss green, moonlight white; warm orange and amber only for fire and lanterns; rare crimson accent.
Lighting inspired by 1980s dark fantasy oil paintings: glowing bioluminescent water, soft mist, moonlit rim light.
Mood: melancholic, quiet, cozy dark fantasy. No text, no letters, no logos, no blood, no religious symbols.
```

Для отдельных объектов (спрайтов) добавляй:

```
Single object, centered, full body visible, transparent background (if transparency is unavailable, use a flat solid #FF00FF background). Even lighting from the upper left, no cast shadow on the background.
```

## Реестр ассетов

| ID | Что | Путь в проекте | Размер в игре | Статус |
|---|---|---|---|---|
| — | заполняется на Э0.4 | — | — | — |
