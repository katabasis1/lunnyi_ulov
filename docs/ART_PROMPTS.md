# ART PROMPTS — промпты для финальной графики (ChatGPT)

Порядок работы с каждым графическим элементом — PLAN.md §2.5, правила стиля — ART_BIBLE.md.
Временный ассет от агента → промпт здесь → финал из ChatGPT в Pod `incoming/art/<ID>.png` → `tools/art/process_art.py --incoming` → замена по тому же пути. Сцены не меняются.

Статусы: `временный` · `промпт выдан` · `финал получен` · `в игре`.

## Как пользоваться (для человека)
1. Открой ChatGPT с генерацией изображений. На каждый ассет — новый чат, чтобы стиль соседних картинок не смешивался.
2. **Прикрепи эталон стиля** `docs/concept/01_approved_style_B_key_scene.png`. Для поз Ирвена и кота после утверждения их idle-финала прикладывай ещё и его — так персонаж останется тем же.
3. Скопируй блок промпта целиком: мастер-блок стиля в нём уже есть.
4. Если ChatGPT может сделать прозрачный фон — хорошо. Если нет — фон должен быть ровным пурпурным `#FF00FF`.
5. Сделай 2–4 варианта, выбери лучший по силуэту и композиции. Сглаженные пиксели не страшны: скрипт сам загонит картинку в сетку и палитру.
6. Скачай PNG, назови `<ID>.png` (ID — в заголовке промпта) и положи в Pod в папку `incoming/art/` (или прикрепи в чат).
7. Напиши агенту «финалы в incoming». Агент обработает, соберёт макет сцены и покажет «было/стало».

Если ChatGPT дорисовал лишнее (воду под замком, пол под персонажем) — ничего не переделывай, агент обрежет исходник (`--crop`).

## Мастер-блок стиля v1.0
Уже вставлен в каждый промпт ниже. Источник — ART_BIBLE.md §13. При изменении — поднять версию и обновить промпты со статусом «промпт выдан».

## Реестр ассетов

| ID | Что | Путь в проекте | Холст | Формат в ChatGPT | Пакет | Статус |
|---|---|---|---|---|---|---|
| `char_irven_idle` | Ирвен сидит (idle) | `art/characters/irven/irven_idle.png` | 96×128 | 1024×1536 | 1 | промпт выдан |
| `char_cat_idle` | Уголёк сидит (idle) | `art/characters/cat/cat_idle.png` | 32×32 | 1024×1024 | 1 | промпт выдан |
| `env_shore_sky` | Небо «Лунного берега» | `art/environment/shore/shore_sky.png` | 640×360 | 1536×1024 | 1 | промпт выдан |
| `env_moon_full` | Полная луна | `art/environment/sky/moon_full.png` | 56×56 | 1024×1024 | 1 | промпт выдан |
| `env_shore_clouds` | Облака | `art/environment/shore/shore_clouds.png` | 640×112 | 1536×1024 | 1 | промпт выдан |
| `env_shore_castle` | Замок Вельмор на острове | `art/environment/shore/shore_castle.png` | 640×260 | 1536×1024 | 1 | промпт выдан |
| `env_shore_cliffs` | Скалы и лес по краям залива | `art/environment/shore/shore_cliffs.png` | 640×300 | 1536×1024 | 1 | промпт выдан |
| `env_shore_water` | Вода залива | `art/environment/shore/shore_water.png` | 640×300 | 1536×1024 | 1 | промпт выдан |
| `env_shore_pier` | Причал с фонарём | `art/environment/shore/shore_pier.png` | 256×160 | 1536×1024 | 1 | промпт выдан |
| `env_shore_foreground` | Передний план: валуны, папоротники | `art/environment/shore/shore_foreground.png` | 640×240 | 1536×1024 | 1 | промпт выдан |
| `prop_bobber_default` | Поплавок (коренастый) | `art/props/bobber/bobber_default.png` | 12×16 | 1024×1536 | 2 | промпт выдан |
| `prop_rod_basic` | Простое удилище, без катушки | `art/props/rod/rod_basic.png` | 96×8 | 1536×1024 | 2 | промпт выдан |
| `ui_catch_card_frame` | Рамка карточки улова | `art/ui/catch_card/card_frame.png` | 232×300 | 1024×1536 | 2 | промпт выдан |
| `ui_rarity_gems` | Камни редкости, 5 кадров | `art/ui/catch_card/rarity_gems.png` | 80×16 | 1536×1024 | 2 | промпт выдан |
| `ui_catch_stamps` | Штампы «Новое!» / «Рекорд!», 2 кадра | `art/ui/catch_card/stamps.png` | 144×28 | 1536×1024 | 2 | промпт выдан |
| `ui_icon_coin` | Серебро, HUD | `art/ui/icons/coin.png` | 16×16 | 1024×1024 | 2 | промпт выдан |
| `ui_icon_coin_lg` | Серебро, крупно (тот же исходник) | `art/ui/icons/coin_lg.png` | 32×32 | — | 2 | промпт выдан |
| `ui_icon_pearl` | Лунный жемчуг, HUD | `art/ui/icons/pearl.png` | 16×16 | 1024×1024 | 2 | промпт выдан |
| `ui_icon_pearl_lg` | Лунный жемчуг, крупно (тот же исходник) | `art/ui/icons/pearl_lg.png` | 32×32 | — | 2 | промпт выдан |
| `cr_moon_roach` | №1 Лунная плотва | `art/creatures/moon_roach.png` | 48×32 | 1536×1024 | 2 | промпт выдан |
| `cr_mist_ruffe` | №2 Туманный ёрш | `art/creatures/mist_ruffe.png` | 48×32 | 1536×1024 | 2 | промпт выдан |
| `cr_tile_hermit` | №3 Краб-отшельник | `art/creatures/tile_hermit.png` | 48×32 | 1536×1024 | 2 | промпт выдан |
| `cr_lanternfish` | №4 Фонарница | `art/creatures/lanternfish.png` | 64×40 | 1536×1024 | 3 | промпт выдан |
| `cr_whisper_eel` | №5 Угорь-шептун | `art/creatures/whisper_eel.png` | 64×40 | 1536×1024 | 3 | промпт выдан |
| `cr_nightlight_jelly` | №6 Медуза-ночник | `art/creatures/nightlight_jelly.png` | 64×40 | 1536×1024 | 3 | промпт выдан |
| `cr_stargazer` | №7 Звездочёт | `art/creatures/stargazer.png` | 96×56 | 1536×1024 | 3 | промпт выдан |
| `cr_knight_pike` | №8 Рыцарская щука | `art/creatures/knight_pike.png` | 96×56 | 1536×1024 | 3 | промпт выдан |
| `cr_lord_of_bay` | №9 Хозяин залива | `art/creatures/lord_of_the_bay.png` | 128×80 | 1536×1024 | 3 | промпт выдан |
| `cr_rust_perch` | №10 Ржавый окунь | `art/creatures/rust_perch.png` | 48×32 | 1536×1024 | 3 | промпт выдан |
| `cr_crest_flounder` | №11 Гербовая камбала | `art/creatures/crest_flounder.png` | 64×40 | 1536×1024 | 3 | промпт выдан |
| `cr_keykeeper_newt` | №12 Тритон-ключник | `art/creatures/keykeeper_newt.png` | 64×40 | 1536×1024 | 3 | промпт выдан |
| `cr_shadow_ray` | №13 Тенекрылка | `art/creatures/shadow_ray.png` | 96×56 | 1536×1024 | 3 | промпт выдан |
| `cr_crimson_carp` | №14 Багровый карп | `art/creatures/crimson_carp.png` | 96×56 | 1536×1024 | 3 | промпт выдан |
| `cr_ghost_sturgeon` | №15 Призрачный осётр | `art/creatures/ghost_sturgeon.png` | 128×80 | 1536×1024 | 3 | промпт выдан |
| `relic_key` | Ржавый ключ от южной башни | `art/relics/relic_key.png` | 32×32 | 1024×1024 | 3 | промпт выдан |
| `relic_horse` | Деревянная лошадка | `art/relics/relic_horse.png` | 32×32 | 1024×1024 | 3 | промпт выдан |
| `relic_medallion` | Медальон с портретом лорда | `art/relics/relic_medallion.png` | 32×32 | 1024×1024 | 3 | промпт выдан |
| `relic_spyglass` | Подзорная труба смотрителя | `art/relics/relic_spyglass.png` | 32×32 | 1024×1024 | 3 | промпт выдан |
| `sil_*` (15 шт.) | Силуэты существ для «Книги вод» | `art/creatures/silhouettes/<имя>.png` | как у существа | — | 3 | производный, промпт не нужен |
| `char_brook_idle` | Брук стоит (idle) | `art/characters/brook/brook_idle.png` | 96×128 | 1024×1536 | 4 | промпт выдан |
| `char_elsa_idle` | Эльса (idle) | `art/characters/elsa/elsa_idle.png` | 96×128 | 1024×1536 | 4 | промпт выдан |
| `env_shop_back` | Лавка Брука: задняя стена с окном | `art/environment/shop/shop_back.png` | 640×360 | 1536×1024 | 4 | промпт выдан |
| `env_shop_counter` | Лавка Брука: прилавок | `art/environment/shop/shop_counter.png` | 640×128 | 1536×1024 | 4 | промпт выдан |
| `env_moat_castle` | Ров Вельмора: стены замка | `art/environment/moat/moat_castle.png` | 640×360 | 1536×1024 | 4 | промпт выдан |
| `env_moat_water` | Ров Вельмора: вода | `art/environment/moat/moat_water.png` | 640×300 | 1536×1024 | 4 | промпт выдан |
| `env_moat_ledge` | Ров Вельмора: обломки ворот (место рыбалки) | `art/environment/moat/moat_ledge.png` | 256×160 | 1536×1024 | 4 | промпт выдан |
| `prop_boat` | Лодка (починенная) | `art/props/boat/boat.png` | 128×48 | 1536×1024 | 4 | промпт выдан |
| `env_moat_foreground` | Ров Вельмора: передний план | `art/environment/moat/moat_foreground.png` | 640×240 | 1536×1024 | 4 | промпт выдан |
| `ui_bait_icons` | Наживки, лист из 5 кадров | `art/ui/icons/baits.png` | 160×32 | 1536×1024 | 4 | промпт выдан |
| `ui_upgrade_icons` | Улучшения, лист из 6 кадров | `art/ui/icons/upgrades.png` | 192×32 | 1536×1024 | 4 | промпт выдан |
| `ui_nav_icons` | Иконки навигации, лист из 5 кадров | `art/ui/icons/nav.png` | 160×32 | 1536×1024 | 4 | промпт выдан |
| `ui_panel_frame` | Рамка панели (9-slice) | `art/ui/frames/panel.png` | 96×96 | 1024×1024 | 4 | промпт выдан |
| `ui_button` | Кнопка, 2 состояния | `art/ui/frames/button.png` | 128×24 | 1536×1024 | 4 | промпт выдан |
| `ui_action_button` | Большая кнопка действия | `art/ui/frames/action_button.png` | 64×64 | 1024×1024 | 4 | промпт выдан |
| `ui_tension_frame` | Рамка шкалы натяжения | `art/ui/frames/tension_frame.png` | 20×160 | 1024×1536 | 4 | промпт выдан |
| `ui_moon_phases` | 8 фаз луны, HUD | `art/ui/icons/moon_phases.png` | 128×16 | 1536×1024 | 4 | промпт выдан |
| `ui_moon_phases_lg` | 8 фаз луны, крупно (тот же исходник) | `art/ui/icons/moon_phases_lg.png` | 256×32 | — | 4 | промпт выдан |
| `ui_logo_emblem` | Логотип: эмблема без текста | `art/ui/logo/logo_emblem.png` | 160×128 | 1024×1024 | 4 | промпт выдан |
| кот в лодке | Уголёк на носу лодки | — (`char_cat_idle` поверх `prop_boat`) | — | — | 4 | отдельный ассет не нужен (D-026) |

