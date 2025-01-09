
# Полный код бота с расширенным функционалом и API для новостей
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# API ключи
FOOTBALL_DATA_API_KEY = "acbdf84eb08b4701bef17f5c292bf970"
NEWS_API_KEY = "149635df82b042dc8954fa430cdf3401"
BOT_TOKEN = "7598387508:AAHbYeJv-r1eQe2YcB9wEiXypGVgw3qd-Js"

# Функция для получения данных о ближайших матчах
def get_upcoming_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        matches = data.get("matches", [])
        result = []

        for match in matches[:5]:  # Ограничиваем до 5 матчей
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            match_date = match['utcDate']

            result.append(f"{home_team} vs {away_team} | {match_date}")

        return "\n".join(result)
    else:
        return "Ошибка при получении данных о матчах."

# Функция для поиска игрока
def get_player_stats(player_name):
    url = f"https://api.football-data.org/v4/players/{player_name}"
    headers = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        player_data = response.json()
        name = player_data.get('name', 'Неизвестно')
        position = player_data.get('position', 'Неизвестно')
        team = player_data.get('team', {}).get('name', 'Неизвестно')
        stats = player_data.get('stats', {})

        return (
            f"Игрок: {name}\n"
            f"Позиция: {position}\n"
            f"Клуб: {team}\n"
            f"Статистика: {stats}"
        )
    else:
        return "Ошибка при получении данных об игроке."

# Функция для получения данных о трансферах
def get_transfers():
    url = "https://api.football-data.org/v4/transfers"
    headers = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        transfers = data.get("transfers", [])
        result = []

        for transfer in transfers[:5]:  # Ограничиваем до 5 трансферов
            player = transfer['player']['name']
            from_team = transfer['fromTeam']['name']
            to_team = transfer['toTeam']['name']
            date = transfer['date']

            result.append(f"Игрок: {player} | Из: {from_team} | В: {to_team} | Дата: {date}")

        return "\n".join(result)
    else:
        return "Ошибка при получении данных о трансферах."

# Функция для получения турнирной таблицы
def get_league_table(league_code):
    url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
    headers = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        standings = data.get("standings", [])[0].get("table", [])
        result = []

        for team in standings:
            position = team['position']
            name = team['team']['name']
            points = team['points']

            result.append(f"{position}. {name} - {points} очков")

        return "\n".join(result)
    else:
        return "Ошибка при получении турнирной таблицы."

# Функция для поиска матчей команды
def search_team_matches(team_name):
    url = f"https://api.football-data.org/v4/teams"
    headers = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        teams = data.get('teams', [])
        for team in teams:
            if team_name.lower() in team['name'].lower():
                team_id = team['id']
                matches_url = f"https://api.football-data.org/v4/teams/{team_id}/matches"
                matches_response = requests.get(matches_url, headers=headers)
                if matches_response.status_code == 200:
                    matches_data = matches_response.json()
                    matches = matches_data.get("matches", [])
                    result = []
                    for match in matches[:5]:
                        home_team = match['homeTeam']['name']
                        away_team = match['awayTeam']['name']
                        match_date = match['utcDate']
                        result.append(f"{home_team} vs {away_team} | {match_date}")
                    return "\n".join(result)
    return "Команда не найдена или данные недоступны."

# Функция для получения новостей
def get_match_news():
    url = f"https://newsapi.org/v2/everything?q=football&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        result = []

        for article in articles[:5]:  # Ограничиваем до 5 новостей
            title = article['title']
            description = article['description']
            url = article['url']
            result.append(f"{title}\n{description}\nСсылка: {url}")

        return "\n\n".join(result)
    else:
        return "Ошибка при получении новостей."

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Я футбольный бот. Вот что я умею:\n"
        "/расписание - ближайшие матчи\n"
        "/поиск <имя игрока> - поиск статистики игрока\n"
        "/трансферы - последние трансферы\n"
        "/таблица <код лиги> - турнирная таблица\n"
        "/команда <название команды> - матчи команды\n"
        "/новости - последние новости футбола"
    )

# Команда /расписание
def schedule(update: Update, context: CallbackContext):
    matches = get_upcoming_matches()
    update.message.reply_text(matches)

# Команда /поиск
def search_player(update: Update, context: CallbackContext):
    if context.args:
        player_name = " ".join(context.args)
        stats = get_player_stats(player_name)
        update.message.reply_text(stats)
    else:
        update.message.reply_text("Пожалуйста, укажите имя игрока.")

# Команда /трансферы
def transfers(update: Update, context: CallbackContext):
    transfer_list = get_transfers()
    update.message.reply_text(transfer_list)

# Команда /таблица
def league_table(update: Update, context: CallbackContext):
    if context.args:
        league_code = context.args[0]
        table = get_league_table(league_code)
        update.message.reply_text(table)
    else:
        update.message.reply_text("Пожалуйста, укажите код лиги (например, PL для АПЛ).")

# Команда /команда
def team_matches(update: Update, context: CallbackContext):
    if context.args:
        team_name = " ".join(context.args)
        matches = search_team_matches(team_name)
        update.message.reply_text(matches)
    else:
        update.message.reply_text("Пожалуйста, укажите название команды.")

# Команда /новости
def news(update: Update, context: CallbackContext):
    news_list = get_match_news()
    update.message.reply_text(news_list)

# Основная функция
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("расписание", schedule))
    dp.add_handler(CommandHandler("поиск", search_player))
    dp.add_handler(CommandHandler("трансферы", transfers))
    dp.add_handler(CommandHandler("таблица", league_table))
    dp.add_handler(CommandHandler("команда", team_matches))
    dp.add_handler(CommandHandler("новости", news))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
