# 📄 config.py

# Настройки Telegram
TELEGRAM_TOKEN = 'telegram_bot_token'
CHAT_ID = 'telegram_chat_id'
THEME_ID = 'theme_id'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# URL RedisQ
REDISQ_URL = 'https://redisq.zkillboard.com/listen.php?queueID=YOUR_UNIQUE_ID'

# ID целевой корпорации
TARGET_CORPORATION_ID = corporation_id  # Замените на нужный ID

# Файл для кэша имен
EVE_NAMES_FILE = "eve_cache.json"