---

## Пакет 1 — «Лунный берег», Ирвен, Уголёк

### `char_irven_idle` — Ирвен сидит
Холст 96×128, привязка — низ по центру. Удочки нет: она отдельный узел и гнётся при вываживании.

```
Create a pixel art game sprite of Irven, an old wandering wizard who fishes at night. Portrait image 1024x1536.

Pose: sitting on the edge of a pier (do NOT draw the pier), legs hanging down, three-quarter back view from the left, body and head turned to the right toward the sea. Hands resting together on his knees, holding nothing (the fishing rod is a separate sprite).
Look: tall pointed wide-brimmed wizard hat, dark brown, the tip bent backward; long heavy dark brown hooded cloak with two or three patches and a frayed hem; rope belt with a small leather pouch; long silver-grey beard visible from the side; face hidden in the shadow of the brim, only the tip of the nose visible; old worn boots. Calm, tired, cozy posture.
Light: thin cold moonlight rim on the right edges of the hat, shoulder and back; faint warm lantern glow on the left side of the cloak.

Single isolated game sprite, the whole figure visible and centered, nothing else in the image.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow on the ground, no floor, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 96x128 pixels, so avoid tiny details.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: limited, about 48 colors. Deep night blues and cobalt dominate; desaturated teal-green forest; mossy greens; cool stone greys; dark weathered wood browns. Warm orange and amber appear only in lantern light, fire and windows. No crimson.
Lighting: full moon key light from the upper right gives a thin cold blue-white rim light on right and top edges; a small warm lantern glow from the lower left; shadows go into deep navy, never pure black.
Mood: quiet, melancholic, cozy dark fantasy, like a 1980s dark fantasy book cover rendered as a pixel art game.
Forbidden: text, letters, logos, watermarks, blood, skulls, crosses, religious symbols, pentagrams.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `char_cat_idle` — Уголёк сидит
Холст 32×32 — очень мелко. Главное — силуэт кота, ободок света и два янтарных глаза.

```
Create a pixel art game sprite of Ugolyok, a small black cat. Square image 1024x1024.

Pose: sitting upright in side view, facing right, tail wrapped around its front paws, ears up.
Look: black fur, big round glowing amber-yellow eyes, one ear with a small notch, slightly fluffy chest. Realistic cat proportions, cute but not cartoonish, no outline.
Light: a thin cold blue moonlight rim along the top and right edges of the silhouette so the black cat reads against a dark night background; a tiny warm glint on the left from a lantern.

Single isolated game sprite, the whole figure visible and centered, nothing else in the image.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow on the ground, no floor, no gradient.
Very bold simple shapes with large pixel clusters: the sprite will be downscaled to 32x32 pixels, so avoid any tiny details.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no text.
Palette: near-black navy for the fur, cobalt and pale blue for the rim light, amber for the eyes. Nothing else.
Mood: quiet, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_shore_sky` — небо
Непрозрачный слой 640×360, бесшовный по горизонтали. Нижние ~15% картинки могут обрезаться.

```
Create a pixel art night sky for a 2D game background. Landscape image 1536x1024, the sky fills the whole image edge to edge.

Smooth vertical gradient of deep cobalt and navy: almost black at the top, lighter and bluer near the bottom edge where the horizon will be. Scattered tiny stars of 1 to 2 pixels, a few brighter four-pointed sparkle stars, a faint diagonal band of the milky way made of dim blue pixel dust.
No moon (it is a separate sprite), no clouds, no land, no water, no trees.
The left and right edges must match so the image tiles seamlessly horizontally.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no noise, no text. Use ordered pixel dithering for the gradient instead of smooth blending.
Palette: deep night blues, cobalt, pale blue-white stars. Nothing warm.
Mood: quiet, melancholic, cozy dark fantasy, like a 1980s dark fantasy book cover rendered as a pixel art game.
Forbidden: text, letters, logos, watermarks.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_moon_full` — полная луна
Холст 56×56, привязка — центр. Ореол и свечение добавит шейдер, фазы — маска в шейдере.

```
Create a pixel art game sprite of a full moon. Square image 1024x1024.

A perfectly round disc, pale blue-white with soft grey-blue craters and darker maria, slightly brighter along the upper right edge. No glow, no halo, no clouds, no stars: the glow will be added in the game.

Single isolated game sprite, centered, nothing else in the image.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no gradient.
Large pixel clusters: the sprite will be downscaled to 56x56 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no text.
Palette: pale blue-white, cool grey-blue, soft cobalt.
Forbidden: text, letters, logos, watermarks, faces in the moon.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_shore_clouds` — облака
Слой 640×112, бесшовный по горизонтали, берётся средняя полоса картинки.

```
Create a pixel art parallax layer of night clouds for a 2D game. Landscape image 1536x1024.

ONE horizontal band of puffy cumulus clouds across the full width, in the vertical middle of the image, about one quarter of the image height tall. The band is uneven: bigger puffs and gaps, soft ragged bottom edge with wisps, never a straight cut. Cobalt cloud bodies, pale blue-white moonlit rims on the top edges, dark navy undersides, large chunky pixel clusters.
The left and right edges must match so the layer tiles seamlessly horizontally.
Everything that is not cloud is perfectly flat solid magenta #FF00FF (or real transparency). No moon, no stars, no land.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: night blues, cobalt, pale blue-white. Nothing warm.
Lighting: full moon from the upper right.
Mood: quiet, melancholic, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_shore_castle` — замок Вельмор
Слой 640×260, низ — линия воды. Используется нижние ~60% картинки.

```
Create a pixel art parallax background layer for a 2D game: the ruined gothic castle Velmor on a rocky island in the middle distance. Landscape image 1536x1024.

The castle stands slightly right of center: tall thin spires and towers, a broken arched bridge, a few warm amber windows still lit, the lower walls half sunk into the sea. Low distant rocky islets and sea stacks along the rest of the horizon. Atmospheric perspective: lighter, bluer and lower in contrast than the foreground, cold blue mist at the base.
Everything sits in the lower 60% of the image. The bottom edge of the image is the waterline: a straight horizontal cut, and NO water is drawn.
Everything that is not part of this layer (the sky above and around) is perfectly flat solid magenta #FF00FF (or real transparency). No moon, no characters.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: night blues, cobalt, misty pale blue, cool stone greys; warm amber only in a few windows. No crimson.
Lighting: full moon key light from the upper right gives a thin cold blue-white rim light on right and top edges; shadows go into deep navy, never pure black.
Mood: quiet, melancholic, cozy dark fantasy, like a 1980s dark fantasy book cover rendered as a pixel art game.
Forbidden: text, letters, logos, watermarks, blood, skulls, crosses on the spires or anywhere, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_shore_cliffs` — скалы и лес
Слой 640×300, низ — линия воды. Центр пустой: там видны вода и замок.

```
Create a pixel art parallax background layer for a 2D game: dark forested cliffs framing a bay. Landscape image 1536x1024.

