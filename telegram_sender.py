# 📄 telegram_sender.py
import aiohttp
from config import TELEGRAM_API_URL, CHAT_ID, THEME_ID
from esi_fetcher import fetch_esi_data

async def send_to_telegram(killmail):
    """Отправляет информацию о килле в Telegram."""
    kill_id = killmail['killmail_id']
    system_id = killmail['solar_system_id']
    victim = killmail['victim']
    ship_id = victim.get('ship_type_id', 'Unknown')
    victim_id = victim.get('character_id')
    victim_corp_id = victim.get('corporation_id')

    # Получаем названия из ESI
    system_name = await fetch_esi_data("systems", system_id)
    ship_name = await fetch_esi_data("types", ship_id)
    victim_name = await fetch_esi_data("characters", victim_id)
    victim_corp_name = await fetch_esi_data("corporations", victim_corp_id)

    message = (f"⚔️ Новый килл!\n"
               f"Система: {system_name}\n"
               f"Жертва: {victim_name} ({victim_corp_name})\n"
               f"Корабль: {ship_name}\n"
               f"Подробнее: https://zkillboard.com/kill/{kill_id}/")

    async with aiohttp.ClientSession() as session:
        payload = {"chat_id": CHAT_ID, "text": message, "reply_to_message_id": THEME_ID}
        async with session.post(TELEGRAM_API_URL, json=payload) as response:
            if response.status == 200:
                print(f"✅ Успешно отправлено: {kill_id}")
            else:
                print(f"❌ Ошибка отправки: {await response.text()}")
