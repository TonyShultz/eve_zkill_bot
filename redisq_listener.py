# 📄 redisq_listener.py
import aiohttp
import asyncio
from config import REDISQ_URL, TARGET_CORPORATION_ID
from telegram_sender import send_to_telegram

async def fetch_killmails():
    """Получает киллмейлы из RedisQ и отправляет в Telegram при соответствии фильтру."""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(REDISQ_URL, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('package'):
                            killmail = data['package']['killmail']
                            victim_corp_id = killmail['victim'].get('corporation_id')

                            if victim_corp_id == TARGET_CORPORATION_ID:
                                await send_to_telegram(killmail)
                            else:
                                print(f"⚠️ Килл {killmail['killmail_id']} не соответствует фильтру.")
                        else:
                            print("🔄 Нет новых киллов.")
                            await asyncio.sleep(1)  # Ждем дольше, если нет новых киллов
                    else:
                        print(f"❌ Ошибка RedisQ: {response.status}")
                        await asyncio.sleep(10)
            except asyncio.TimeoutError:
                print("⏳ Таймаут запроса к RedisQ. Повтор через 10 сек...")
                await asyncio.sleep(10)
            except Exception as e:
                print(f"❌ Ошибка запроса: {e}")
                await asyncio.sleep(10)
