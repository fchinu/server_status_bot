""" Main bot application to run the bot. """
from telegram.ext import Application, CommandHandler
import yaml
from server_bot.commands import start, status, killall, killuser, topcpu, topram

# Load config
with open("config.yaml", "r", encoding="utf-8") as file:
    CONFIG = yaml.safe_load(file)

BOT_TOKEN = CONFIG["bot"]["token"]


def main():
    """
    Main function to initialize and run the bot application.

    This function performs the following tasks:
    1. Builds the application with the provided bot token.
    2. Registers command handlers for various bot commands:
       - /start: Starts the bot.
       - /status: Checks the status.
       - /topcpu: Displays the top CPU-consuming processes.
       - /topram: Displays the top RAM-consuming processes.
       - /killall: Kills all specified processes.
       - /killuser: Kills all processes for a given user.
    3. Runs the bot in polling mode to listen for incoming updates and commands.
    """

    app = Application.builder().token(BOT_TOKEN).build()

    # Register commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("topcpu", topcpu))
    app.add_handler(CommandHandler("topram", topram))
    app.add_handler(CommandHandler("killall", killall))
    app.add_handler(CommandHandler("killuser", killuser))

    app.run_polling()


if __name__ == "__main__":
    main()
