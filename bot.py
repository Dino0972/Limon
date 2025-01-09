from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

# Конфигурация
BOT_TOKEN = "7598387508:AAHbYeJv-r1eQe2YcB9wEiXypGVgw3qd-Js"
WEBHOOK_URL = "https://ВАШ-СЕРВЕР/render.com/webhook"  # Замените на ваш HTTPS URL

# Создаём приложение Flask
app = Flask(__name__)

# Создаём экземпляр бота
application = Application.builder().token(BOT_TOKEN).build()

# Команды
async def start(update: Update, context):
    await update.message.reply_text(
        "Привет! Я футбольный бот. Вот что я умею:\n"
        "/schedule - ближайшие матчи\n"
        "/search_player <имя игрока> - поиск статистики игрока\n"
        "/transfers - последние трансферы\n"
        "/league_table <код лиги> - турнирная таблица\n"
        "/team_matches <название команды> - матчи команды\n"
        "/news - последние новости футбола"
    )

async def schedule(update: Update, context):
    await update.message.reply_text("Здесь будет расписание ближайших матчей.")

async def search_player(update: Update, context):
    await update.message.reply_text("Здесь будет информация об игроке.")

async def transfers(update: Update, context):
    await update.message.reply_text("Здесь будет список последних трансферов.")

async def league_table(update: Update, context):
    await update.message.reply_text("Здесь будет турнирная таблица.")

async def team_matches(update: Update, context):
    await update.message.reply_text("Здесь будет информация о матчах команды.")

async def news(update: Update, context):
    await update.message.reply_text("Здесь будут последние новости футбола.")

# Регистрируем команды
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("schedule", schedule))
application.add_handler(CommandHandler("search_player", search_player))
application.add_handler(CommandHandler("transfers", transfers))
application.add_handler(CommandHandler("league_table", league_table))
application.add_handler(CommandHandler("team_matches", team_matches))
application.add_handler(CommandHandler("news", news))

# Маршрут для Telegram вебхука
@app.route(f"/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return "OK", 200

# Основной запуск
if __name__ == "__main__":
    # Устанавливаем вебхук
    application.bot.set_webhook(WEBHOOK_URL)
    # Запускаем Flask
    app.run(host="0.0.0.0", port=5000)