On the left side a tall cliff with dark fir trees reaching high; on the right side lower rocky cliffs with a few fir trees and two tall sea stacks. The whole center of the image, about 60% of the width, is open and empty so the sea and a distant castle stay visible. Deep teal-blue silhouettes with moonlit rim highlights, wisps of mist at the base, a few fireflies as tiny amber dots.
Everything sits in the lower 70% of the image. The bottom edge is the waterline: a straight horizontal cut, NO water drawn.
Everything that is not part of this layer (sky and the open center) is perfectly flat solid magenta #FF00FF (or real transparency). No castle, no characters.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: night blues, dark desaturated teal-green forest, cool stone greys, tiny amber fireflies. No crimson.
Lighting: full moon key light from the upper right gives a thin cold blue-white rim light on right and top edges; shadows go into deep navy, never pure black.
Mood: quiet, melancholic, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_shore_water` — вода залива
Непрозрачный слой 640×300, верх — горизонт. Нижние ~30% картинки могут обрезаться. Волны и блики потом оживит шейдер воды.

```
Create a pixel art calm night sea surface for a 2D game. Landscape image 1536x1024, the water fills the whole image edge to edge.

Seen from a low angle: the horizon is exactly at the top edge, lighter cobalt there, getting deeper navy toward the bottom. Gentle horizontal wave lines in cobalt and cyan: tiny near the top, larger near the bottom. A bright vertical moon-path reflection of shimmering pale blue-white pixel dashes centered at about 65% of the width from the left, narrow at the top and widening toward the bottom. Sparse glowing bioluminescent blue sparkles.
No land, no sky, no objects, no boats.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no text. Use ordered pixel dithering instead of smooth blending.
Palette: deep night blues, cobalt, cyan, pale blue-white. Nothing warm.
Mood: quiet, melancholic, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_shore_pier` — причал с фонарём
Холст 256×160, привязка — низ по центру. Фонарь слева: потом свет станет живым (шейдер или Light2D).

```
Create a pixel art game sprite: the end of an old wooden fishing pier. Landscape image 1536x1024.

Three-quarter side view; the deck runs horizontally from the left to the right end. Weathered dark planks, thick round wooden pilings going straight down and cut off flat at the bottom, ropes wrapped around the posts, moss on the pilings. At the left end a tall wooden post with a crossbar and a hanging iron lantern glowing warm amber-orange; warm light on the nearest planks. The rest is lit by cold blue moonlight from the upper right.
No people, no fishing rod, no water.

Single isolated game sprite, nothing else in the image.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no gradient.
Large pixel clusters: the sprite will be downscaled to 256x160 pixels.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: dark weathered wood browns, night blues, mossy greens, warm amber and orange only around the lantern. No crimson.
Lighting: full moon key light from the upper right gives a thin cold blue-white rim light on right and top edges; shadows go into deep navy, never pure black.
Mood: quiet, melancholic, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_shore_foreground` — передний план
Слой 640×240, низ — низ экрана. Используется нижняя половина картинки. Центр пустой: там вода и поплавок.

```
Create a pixel art foreground framing layer for the bottom of a 2D game screen. Landscape image 1536x1024.

Large mossy dark boulders, ferns and tall grass in the bottom left and bottom right corners, rising a bit higher on the left. A few fireflies as small glowing amber dots. Dark silhouettes with subtle blue moonlit rims and a little warm glow on the left.
Everything sits in the lower half of the image; the center and the whole upper half are empty so the water behind stays visible. The bottom edge of the image is the bottom of the screen.
Everything that is not rocks or plants is perfectly flat solid magenta #FF00FF (or real transparency). No water, no characters.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: night blues, mossy greens, dark desaturated teal, cool stone greys, tiny amber accents. No crimson.
Lighting: full moon key light from the upper right gives a thin cold blue-white rim light on right and top edges; shadows go into deep navy, never pure black.
Mood: quiet, melancholic, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

---

## Пакет 2 — рыбалка и карточка улова, первые 3 существа (Э0.4.3)

Общее для пакета: один исходник = один ассет, кроме монеты и жемчуга (один исходник даёт иконки 16 и 32 px) и листов `ui_rarity_gems` / `ui_catch_stamps` (скрипт сам находит объекты, ровная сетка не нужна). Макеты для сверки: `docs/art_mocks/fishing_mock_latest.png`, `docs/art_mocks/catch_mock_latest.png`.

### `prop_bobber_default` — поплавок
Холст 12×16, привязка — низ по центру (точка на воде). Должен быть **коренастым**: тонкий перьевой поплавок в 12 px превращается в палочку шириной 3 px, и сжатие-растяжение на нём не видно.

```
Create a pixel art game sprite of a single chunky fishing float (bobber), upright, front view. Portrait image 1024x1536.

Look: a fat round pear-shaped carved wooden body, almost as wide as it is tall; the lower half dark weathered brown wood, the upper half bone-white with one thin dark band; on top a short thick stubby antenna ending in a round glowing warm amber bead like a firefly; a tiny wire eyelet at the very bottom. Cute, bold, readable silhouette.
Light: thin cold blue-white moonlight rim on the right edge; a warm amber glint from the bead.

Single isolated game sprite, the whole object visible and centered, nothing else in the image, no water.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Very large simple shapes: the sprite will be downscaled to 12x16 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: dark weathered wood browns, bone white, night blues; amber only in the bead. No crimson, no red.
Mood: quiet, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `prop_rod_basic` — простое удилище
Холст 96×8: горизонтально, рукоять слева, кончик справа. Без катушки: она торчит вниз и не помещается в 8 px; катушка будет у улучшенных удочек. В игре текстура гнётся костями при вываживании.

```
Create a pixel art game sprite of a plain old wooden fishing pole lying perfectly horizontal and straight across the whole width of the image. Landscape image 1536x1024.

Look: a straight hazel branch pole with NO reel. Handle on the LEFT: a thicker grip wrapped with dark cord and a small leather band. From there the pole tapers smoothly and evenly to a very thin tip at the RIGHT edge; two small wood knots along the length. Nothing hangs below the pole: no reel, no line, no hook, no hands.
Light: a soft, subtle cool highlight along the top edge only; dark brown shadow along the bottom edge. Mostly dark weathered wood.

Single isolated game sprite, the whole pole visible, straight and level, nothing else in the image.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
The sprite will be downscaled to 96x8 pixels: the grip must be clearly thicker than the tip.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: dark weathered wood browns, dark cord, a little night blue in the highlight. No crimson.
Forbidden: text, letters, logos, watermarks.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_catch_card_frame` — рамка карточки улова
Холст 232×300. Окно сверху — под существо ×2, гнездо по центру верхней кромки — под камень редкости 16×16, пергамент снизу — под имя, размер и цену (текст пишет Godot). Тон пергамента задан в промпте специально: бежевого в палитре нет, и пергамент ложится на тёплый ряд skin/wood (DECISIONS D-024).

```
Create a pixel art UI panel for a 2D game: an empty "catch card" frame, portrait, front view. Portrait image 1024x1536.

The card itself has proportions of about 3 wide by 4 tall (232 x 300) and fills the image height; leave magenta on the left and right.
Frame: dark wrought iron with rivets and small leaf-and-wave ornaments in the four corners; a thin cold blue moonlit highlight on the top and right edges of the iron. At the top center, sitting on the upper edge of the frame, a small empty round iron socket; its hole is about 7% of the card width (a 16-pixel gem goes there later).
Inside, two areas separated by a thin iron bar:
- upper area, from about 8% to 60% of the card height: a recessed window filled with deep navy night water, slightly lighter in the middle, a few faint blue sparkles, completely empty;
- lower area, from about 63% to 95% of the height: an aged parchment plate in warm peach-tan (close to #e0a982) with darker tan worn edges (close to #b88a52), completely empty.
Absolutely no text, letters, numbers or symbols anywhere. No creature, no characters.

Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Clean large pixel clusters: the panel will be downscaled to 232x300 pixels.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise.
Palette: dark iron greys and navy, cobalt, warm peach-tan parchment, dark tan. No crimson, no bright yellow, no pure white.
Lighting: moon key light from the upper right, shadows go into deep navy, never pure black.
Mood: quiet, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_rarity_gems` — камни редкости (лист из 5 кадров)
Холст 80×16 (5 кадров по 16×16). Порядок — по редкостям GDD §6: обычная, необычная, редкая, легендарная, лунная. Кабошоны, а не огранка: грани в 16 px рассыпаются в пятна.

```
Create a pixel art game icon sheet. Landscape image 1536x1024.

Exactly FIVE smooth round cabochon gemstones (polished domes, no facets) in one horizontal row, evenly spaced with wide gaps, all the same size, each in a thin dark iron bezel ring. Each gem is one solid color with simple shading: darker at the bottom, the main tone in the middle, one small bright highlight in the upper right.
From left to right: 1) pale milky moon-white; 2) pure emerald green; 3) deep cobalt blue; 4) warm glowing amber-gold; 5) soft lavender violet.

Nothing else in the image. Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Each gem will be downscaled to 16x16 pixels: bold and simple, no patterns, no swirls.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no text.
Forbidden: text, letters, numbers, logos, watermarks.
Use the attached reference image only for style and lighting, not for composition.
```

### `ui_catch_stamps` — штампы «Новое!» / «Рекорд!» (лист из 2 кадров)
Холст 144×28 (2 кадра по 72×28). Рамка пустая: надпись — Label в Godot, чтобы работала локализация. Наклон −12° делает узел в игре. Кадр 0 — бирюзовый, кадр 1 — янтарный.

```
Create pixel art UI elements for a 2D game. Landscape image 1536x1024.

