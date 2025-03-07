# 📄 esi_fetcher.py
import aiohttp
import json
import os
from config import EVE_NAMES_FILE

# Загружаем кэш из файла
if os.path.exists(EVE_NAMES_FILE):
    with open(EVE_NAMES_FILE, "r", encoding="utf-8") as f:
        try:
            cache = json.load(f)
        except json.JSONDecodeError:
            cache = {}
else:
    cache = {}

async def save_cache():
    """Сохраняет кэш имен в файл."""
    with open(EVE_NAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)

async def fetch_esi_data(entity_type, entity_id):
    """Запрашивает данные из ESI API и кэширует их."""
    if not entity_id:
        return "Unknown"

    if str(entity_id) in cache:
        return cache[str(entity_id)]

    esi_urls = {
        "characters": f"https://esi.evetech.net/latest/characters/{entity_id}/",
        "corporations": f"https://esi.evetech.net/latest/corporations/{entity_id}/",
        "alliances": f"https://esi.evetech.net/latest/alliances/{entity_id}/",
        "types": f"https://esi.evetech.net/latest/universe/types/{entity_id}/",
        "systems": f"https://esi.evetech.net/latest/universe/systems/{entity_id}/"
    }

    url = esi_urls.get(entity_type)
    if not url:
        return "Unknown"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    name = data.get("name", "Unknown")
                    cache[str(entity_id)] = name
                    await save_cache()
                    return name
    except Exception as e:
        print(f"⚠️ Ошибка запроса к ESI ({entity_type}, {entity_id}): {e}")

    return "Unknown"
