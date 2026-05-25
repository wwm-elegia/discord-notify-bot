import os
from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1490326165192183859

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

MOSCOW_TZ = ZoneInfo("Europe/Moscow")

WEEKDAY_MESSAGE = """
Открыта запись на ГВГ на субботу и воскресенье.

🕘 Начало ГВГ — 21:30 (по МСК)
⚔️ Формат: два боя по 30 минут.

Просьба всем желающим записаться на удобный для вас день — или на оба дня, если есть возможность.

Очень просим каждого принять участие: каждый из вас ценен для гильдии, и присутствие каждого игрока действительно влияет на общий результат. Чем больше нас будет, тем сильнее и увереннее мы сможем выступить. 🖤

📌 Ссылка для записи находится в закрепе:
• в Telegram
• в Discord
"""

SATURDAY_MESSAGE = """
Напоминаем, что сегодня — суббота, и у нас ГВГ. ⚔️

🕘 Начало — 21:30 (по МСК)
Формат: два боя по 30 минут.

Если вы ещё не записались, пожалуйста, отметьтесь как можно скорее. Каждый игрок действительно важен для общего результата, и ваше присутствие очень помогает гильдии. 🖤

📌 Ссылка для записи находится в закрепе:
• в Telegram
• в Discord
"""

SUNDAY_MESSAGE = """
Напоминаем, что сегодня — воскресенье, и у нас ГВГ. ⚔️

🕘 Начало — 21:30 (по МСК)
Формат: два боя по 30 минут.

Если вы ещё не записались, пожалуйста, отметьтесь как можно скорее. Каждый игрок действительно важен для общего результата, и ваше присутствие очень помогает гильдии. 🖤

📌 Ссылка для записи находится в закрепе:
• в Telegram
• в Discord
"""

TIMES = [
    (9, 0),
    (15, 0),
    (19, 0)
]

last_sent = None

@tasks.loop(minutes=1)
async def scheduler():
    global last_sent

    now = datetime.now(MOSCOW_TZ)
    current_time = (now.hour, now.minute)

    if current_time not in TIMES:
        return

    unique_key = f"{now.date()}-{now.hour}-{now.minute}"

    if last_sent == unique_key:
        return

    channel = bot.get_channel(CHANNEL_ID)

    if not channel:
        print("Канал не найден.")
        return

    weekday = now.weekday()

    if weekday <= 4:
        message = WEEKDAY_MESSAGE
    elif weekday == 5:
        message = SATURDAY_MESSAGE
    else:
        message = SUNDAY_MESSAGE

    embed = discord.Embed(
        description=message,
        color=0x000000
    )

    embed.set_footer(text="Elegia")

    await channel.send(embed=embed)

    print(f"Сообщение отправлено: {now}")

    last_sent = unique_key

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")

    if not scheduler.is_running():
        scheduler.start()

bot.run(TOKEN)
