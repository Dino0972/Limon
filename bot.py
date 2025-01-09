from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import logging

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# API ключи
FOOTBALL_DATA_API_KEY = "acbdf84eb08b4701bef17f5c292bf970"
NEWS_API_KEY = "149635df82b042dc8954fa430cdf3401"
BOT_TOKEN = "7598387508:AAHbYeJv-r1eQe2YcB9wEiXypGVgw3qd-Js"

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я футбольный бот. Вот что я умею:\n"
        "/расписание - ближайшие матчи\n"
        "/поиск <имя игрока> - поиск статистики игрока\n"
        "/трансферы - последние трансферы\n"
        "/таблица <код лиги> - турнирная таблица\n"
        "/команда <название команды> - матчи команды\n"
        "/новости - последние новости футбола"
    )

# Основная функция
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Здесь будет расписание ближайших матчей.")

async def search_player(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Здесь будет информация об игроке.")

async def transfers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Здесь будет список последних трансферов.")

async def league_table(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Здесь будет турнирная таблица.")

async def team_matches(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Здесь будет информация о матчах команды.")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Здесь будут последние новости футбола.")

# Основной код
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("расписание", schedule))
    application.add_handler(CommandHandler("поиск", search_player))
    application.add_handler(CommandHandler("трансферы", transfers))
    application.add_handler(CommandHandler("таблица", league_table))
    application.add_handler(CommandHandler("команда", team_matches))
    application.add_handler(CommandHandler("новости", news))

    application.run_polling()

if name == "__main__":
    main()