Exactly TWO empty ink stamp frames side by side with a wide gap, same size and shape. Each is a wide horizontal rounded-rectangle rubber-stamp border with a double outline and a rough worn ink texture with small gaps, like a real stamp; the interior is EMPTY and transparent. Left stamp: turquoise jade-green ink. Right stamp: warm amber-gold ink. Both perfectly level, not rotated.
Absolutely no text, letters, numbers or symbols.

Nothing else in the image. Background: perfectly flat solid magenta #FF00FF (or real transparency), no paper, no shadow, no gradient.
Each stamp will be downscaled to 72x28 pixels: the border must be bold, about 3 pixels thick at that size.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur.
Forbidden: text, letters, logos, watermarks.
Use the attached reference image only for style, not for composition.
```

### `ui_icon_coin` + `ui_icon_coin_lg` — серебро
Холсты 16×16 (HUD, цены) и 32×32 (лавка, награды) из одного исходника. Рыбка на монете в 16 px почти исчезает — это нормально, читается край и блик.

```
Create a pixel art game currency icon. Square image 1024x1024.

One old silver coin, front view, perfectly round, thick raised rim, an embossed simple fish emblem in the center, slightly worn. Cool silver-grey and pale blue-white tones; a bright moonlight highlight on the upper right of the rim; deep navy shadow on the lower left.

Single isolated icon, centered, nothing else in the image.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Bold and readable: the icon will be downscaled to 16x16 and 32x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no text.
Palette: silver greys, pale blue-white, navy. No gold, no crimson.
Forbidden: text, letters, numbers, logos, watermarks, crosses, religious symbols.
Use the attached reference image only for style and lighting, not for composition.
```

### `ui_icon_pearl` + `ui_icon_pearl_lg` — лунный жемчуг
Холсты 16×16 и 32×32 из одного исходника. Ореол свечения не рисовать: его даст шейдер, а в спрайте он превращается в грязную кайму.

```
Create a pixel art game currency icon. Square image 1024x1024.

One moon pearl: a perfectly round glowing pearl, pale blue-white with soft lavender and cobalt iridescent bands, a bright white highlight in the upper right, a small four-pointed sparkle star touching its upper right edge, deep cobalt shade at the lower left.

Single isolated icon, centered, nothing else in the image: no shell, no glow halo.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Bold and readable: the icon will be downscaled to 16x16 and 32x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no text.
Palette: pale blue-white, lavender, cobalt, navy only.
Forbidden: text, letters, logos, watermarks.
Use the attached reference image only for style and lighting, not for composition.
```

### `cr_moon_roach` — Лунная плотва (№1, обычная)
Холст 48×32, голова влево (как у всех существ). В карточке показывается ×2. GDD: «Чешуя отливает голубым, даже когда луна за тучами.»

```
Create a pixel art game sprite of a magical fish, the Moon Roach. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible, slightly curved as if swimming. A slender silvery roach with big round dark eyes; silver-blue scales that shimmer pale blue-white; a row of small softly glowing pale-blue dots along the side line; translucent cobalt fins and a forked tail with pale blue edges. Friendly and simple, realistic fish proportions.
Light: cold moonlight rim on the top edge, deep navy belly shadow.

Single isolated game sprite, centered, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 48x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: silver, pale blue-white, cobalt, navy. No red, no orange (real roach fins are red, ours are not).
Mood: quiet, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_mist_ruffe` — Туманный ёрш (№2, обычная)
Холст 48×32, голова влево. GDD: «Колючий и обидчивый.» Характер — в спинном плавнике-гребне и надутой морде.

```
Create a pixel art game sprite of a magical fish, the Mist Ruffe. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible. A small chubby spiky perch-like fish with a big spiny dorsal fin raised like a crest; a grumpy, offended face with a down-turned mouth and a big eye. Smoky grey-blue body with darker misty blotches; fin tips and tail fade into pale wisps like fog; a faint lavender sheen on the fins.
Light: cold moonlight rim on the top edge and the spines, deep navy belly shadow.

Single isolated game sprite, centered, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 48x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: misty grey-blue, slate, pale blue-white, a little lavender, navy. No red, no orange.
Mood: quiet, cozy dark fantasy, a little funny.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_tile_hermit` — Краб-отшельник (№3, обычная)
Холст 48×32, смотрит влево. GDD: «Живёт в обломке черепицы с крыши замка. Съезжать не собирается.» Черепица — сланцевая, как крыши Вельмора на фоне, а не терракотовая.

```
Create a pixel art game sprite of the Tile Hermit. Landscape image 1536x1024.

A small hermit crab that lives inside a curved broken piece of old slate roof tile instead of a shell. Side view, facing LEFT, peeking out of the tile with two eye stalks; one big claw and one small claw; a few walking legs. The tile piece is dark blue-grey slate, curved, with chipped edges and a little green moss on top. Legs and claws are muted warm brown with pale tips. Stubborn, cozy, funny character.
Light: cold moonlight rim on the top of the tile and the claws, deep navy shadows.

Single isolated game sprite, centered, the whole figure visible, nothing else in the image: no ground, no water.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 48x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: slate grey-blue, navy, moss green, muted brown. No red, no crimson.
Mood: quiet, cozy dark fantasy, a little funny.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

## Пакет 3 — существа №4–15 и реликвии (Э0.4.4)

Существа: голова влево, холст по классу (S 48×32, M 64×40, L 96×56, XL 128×80, ART_BIBLE §9). Реликвии: иконки 32×32, тот же эталон стиля.
**Силуэты** для неоткрытых существ в «Книге вод» рисовать не нужно: скрипт сам строит их из готового спрайта (заливка night_2) каждый раз, когда приходит финал существа.
**Осётр (`cr_ghost_sturgeon`) — на зелёном фоне `#00FF00`**, остальные на пурпурном.

### `cr_lanternfish` — №4 Фонарница
Холст 64×40, голова влево. GDD: «Носит на лбу огонёк и плывёт на любой свет». Огонёк — единственное тёплое пятно, ряд lantern.

```
Create a pixel art game sprite of a magical fish, the Lanternfish. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible. A small anglerfish-like fish with a big round head, a wide grin with a few tiny harmless teeth, big curious eyes, and a long thin stalk on its forehead that ends in a glowing warm amber light bulb hanging in front of its face. Dark navy-teal body with soft blue-grey spots, small fins, short tail. Curious and mischievous, more cute than scary.
Light: the amber lure casts warm light on the face and the front of the body; cold moonlight rim on the top edge; deep navy belly shadow.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 64x40 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: dark navy, teal, slate blue; warm amber and pale gold only for the lure glow. No red.
Mood: quiet, cozy dark fantasy, a little funny.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_whisper_eel` — №5 Угорь-шептун
Холст 64×40, голова влево, тело S-изгибом, чтобы угорь уместился в карточку. GDD: «Если поднести к уху, слышно что-то вроде шёпота».

```
Create a pixel art game sprite of a magical fish, the Whisper Eel. Landscape image 1536x1024.

A long slender eel in a gentle S-curve, head pointing LEFT, the whole body fits the frame. Smooth dark indigo-blue skin with a faint pale-blue shimmer line along the back; one long continuous soft fin along the back and the belly with pale cyan edges; small calm eyes, mouth slightly open as if whispering; a few tiny faint pale-blue swirl marks near the gills, like whispers made visible. Mysterious and sly.
Light: cold moonlight rim along the top of the curves, deep navy shadows inside the bends.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 64x40 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: indigo, navy, cobalt, pale cyan, a hint of teal. No red, no orange.
Mood: quiet, mysterious, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_nightlight_jelly` — №6 Медуза-ночник
Холст 64×40. Медуза «плывёт» влево, как все существа: купол слева, щупальца тянутся вправо. GDD: «Светится ровно и тихо».

```
Create a pixel art game sprite of a magical jellyfish, the Nightlight Jelly. Landscape image 1536x1024.

A glowing jellyfish swimming to the LEFT: a rounded bell dome on the left, soft ribbon tentacles trailing behind it to the right, so the whole creature lies horizontally. The bell is translucent pale blue with a softly glowing pale blue-white core and a scalloped rim; tentacles thin and wavy, cyan fading to deep blue, with tiny glowing dots. Calm and gentle, like a night-light.
Light: it glows by itself: bright pale blue-white core, darker cobalt edges, deep navy shadows in the folds.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 64x40 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: pale blue-white, cyan, cobalt, navy, a touch of soft teal. No red, no orange, no warm colors.
Mood: quiet, gentle, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_stargazer` — №7 Звездочёт
Холст 96×56, голова влево. GDD: «Глаза на макушке, смотрит только вверх. Считает звёзды и каждый раз сбивается». Крапины-звёзды — night_10/white.

```
Create a pixel art game sprite of a magical fish, the Stargazer. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible. A stocky flat-headed fish with a wide upturned mouth and two big eyes on the very top of its head, looking straight UP at the sky. Its dark navy back is covered with tiny white and pale-blue star-like speckles, like a night sky with little constellations; pale grey-blue belly; broad rounded pectoral fins; a dreamy, thoughtful expression.
Light: cold moonlight rim on the top of the head and back; the star speckles glow softly; deep navy belly shadow.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 96x56 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: deep navy, cobalt, slate blue, a little teal, pale blue-white and white for the speckles. No red, no orange.
Mood: quiet, dreamy, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_knight_pike` — №8 Рыцарская щука
Холст 96×56, голова влево. GDD: «Чешуя похожа на старый доспех, со вмятинами и рыжими пятнами». Ржавчина — lantern_0/wood, не красный.

