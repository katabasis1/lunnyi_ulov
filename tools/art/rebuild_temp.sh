#!/usr/bin/env bash
# Пересборка ВРЕМЕННЫХ ассетов из исходников агента (Pod: art_sources/, вне репозитория).
# Финалы из ChatGPT обрабатываются отдельно: python3 tools/art/process_art.py --incoming
# Запуск из корня lunnyi_ulov/:  bash tools/art/rebuild_temp.sh [путь_к_art_sources]
set -e
SRC="${1:-../art_sources}"
P="python3 tools/art/process_art.py"
# --- Пакет 1 (Э0.4.2) ---
$P char_irven_idle      "$SRC/batch1/char_irven_idle.png"
$P char_cat_idle        "$SRC/batch1/char_cat_idle.png"
$P env_shore_sky        "$SRC/batch1/env_shore_sky.png"
$P env_moon_full        "$SRC/batch1/env_moon_full.png"
$P env_shore_clouds     "$SRC/batch1/env_shore_clouds.png"     --crop 0,0.33,1,0.68
$P env_shore_castle     "$SRC/batch1/env_shore_castle.png"     --crop 0,0,1,0.852
$P env_shore_cliffs     "$SRC/batch1/env_shore_cliffs.png"
$P env_shore_water      "$SRC/batch1/env_shore_water.png"
$P env_shore_pier       "$SRC/batch1/env_shore_pier.png"
$P env_shore_foreground "$SRC/batch1/env_shore_foreground.png"
python3 tools/art/compose_mock.py shore docs/art_mocks/shore_mock_latest.png --scale 1
# --- Пакет 2 (Э0.4.3) ---
$P prop_bobber_default  "$SRC/batch2/prop_bobber_default.png"
$P prop_rod_basic       "$SRC/batch2/prop_rod_basic.png"
$P ui_catch_card_frame  "$SRC/batch2/ui_catch_card_frame.png"
$P ui_rarity_gems       "$SRC/batch2/ui_rarity_gems.png"
$P ui_catch_stamps      "$SRC/batch2/ui_catch_stamps.png"
$P ui_icon_coin         "$SRC/batch2/ui_icon_coin.png"
$P ui_icon_coin_lg      "$SRC/batch2/ui_icon_coin.png"
$P ui_icon_pearl        "$SRC/batch2/ui_icon_pearl.png"
$P ui_icon_pearl_lg     "$SRC/batch2/ui_icon_pearl.png"
$P cr_moon_roach        "$SRC/batch2/cr_moon_roach.png"
$P cr_mist_ruffe        "$SRC/batch2/cr_mist_ruffe.png"
$P cr_tile_hermit       "$SRC/batch2/cr_tile_hermit.png"
# пакет 3 (Э0.4.4): силуэты sil_* строятся сами после каждого существа
$P cr_lanternfish       "$SRC/batch3/cr_lanternfish.png"
$P cr_whisper_eel       "$SRC/batch3/cr_whisper_eel.png"
$P cr_nightlight_jelly  "$SRC/batch3/cr_nightlight_jelly.png"
$P cr_stargazer         "$SRC/batch3/cr_stargazer.png"
$P cr_knight_pike       "$SRC/batch3/cr_knight_pike.png"
$P cr_lord_of_bay       "$SRC/batch3/cr_lord_of_bay.png"
$P cr_rust_perch        "$SRC/batch3/cr_rust_perch.png"
$P cr_crest_flounder    "$SRC/batch3/cr_crest_flounder.png"
$P cr_keykeeper_newt    "$SRC/batch3/cr_keykeeper_newt.png"
$P cr_shadow_ray        "$SRC/batch3/cr_shadow_ray.png"
$P cr_crimson_carp      "$SRC/batch3/cr_crimson_carp.png"
$P cr_ghost_sturgeon    "$SRC/batch3/cr_ghost_sturgeon.png"
$P relic_key            "$SRC/batch3/relic_key.png"
$P relic_horse          "$SRC/batch3/relic_horse.png"
$P relic_medallion      "$SRC/batch3/relic_medallion.png" --crop 0.2,0.3,0.8,0.9
$P relic_spyglass       "$SRC/batch3/relic_spyglass.png"
python3 tools/art/compose_mock.py fishing docs/art_mocks/fishing_mock_latest.png --scale 2
python3 tools/art/compose_mock.py catch   docs/art_mocks/catch_mock_latest.png   --scale 2
python3 tools/art/compose_mock.py catch_legendary docs/art_mocks/catch_legendary_mock_latest.png --scale 2
python3 tools/art/creature_sheet.py docs/art_mocks/creatures_overview_latest.png
# --- Пакет 4 (Э0.4.5) ---
$P char_brook_idle      "$SRC/batch4/char_brook_idle.png"
$P char_elsa_idle       "$SRC/batch4/char_elsa_idle.png"
$P env_shop_back        "$SRC/batch4/env_shop_back.png"
$P env_shop_counter     "$SRC/batch4/env_shop_counter.png"
$P env_moat_castle      "$SRC/batch4/env_moat_castle.png"      --crop 0,0,1,0.985
$P env_moat_water       "$SRC/batch4/env_moat_water.png"
$P env_moat_ledge       "$SRC/batch4/env_moat_ledge.png"
$P prop_boat            "$SRC/batch4/prop_boat.png"
$P env_moat_foreground  "$SRC/batch4/env_moat_foreground.png"
$P ui_bait_icons        "$SRC/batch4/ui_bait_icons.png"
$P ui_upgrade_icons     "$SRC/batch4/ui_upgrade_icons.png"
$P ui_nav_icons         "$SRC/batch4/ui_nav_icons.png"
$P ui_panel_frame       "$SRC/batch4/ui_panel_frame.png"
$P ui_button            "$SRC/batch4/ui_button.png"
$P ui_action_button     "$SRC/batch4/ui_action_button.png"
$P ui_tension_frame     "$SRC/batch4/ui_tension_frame.png"
$P ui_logo_emblem       "$SRC/batch4/ui_logo_emblem.png"
# фазы луны: временный исходник строится из env_moon_full (D-028); ChatGPT-финал листа идёт через --incoming
python3 tools/art/moon_phases_src.py "$SRC/batch4/ui_moon_phases.png"
$P ui_moon_phases       "$SRC/batch4/ui_moon_phases.png"
$P ui_moon_phases_lg    "$SRC/batch4/ui_moon_phases.png"
for m in moat hud shop shop_workshop elsa title moon_calendar; do
  python3 tools/art/compose_mock.py $m docs/art_mocks/${m}_mock_latest.png --scale 2
done
