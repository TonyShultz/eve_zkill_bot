# 📄 main.py
import asyncio
from redisq_listener import fetch_killmails

async def main():
    await fetch_killmails()

if __name__ == "__main__":
    asyncio.run(main())