```
Create a pixel art game sprite of a magical fish, the Knight Pike. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible. A long powerful pike with a long jaw (small teeth, not scary) and a stern proud eye. Its scales look like old knight's plate armor: overlapping steel-grey plates with tiny rivets, small dents and rusty orange-brown spots; the dorsal fin near the tail looks like a tattered plume. A stubborn guardian.
Light: cold moonlight shines on the top plates with bright steel highlights; deep navy shadows below.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 96x56 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: steel grey-blue, slate, navy; rust brown and dull orange only for rust spots; a little moss green. No red.
Mood: quiet, proud, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_lord_of_bay` — №9 Хозяин залива
Холст 128×80, голова влево. Легендарное существо. GDD: «Старше причала, а может, и замка. В усах ракушки. Никуда не торопится». Не страшный — древний и спокойный.

```
Create a pixel art game sprite of a magical fish, the Lord of the Bay. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible. A huge ancient catfish: massive broad head, small wise half-closed eyes, a wide calm mouth, very long drooping whiskers with small seashells and tiny barnacles hanging on them. Dark olive-teal skin; moss and tiny weeds grow on its back like on an old stone; a few softly glowing pale amber spots along its side; big rounded fins, heavy tail. Old, calm, unhurried and majestic.
Light: cold moonlight rim on the head and back, faint warm amber glow from the spots, deep navy shadow under the belly.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 128x80 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: dark teal, olive and moss green, slate, navy, pale grey-beige for the shells, faint amber for the glowing spots. No red.
Mood: quiet, majestic, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood, scary teeth.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_rust_perch` — №10 Ржавый окунь
Холст 48×32, голова влево. GDD: «Полосы на боках цвета старого железа».

```
Create a pixel art game sprite of a magical fish, the Rust Perch. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible. A small sturdy perch with a spiny dorsal fin and a calm round eye. Dark vertical stripes on its sides colored like old rusted iron (rust brown and dull orange-brown) over a muted greenish-slate body; amber-brown fins.
Light: cold moonlight rim on the top edge, deep navy belly shadow.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 48x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: slate green, moss, rust brown, dull orange-brown, navy. No bright red.
Mood: quiet, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_crest_flounder` — №11 Гербовая камбала
Холст 64×40, голова и оба глаза слева. GDD: «На спине узор, похожий на герб Вельмора». Узор выдуманный: щит с волной, без реальных гербов и символов (правила Яндекса).

```
Create a pixel art game sprite of a magical fish, the Crest Flounder. Landscape image 1536x1024.

A flat oval flounder seen from above at a slight tilt, its head and both eyes on the LEFT. On its back a natural spotted pattern that looks a bit like an old shield shape with a simple wave line inside, made of pale sand-colored spots on a dark slate-brown body. It is an invented pattern, not a real coat of arms. A soft frilled fin runs around the whole edge, a small tail on the right. Proud, heavy and a little funny.
Light: cold moonlight rim on the upper edge of the fin, deep navy shadow on the lower edge.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 64x40 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: slate brown, sand beige, muted wood brown, navy shadows, a little pale blue on the rim. No red.
Mood: quiet, cozy dark fantasy, a little funny.
Forbidden: text, letters, logos, watermarks, blood, crosses, real heraldic symbols, animals inside the pattern.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_keykeeper_newt` — №12 Тритон-ключник
Холст 64×40 (исключение из класса S, D-025), голова влево. GDD: «Тащит в пасть всё блестящее. Однажды у него нашли ключ». Ключик во рту — 2–3 пикселя латуни.

```
Create a pixel art game sprite of a magical newt, the Keykeeper Newt. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible, swimming with a long flat tail. A small newt with dark teal-green skin, a pale amber speckled belly line, a frilly crest along its back and big shiny curious eyes. It holds a tiny old brass key in its mouth. Sneaky, cute, mischievous.
Light: cold moonlight rim on the crest and head, the brass key catches a warm glint, deep navy shadows.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 64x40 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: dark teal, jade green, moss green, pale amber for the belly speckles, brass gold for the key, navy. No red.
Mood: quiet, cozy dark fantasy, a little funny.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_shadow_ray` — №13 Тенекрылка
Холст 96×56. Вид 3/4 сверху, скользит влево, хвост вправо. GDD: «Скользит под водой, как тень от облака». Почти чёрный силуэт с тонкой синей кромкой.

```
Create a pixel art game sprite of a magical ray, the Shadow Ray. Landscape image 1536x1024.

A manta-like ray gliding to the LEFT, seen from above at a three-quarter angle, wide wings spread, a long thin tail trailing to the right. Its body is nearly black deep navy, like a shadow, with soft smoky patches; the very edges of the wings glow with a thin cold cobalt-blue line; two small pale eyes at the front. Silent, elegant, mysterious.
Light: mostly dark; a thin bright blue rim along the wing edges.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 96x56 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: near-black navy, deep indigo, cobalt, a little pale blue for the rim. No warm colors.
Mood: quiet, mysterious, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_crimson_carp` — №14 Багровый карп
Холст 96×56, голова влево. Событие «Багровая луна» — единственное существо на ряду crimson. GDD: «При обычном свете он серый, как камень» — серые пятна на голове.

```
Create a pixel art game sprite of a magical fish, the Crimson Carp. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible. A large koi-like carp with long flowing fins, a long trailing tail and two small whiskers. It glows under a red moon: big scales in deep crimson and rose red with brighter edges and dark wine-red shadows; a few stone-grey patches on the head (in normal light it is grey as stone); a calm dignified eye. Rare, magical, beautiful.
Light: crimson moonlight from above: bright rose-red highlights on the top, dark wine-red and navy shadows below.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 96x56 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: crimson, rose red, dark wine red, stone grey, navy. No orange, no gold.
Mood: quiet, magical, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood, gore, wounds.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `cr_ghost_sturgeon` — №15 Призрачный осётр
Холст 128×80, голова влево. Легендарное. GDD: «Сквозь него видно дно». Ряд ghost (лаванда/фиолет). **Фон зелёный**, не пурпурный: пурпур съел бы края лаванды. Полупрозрачность — modulate в Godot.

```
Create a pixel art game sprite of a magical fish, the Ghost Sturgeon. Landscape image 1536x1024.

Side view, head pointing LEFT, the whole body visible. A huge ghostly sturgeon: long pointed snout, small barbels, rows of bony diamond-shaped scutes along its back and sides, a long shark-like upper tail lobe. It is a gentle spirit: glowing pale lavender outline and scutes, the body inside darker violet-indigo that looks semi-transparent, faint wisps of mist trailing from the fins and the tail. Calm, ancient, eerie but gentle, not scary.
Light: it glows by itself: brightest pale lavender on the outline and the scutes, deep indigo inside.

Single isolated game sprite, centered, the whole body visible, nothing else in the image: no water, no bubbles.
Background: perfectly flat solid pure green #00FF00 (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 128x80 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: lavender, soft violet, indigo, deep navy, a touch of pale blue-white for the brightest glow. No red, no orange, no green on the creature.
Mood: quiet, ancient, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood, skeleton, bones, skulls.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `relic_key` — Ржавый ключ от южной башни
Иконка 32×32. «Ржавый ключ от южной башни» — фрагмент 1 истории Эльсы.

```
Create a pixel art game item icon: an old rusty key. Square image 1024x1024.

An old rusty iron key lying diagonally (the bow at the top left, the bit at the bottom right). Big ornate looped bow shaped like a swirl, a long shaft, a chunky bit. Dark iron grey with rust brown and a few warm orange rust spots, a little green moss: it lay in the water for years.
Light: cold pale-blue moonlight highlights on the metal edges, deep navy shadow.

Single isolated game icon, centered, the whole object visible, nothing else in the image: no table, no water, no hands.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 32x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: dark iron grey, rust brown, dull orange, moss green, pale blue highlights, navy. No red.
Mood: quiet, nostalgic, cozy dark fantasy; a precious relic from a drowned castle.
Forbidden: text, letters, logos, watermarks, blood, religious symbols, crosses.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `relic_horse` — Деревянная лошадка
Иконка 32×32. «Деревянная лошадка» — фрагмент 2. Игрушка на качалке, смотрит влево.

```
Create a pixel art game item icon: a small wooden toy horse. Square image 1024x1024.

A child's small old wooden rocking horse toy, side view, facing LEFT. Worn painted wood: faded warm brown body, a darker carved mane and tail, a faded teal saddle, small chips and water stains. Touching and nostalgic.
Light: pale moonlight highlights on the top edges, warm wood in the middle, deep navy shadow under the rocker.

Single isolated game icon, centered, the whole object visible, nothing else in the image: no table, no water, no hands.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 32x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: warm wood browns, faded beige, a little faded teal, navy. No red.
Mood: quiet, nostalgic, cozy dark fantasy; a precious relic from a drowned castle.
Forbidden: text, letters, logos, watermarks, blood, religious symbols, crosses.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `relic_medallion` — Медальон с портретом лорда
Иконка 32×32. «Медальон с портретом лорда» — фрагмент 3. Портрет — тёмный силуэт без черт лица (при 32 px всё равно не читается).

```
Create a pixel art game item icon: an old medallion with a tiny portrait. Square image 1024x1024.

An oval brass medallion on a short broken chain, front view. In the center a small oval painted miniature portrait of a nobleman in dark clothes, shown as a simple dark head-and-shoulders silhouette on a faded blue background, no facial details. The frame has a simple leaf ornament, tarnished, with a little green patina.
Light: pale moonlight glint on the top of the frame, deep navy shadow at the bottom.

Single isolated game icon, centered, the whole object visible, nothing else in the image: no table, no water, no hands.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 32x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: brass gold, tarnished bronze, green patina, faded blue, navy, pale highlights. No red.
Mood: quiet, nostalgic, cozy dark fantasy; a precious relic from a drowned castle.
Forbidden: text, letters, logos, watermarks, blood, religious symbols, crosses.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `relic_spyglass` — Подзорная труба смотрителя
Иконка 32×32. «Подзорная труба смотрителя» — фрагмент 4, финал главы 1. По диагонали: окуляр снизу слева, линза сверху справа.

```
Create a pixel art game item icon: an old brass spyglass. Square image 1024x1024.

