from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# API ключи
BOT_TOKEN = "7598387508:AAHbYeJv-r1eQe2YcB9wEiXypGVgw3qd-Js"

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я футбольный бот. Вот что я умею:\n"
        "/schedule - ближайшие матчи\n"
        "/search_player <имя игрока> - поиск статистики игрока\n"
        "/transfers - последние трансферы\n"
        "/league_table <код лиги> - турнирная таблица\n"
        "/team_matches <название команды> - матчи команды\n"
        "/news - последние новости футбола"
    )

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

# Основная функция
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("schedule", schedule))
    application.add_handler(CommandHandler("search_player", search_player))
    application.add_handler(CommandHandler("transfers", transfers))
    application.add_handler(CommandHandler("league_table", league_table))
    application.add_handler(CommandHandler("team_matches", team_matches))
    application.add_handler(CommandHandler("news", news))

    application.run_polling()

if __name__ == "__main__":
    main()