A brass spyglass (small telescope) extended in three sections, lying diagonally: the eyepiece at the bottom left, the wide lens at the top right. Worn brass with small dents and green patina, a dark leather wrap on the widest section, the lens glints pale blue.
Light: cold moonlight highlights along the top of the tube, the lens glints pale blue, deep navy shadow below.

Single isolated game icon, centered, the whole object visible, nothing else in the image: no table, no water, no hands.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 32x32 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: brass gold, bronze, dark leather brown, green patina, pale blue, navy. No red.
Mood: quiet, nostalgic, cozy dark fantasy; a precious relic from a drowned castle.
Forbidden: text, letters, logos, watermarks, blood, religious symbols, crosses.
Use the attached reference image only for style, palette and lighting, not for composition.
```

## Пакет 4 — Брук, Эльса, лавка, Ров Вельмора, иконки, UI, фазы луны, логотип (Э0.4.5)

NPC — холст 96×128, как у Ирвена. Лавка и ров — панорамы шириной 640, как «Лунный берег»; небо, луна и облака во рву общие с берегом, поэтому в слоях рва их нет (D-026).
**Эльса (`char_elsa_idle`) — на зелёном фоне `#00FF00`**, остальные на пурпурном.
**Без надписей.** Рамки, кнопки и логотип рисуются без текста: надписи делает `Label` (локализация, генераторы портят кириллицу). Логотип — только эмблема, название под ней (D-027).
**Листы иконок** (наживки, улучшения, навигация, фазы луны, кнопка): предметы с широкими промежутками, скрипт сам находит их и режет; порядок — по строкам слева направо, как в промпте.
`ui_moon_phases_lg` делается из того же исходника, что `ui_moon_phases`. Временный лист фаз агент строит из готовой луны `env_moon_full` (D-028); пришёл финал луны — лист фаз пересобирается.
Кот в лодке — отдельный ассет не нужен: тот же `char_cat_idle` на носу `prop_boat` (D-026).

### `char_brook_idle` — Брук стоит (idle)
Холст 96×128, привязка — низ по центру. Рисуется в полный рост: в лавке прилавок `env_shop_counter` — отдельный слой поверх ног. Тёплый свет свечей слева, холодный ободок луны из окна справа.

```
Create a pixel art game sprite of Brook, a gnome trader who buys fish and odd things in a hut carved into a sea cliff. Portrait image 1024x1536.

Pose: standing, full figure, front three-quarter view turned slightly to the left, looking at the viewer with a sly friendly grin. One hand on his round belly, the other raised holding a small brass magnifying loupe, as if about to appraise a fish. Short and stocky: big head, broad shoulders, short legs, heavy boots.
Look: round brass goggles pushed up on his forehead; a bushy ginger beard with grey streaks, its end tied with a brass bead; a big round nose and rosy cheeks; a small knitted dark blue cap; rolled-up sleeves of a moss-green shirt; a thick brown leather apron with brass buckles and pockets full of small tools; a coin pouch on the belt.
Light: warm amber candle light from the lower left on his face, beard and apron; a thin cold blue moonlight rim on the right edges from a window behind him.

Single isolated game sprite, the whole figure visible from the cap to the boots and centered, nothing else in the image: no counter, no shelves, no floor.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow on the ground, no floor, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 96x128 pixels, so avoid tiny details.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: limited, about 48 colors. Warm browns, leather, brass and amber, a ginger beard, peach skin; deep night blues and navy in the shadows; a touch of moss green. No crimson, no bright red.
Lighting: warm candle key light from the lower left, cold blue moon rim from the upper right; shadows go into deep navy, never pure black.
Mood: cozy, funny and kind-hearted shopkeeper of a cozy dark fantasy world, like a 1980s fantasy book illustration rendered as a pixel art game.
Forbidden: text, letters, logos, watermarks, blood, skulls, crosses, religious symbols, weapons.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `char_elsa_idle` — Эльса (idle)
Холст 96×128, привязка — низ по центру, смотрит влево (на Ирвена: она появляется у края причала справа). Ряд ghost. **Фон зелёный**, не пурпурный: пурпур съест края лаванды (как у призрачного осётра). Полупрозрачность и колыхание — в Godot.

```
Create a pixel art game sprite of Elsa, the gentle ghost of the old castle's key keeper. Portrait image 1024x1536.

Pose: floating upright just above the ground, full figure, three-quarter view turned to the LEFT, head slightly bowed, looking down to the left with a sad, calm, kind expression. Both hands folded in front of her waist, holding a big ring of old keys.
Look: a young woman in a long simple medieval dress with a high collar and a shawl over her shoulders; long hair in a loose braid; the end of the braid and the hem of the dress dissolve into soft wisps of mist, no feet visible. A kind, slightly sad face drawn simply, eyes half-closed.
She is a ghost: she glows by herself with pale lavender light; the inner areas are darker violet-indigo and look semi-transparent; the brightest pale lavender-white is on the edges of the hair, the shoulders and the keys.

Single isolated game sprite, the whole figure visible and centered, nothing else in the image: no ground, no water, no pier.
Background: perfectly flat solid pure green #00FF00 (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 96x128 pixels, so avoid tiny details.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: lavender, soft violet, indigo, deep navy, a touch of pale blue-white for the brightest glow. No red, no orange, no green on the character.
Lighting: she is her own light source; a thin cold moonlight rim on the right edges.
Mood: quiet, melancholic, tender; sad but never scary, suitable for all ages.
Forbidden: text, letters, logos, watermarks, blood, skulls, skeletons, empty eye sockets, horror faces, chains on the body, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_shop_back` — Лавка Брука: задняя стена с окном
Слой 640×360, непрозрачный. Окно на залив и замок — по центру (в телефонном кадре), полки уходят к краям панорамы. Нижняя четверть — пустой пол: перед ним встанут Брук и прилавок. Из 1536×1024 берётся середина по высоте (~84 %).

```
Create a pixel art background for a 2D game: the inside of a gnome trader's shop carved into a sea cliff, at night. Landscape image 1536x1024.

Straight-on front view of the back wall, like a stage set. In the center, a big round window with small leaded panes; through it we see the night bay: a full moon, the ruined gothic castle Velmor on an island far away with a few amber windows, calm water with a moonlit path. Around the window: rough rock walls with thick wooden beams; crooked wooden shelves on the left and right full of glass jars (some with faintly glowing teal-green and blue contents), bottles, coils of fishing line, a few hanging dried fish, nets and cork floats on hooks, old lanterns and burning candles with warm amber light; a hanging brass scale.
The lower quarter of the image is a plain dark wooden floor and the base of the wall with nothing on it (a counter will be placed in front later). No characters, no counter, no table.
The whole image is filled, no empty areas. Keep the main composition in the middle 60% of the width; the left and right edges just continue the shelves. Keep important things away from the top and bottom 8% of the image.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: warm wood browns, amber candle light, dark rock greys; deep night blues and cobalt in the window and in the shadows; a teal-green glow in a few jars. No crimson.
Lighting: warm candle light from the shelves, cold blue moonlight through the window onto the middle of the room; shadows go into deep navy, never pure black.
Mood: a cozy, cluttered, warm hideout on a cold night; cozy dark fantasy, like a 1980s fantasy book illustration rendered as a pixel art game.
Forbidden: text, letters, numbers, labels on jars, signs, logos, watermarks, blood, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_shop_counter` — Лавка Брука: прилавок
Слой 640×128, низ — край экрана сцены. Середина столешницы пустая: на неё кладётся улов при продаже, с неё сыплются монеты (GDD §9). Используется нижние ~30 % картинки.

```
Create a pixel art foreground layer for a 2D game: the wooden counter of a gnome trader's shop, seen straight from the front. Landscape image 1536x1024.

A long, thick, old wooden counter that spans the entire width of the image from the left edge to the right edge. Its top is a heavy plank with worn edges and a few nicks; the front is made of vertical dark boards with iron bands and rivets. Small things stand only near the ends of the counter top: on the left, a brass balance scale and a small stack of silver coins; on the right, a candle in an iron holder with a warm amber flame and a small jar with a glowing teal-green moth. The middle 60% of the counter top is empty.
The counter occupies only the lower 30% of the image; its bottom is cut by the bottom edge of the image.
Everything that is not part of this layer is perfectly flat solid magenta #FF00FF (or real transparency). No characters, no wall, no shelves.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: warm wood browns, dark iron, brass and amber candle light, deep navy shadows; one small teal-green glow. No crimson.
Lighting: warm candle light from the right end and from above; shadows go into deep navy, never pure black.
Mood: cozy, cluttered, warm.
Forbidden: text, letters, numbers, signs, price tags, logos, watermarks, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_moat_castle` — Ров Вельмора: стены замка
Слой 640×360, низ — линия воды. Небо, луна и облака во рву общие с «Лунным берегом» (D-026): верхние 35 % картинки — пустое небо, между башнями — просвет для луны. Проём ворот тёмный, не сквозной. Воду не рисовать — она отдельным слоем. Используются нижние ~84 % картинки.

```
Create a pixel art parallax background layer for a 2D game: the walls of the half-sunken gothic castle Velmor seen up close from its flooded moat. Landscape image 1536x1024.

Massive dark stone walls rise straight out of the water and span the whole width of the image, from the left edge to the right edge. Two round towers stand near the left and right edges; between them a lower curtain wall with battlements. In the center of the wall, a huge pointed arched gateway, half under water, with a broken raised iron portcullis; the gateway opening is filled with the deep dark navy shadow of the gate passage, it is NOT see-through. Narrow arched windows, a few of them still glowing warm amber; ivy and moss hanging from the battlements, wet dark stains near the waterline, cold mist at the base.
Composition: the walls occupy only the LOWER 65% of the image; the upper 35% of the image is empty sky. The tops of the two towers reach up to about 35% from the top, the battlements of the curtain wall are lower, at about 50% from the top, so there is a wide gap of empty sky in the middle (the moon will be placed there later). The bottom edge of the image is the waterline: a straight horizontal cut, and NO water is drawn.
Everything that is not part of this layer is perfectly flat solid magenta #FF00FF (or real transparency). The whole sky above the walls and between the towers is flat magenta. No moon, no clouds, no characters.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: cool stone greys, night blues, cobalt, deep navy; moss and ivy greens; warm amber only in a few windows. No crimson.
Lighting: full moon key light from the upper right gives a thin cold blue-white rim light on right and top edges; shadows go into deep navy, never pure black.
Mood: quiet, melancholic, cozy dark fantasy, like a 1980s dark fantasy book cover rendered as a pixel art game.
Forbidden: text, letters, logos, watermarks, blood, skulls, scary gargoyles, crosses on the towers or anywhere, religious symbols, flags with emblems.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_moat_water` — Ров Вельмора: вода
Слой 640×300, непрозрачный, от линии воды вниз. Темнее и зеленее, чем в заливе. Рябь и лунную дорожку оживит шейдер воды (Э3.4). Используется верхние ~70 % картинки.

```
Create a pixel art background layer for a 2D game: the still dark water of a flooded castle moat at night, seen from slightly above. Landscape image 1536x1024.

The whole image is water: no shore, no walls, no sky. Calm, almost still water in deep navy and dark teal-green, darker toward the bottom. In the upper part, long soft reflections of dark castle walls broken by ripples and two or three warm amber reflections of lit windows; a shimmering pale blue moonlit path in the middle going down. Thin horizontal ripple lines, a few floating leaves, a few faint green glowing dots of tiny water creatures.
The image is fully filled, no empty areas.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: deep navy, cobalt, dark teal-green, pale blue moon highlights; tiny amber reflections only. No crimson.
Lighting: moonlight from above; shadows go into deep navy, never pure black.
Mood: quiet, still, mysterious, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood, skulls, creatures, characters, boats.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_moat_ledge` — Ров Вельмора: обломки ворот (место рыбалки)
Холст 256×160, привязка — низ (линия воды). Во рву Ирвен сидит не на причале, а на обломках рухнувших ворот: тот же спрайт idle, ноги свешены с правого края. Фонарь — на погнутом пруте решётки.

```
Create a pixel art game sprite: a fishing spot made of the fallen stones of a castle gate in a flooded moat. Landscape image 1536x1024.

Side view. A low pile of huge fallen carved stone blocks sticking out into the water from the left, forming a flat top ledge about one third of the image height above the bottom. The right end of the ledge is a clean flat block edge (an old wizard will sit there with his legs hanging down). On the left part of the ledge, a bent iron bar from a broken gate grille with an old iron lantern hanging from it, glowing warm amber. Moss, ivy and small ferns in the cracks, wet dark stones near the bottom. The bottom of the stones is a straight horizontal waterline at the bottom edge of the image; NO water is drawn.
The ledge spans about 80% of the image width.

Single isolated game sprite, nothing else in the image: no characters, no boat, no castle, no sky.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 256x160 pixels.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: cool stone greys, deep navy, moss greens, dark iron; warm amber only in the lantern and its glow on nearby stones. No crimson.
Lighting: full moon key light from the upper right gives a thin cold blue-white rim light on right and top edges; shadows go into deep navy, never pure black. A small warm lantern glow on the left.
Mood: quiet, melancholic, cozy dark fantasy, like a 1980s dark fantasy book cover rendered as a pixel art game.
Forbidden: text, letters, logos, watermarks, blood, skulls, crosses, religious symbols, carved faces.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `prop_boat` — Лодка (починенная)
Холст 128×48, привязка — низ (линия воды), нос вправо. Ставится у обломков ворот во рву, плывёт по карте. Кот на носу — тот же спрайт `char_cat_idle` поверх лодки (GDD §13.1, D-026).

```
Create a pixel art game sprite of a small old wooden rowboat. Landscape image 1536x1024.

Side view, the bow (front) pointing RIGHT and slightly raised, the stern on the left. A short, wide rowboat made of overlapping dark weathered planks, freshly repaired: a few lighter new planks and patches with visible nails, a rope band along the rim. Two oars resting inside along the boat, a coiled rope, a small iron ring on the bow. The boat is empty: no people, no animals.
The hull is drawn down to a straight horizontal waterline; the part below the waterline is NOT drawn.

Single isolated game sprite, centered, the whole boat visible, nothing else in the image: no water, no reflection.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clear silhouette with large pixel clusters: the sprite will be downscaled to 128x48 pixels.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: dark weathered wood browns, a few lighter new planks, dark iron, rope beige-brown, deep navy shadows. No crimson.
Lighting: full moon key light from the upper right gives a thin cold blue-white rim light on right and top edges; shadows go into deep navy, never pure black.
Mood: quiet, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, blood, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `env_moat_foreground` — Ров Вельмора: передний план
Слой 640×240, привязка — низ. Заполнены только нижние углы, середина свободна: там зона заброса и вываживания. Используется нижние ~56 % картинки.

```
Create a pixel art foreground parallax layer for a 2D game: the near edge of a flooded castle moat at night. Landscape image 1536x1024.

Only the bottom left and bottom right corners are filled. Bottom left: a broken carved stone column lying on its side and a few square fallen stones with moss, a couple of water lily pads with a small closed pale flower. Bottom right: a heap of tumbled wall blocks with ivy, tall reeds and cattails leaning inward, one lily pad glowing faint jade green. The middle 60% of the width stays empty.
Everything sits in the lower 55% of the image; the objects are cut by the bottom edge of the image.
Everything that is not part of this layer is perfectly flat solid magenta #FF00FF (or real transparency). No water surface, no sky, no characters.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: dark stone greys, deep navy, mossy and forest greens, a touch of jade glow; the foreground is darker than the scene behind it. No crimson.
Lighting: a thin cold moonlight rim on the top edges; the rest are dark silhouettes.
Mood: quiet, melancholic, cozy dark fantasy, like a 1980s dark fantasy book cover rendered as a pixel art game.
Forbidden: text, letters, logos, watermarks, blood, skulls, crosses, religious symbols, carved faces.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_bait_icons` — Наживки, лист из 5 кадров
Лист 160×32 (5 кадров по 32×32). Порядок — GDD §8.3: червяк, светлячок, лунный мотыль, мох с руин, звёздная крошка.

```
Create a pixel art game item icon sheet: five fishing baits. Landscape image 1536x1024.

Exactly FIVE separate items in one horizontal row, evenly spaced with wide gaps, all about the same size. From left to right:
1) an earthworm: a plump pinkish-brown worm curled into a loose S shape;
2) a firefly: a small round beetle with folded dark wings and a big glowing warm amber-yellow tail;
3) a moon moth: a pale moth seen from above with wide pale blue-white wings and soft lavender eye-spots;
4) ruin moss: a small clump of bright green moss growing on a broken piece of grey carved stone;
5) star dust: a small corked glass vial full of tiny glittering pale blue and white sparkles, glowing softly.

Nothing else in the image. Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Each item will be downscaled to 32x32 pixels: bold simple shapes, big pixel clusters, a dark navy outline.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: navy outlines and shadows; pinkish-brown, amber, pale blue, lavender, moss green, stone grey. No crimson.
Lighting: a thin cold moonlight highlight on the upper right of each item.
Forbidden: text, letters, numbers, labels, logos, watermarks, blood.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_upgrade_icons` — Улучшения, лист из 6 кадров
Лист 192×32 (6 кадров по 32×32), исходник — сетка 3×2. Порядок — ветки GDD §8.2: удилище, катушка, фонарь, корзина, сеть, лодка.

```
Create a pixel art game icon sheet: six upgrade icons for a fishing workshop. Landscape image 1536x1024.

Exactly SIX separate items in a grid of 3 columns and 2 rows, evenly spaced with wide gaps, all about the same size.
Top row, left to right: 1) a fishing rod: a wooden rod with brass rings drawn diagonally from the bottom left to the top right, a short line with a small float hanging from the tip; 2) a fishing reel: a round brass and dark iron reel with a small handle, front view; 3) an old iron lantern with a warm amber flame and a carrying ring on top.
Bottom row, left to right: 4) a woven wicker fishing basket with a lid and a leather strap; 5) a folded fishing net with round cork floats; 6) a small wooden rowboat in side view, bow to the right.

Nothing else in the image. Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Each item will be downscaled to 32x32 pixels: bold simple shapes, big pixel clusters, a dark navy outline.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: navy outlines and shadows; wood browns, brass and amber, dark iron, wicker tan, cork. No crimson.
Lighting: a thin cold moonlight highlight on the upper right of each item.
Forbidden: text, letters, numbers, labels, logos, watermarks, blood, hooks with bait.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_nav_icons` — Иконки навигации, лист из 5 кадров
Лист 160×32 (5 кадров по 32×32). Нижняя полоса причала (GDD §16.2): Корзина, Книга вод, Лавка, Карта, Настройки.

```
Create a pixel art game icon sheet: five navigation buttons icons for a cozy fishing game. Landscape image 1536x1024.

Exactly FIVE separate icons in one horizontal row, evenly spaced with wide gaps, all about the same size. From left to right:
1) a woven wicker fish basket, front view, with a fish tail sticking out of it;
2) a thick closed old book with a dark blue leather cover, brass corners and a small fish shape embossed on the cover;
3) a small round hut door set into a rock, with a warm glowing round window and a little hanging lantern (a gnome's shop);
4) a half-unrolled old parchment map with a dotted path and a tiny drawn boat;
5) a dark iron cogwheel with a brass center.

Nothing else in the image. Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Each icon will be downscaled to 32x32 pixels: bold simple shapes, big pixel clusters, a dark navy outline.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: navy outlines and shadows; wicker tan, dark blue leather, brass and amber, rock grey, warm peach-tan parchment, dark iron. No crimson.
Lighting: a thin cold moonlight highlight on the upper right of each icon.
Forbidden: text, letters, numbers, logos, watermarks, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_panel_frame` — Рамка панели (9-slice)
Холст 96×96 для `NinePatchRect`, поля 24 px со всех сторон: углы с орнаментом не тянутся, стороны и пергамент в середине тянутся (лучше плиткой). Пергамент — ряды skin/wood (D-024). Основа всех окон: корзина, лавка, календарь, настройки, диалог Эльсы.

```
Create a pixel art UI panel for a 2D game: an empty square window frame, front view. Square image 1024x1024.

The frame fills almost the whole image, leave a thin magenta margin around it. Frame: dark wrought iron, about 9% of the panel width thick, with one rivet in the middle of each side and small curled leaf-and-wave ornaments in the four corners; a thin cold blue moonlit highlight on the top and right edges of the iron. Inside: one big empty area of aged parchment in warm peach-tan (close to #e0a982) with darker tan worn edges and corners (close to #b88a52) and a very subtle even texture, no stains in the middle.
Between the corners, the four sides of the frame are plain and uniform: the panel will be stretched as a 9-slice, the corners stay and the sides repeat.
Absolutely no text, letters, numbers or symbols anywhere.

Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Clean large pixel clusters: the panel will be downscaled to 96x96 pixels.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: dark iron greys and navy, cobalt, warm peach-tan parchment, dark tan. No crimson, no bright yellow, no pure white.
Lighting: moon key light from the upper right, shadows go into deep navy, never pure black.
Mood: quiet, cozy dark fantasy.
Forbidden: text, letters, logos, watermarks, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_button` — Кнопка, 2 состояния
Лист 128×24 (2 кадра по 64×24): обычная и нажатая. `StyleBoxTexture`, поля 8 px. Надпись — `Label` в Godot (локализация). Неактивная — затемнение через modulate.

```
Create a pixel art UI sheet for a 2D game: two states of the same empty wide button. Landscape image 1536x1024.

Exactly TWO buttons side by side with a wide gap, the same size, each about 2.7 times wider than tall (a wide rectangle with small cut corners).
Left, normal: a dark wrought iron rim with a tiny rivet at each end; the face is aged parchment in warm peach-tan (close to #e0a982), slightly raised, with a lighter line along the top inner edge and darker tan (close to #b88a52) along the bottom inner edge; a thin cold blue moonlit highlight on the top of the iron rim.
Right, pressed: the same button pushed in: the parchment face is darker tan, light and shadow are swapped (dark along the top inner edge), no moon highlight.
Both faces are completely empty: no text, letters, numbers or icons.

Nothing else in the image. Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Clean large pixel clusters: each button will be downscaled to 64x24 pixels.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: dark iron greys and navy, warm peach-tan parchment, dark tan. No crimson, no bright yellow, no pure white.
Lighting: moon key light from the upper right, shadows go into deep navy, never pure black.
Forbidden: text, letters, numbers, logos, watermarks, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_action_button` — Большая кнопка действия
Холст 64×64, центр. Внизу по центру причала (GDD §16.2). Середина пустая: иконку действия и дугу прогресса (`TextureProgressBar`, радиальный) Godot кладёт поверх.

```
Create a pixel art UI element for a 2D game: a big round action button, front view. Square image 1024x1024.

A circular button filling most of the image: a thick dark wrought iron ring with eight small rivets evenly around it and a thin cold blue moonlit highlight on its upper right; inside, a slightly domed deep navy-blue glass disc with a soft pale blue glow in the center, like moonlight seen through water, and one small bright highlight in the upper right. The center of the disc is empty: an icon will be placed on it later.
Absolutely no text, letters, numbers or symbols anywhere.

Single isolated UI element, centered, nothing else in the image.
Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big clean shapes: the button will be downscaled to 64x64 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: dark iron greys, navy, cobalt, pale blue glow. No crimson, no warm colors.
Lighting: moon key light from the upper right, shadows go into deep navy, never pure black.
Forbidden: text, letters, numbers, logos, watermarks, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_tension_frame` — Рамка шкалы натяжения
Холст 20×160, центр. Справа на причале во время вываживания (GDD §5.4). Внутри пустой тёмный паз: заливку рисует `TextureProgressBar` снизу вверх, цвета зон — в Godot.

```
Create a pixel art UI element for a 2D game: an empty vertical gauge for fishing line tension, front view. Portrait image 1024x1536.

A very tall and narrow gauge standing in the center and filling the full image height, about 8 times taller than wide: a dark wrought iron frame with a small round rivet cap at the top and at the bottom end and a few rivets along the sides; inside, one long empty dark navy slot (the game draws the fill later). A thin cold blue moonlit highlight on the right edge of the iron. Leave magenta on the left and right.
Absolutely no text, numbers, marks or symbols.

Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Clean large pixel clusters: the gauge will be downscaled to 20x160 pixels.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: dark iron greys, navy, cobalt, pale blue highlight. No crimson, no warm colors.
Forbidden: text, letters, numbers, logos, watermarks, skulls, crosses, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_moon_phases` — 8 фаз луны, HUD
Лист 128×16 (8 кадров по 16×16), иконка луны в HUD рядом с таймером. Исходник — сетка 4×2. Порядок — GDD §7.1: новолуние, растущий серп, первая четверть, растущая, полнолуние, убывающая, последняя четверть, убывающий серп. Тёмная часть диска — тёмно-синяя с тонким ободком, чтобы новолуние было видно. Временный исходник агент собирает из `env_moon_full` скриптом `tools/art/moon_phases_src.py` (D-028).

```
Create a pixel art game icon sheet: the eight phases of the moon. Landscape image 1536x1024.

Exactly EIGHT moon discs of the same size in a grid of 4 columns and 2 rows, evenly spaced with wide gaps. Every disc is the same pale moon with a few soft grey-blue craters; the unlit part of every disc is dark navy blue with a thin faint blue rim, so all eight are full circles of the same size.
Top row, left to right: 1) new moon: a fully dark disc with only the faint rim; 2) waxing crescent: a thin lit sliver on the RIGHT side; 3) first quarter: the right half lit; 4) waxing gibbous: lit except a thin dark crescent on the left.
Bottom row, left to right: 5) full moon: fully lit; 6) waning gibbous: lit except a thin dark crescent on the right; 7) last quarter: the left half lit; 8) waning crescent: a thin lit sliver on the LEFT side.

Nothing else in the image: no stars, no clouds, no glow halo. Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Each disc will be downscaled to 16x16 and 32x32 pixels: simple shapes, a clean sharp edge between light and dark.

Style: 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no text.
Palette: pale moon white and soft blue-grey for the lit part, deep navy for the dark part. No warm colors.
Forbidden: text, letters, numbers, faces on the moon, logos, watermarks, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```

### `ui_logo_emblem` — Логотип: эмблема без текста
Холст 160×128, центр. Только эмблема: генераторы портят кириллицу, а название ещё и локализуется. Надпись «Лунный улов» — `Label` пиксельным шрифтом под эмблемой (шрифт — Э5.1), D-027. Экран загрузки и титул (GDD §16.1).

```
Create a pixel art game logo emblem with no text. Square image 1024x1024.

A badge-like round composition: a big glowing full moon; in front of its lower half, the dark silhouette of the ruined gothic castle Velmor on a small rocky island with two warm amber windows; calm water in front with a bright moonlit path. A magical glowing fish (pale blue with soft jade-green glowing spots) leaps in a graceful arc across the face of the moon; a single thin fishing line curves up to it from the lower left. The whole emblem is wrapped in an oval of soft cold mist at its edges.

Single isolated emblem, centered, nothing else in the image. Background: perfectly flat solid magenta #FF00FF (or real transparency), no shadow, no gradient.
Big bold shapes: the emblem will be downscaled to 160x128 pixels, so keep it simple and readable.

Style: detailed 16-bit pixel art, crisp square pixels on a strict grid, no anti-aliasing, no blur, no soft gradients, no noise, no text.
Palette: night blues, cobalt, pale moon white, cool stone greys; a jade-green glow on the fish; warm amber only in two windows. No crimson.
Lighting: the moon is the light source: cold blue-white rim light on the castle, the fish and the waves.
Mood: quiet, melancholic, cozy dark fantasy, like a 1980s dark fantasy book cover rendered as a pixel art game.
Forbidden: text, letters, numbers, logos of other brands, watermarks, blood, skulls, crosses on the spires or anywhere, religious symbols.
Use the attached reference image only for style, palette and lighting, not for composition.
```
