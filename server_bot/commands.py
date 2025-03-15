"""Command handlers for the Telegram bot."""
from functools import wraps
from telegram import Update, LinkPreviewOptions
from telegram.ext import CallbackContext
import yaml
from server_bot.utils import (
    get_total_cpu_usage,
    get_total_ram_usage,
    get_top_processes,
    get_user_resource_usage,
    kill_processes_by_name,
    kill_processes_by_user,
    get_sensors_data
)

# Load config
with open("config.yaml", "r", encoding="utf-8") as file:
    CONFIG = yaml.safe_load(file)

ALLOWED_USER = CONFIG["bot"]["allowed_user_ID"]
USERNAME = CONFIG["bot"]["user_username"]


def check_permission(update: Update):
    """Check if the user is allowed to use the bot."""
    user_id = update.message.from_user.id
    return user_id == ALLOWED_USER


def restricted(func):
    """Restrict access to a function based on user permissions."""
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        if not check_permission(update):
            await update.message.reply_text("Unauthorized!")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped


@restricted
async def start(update: Update, _: CallbackContext):
    """Send a welcome message."""
    await update.message.reply_text("Welcome! Use /status, /topcpu, /topram, or /killall.")


@restricted
async def help_command(update: Update, _: CallbackContext):
    """Send a help message with an overview of the bot's functionality."""
    help_text = (
        r"🤖 *Ali50 Monitoring Bot*"
        "\n\n"
        r"This bot allows you to monitor your server and manage processes\."
        "\n\n"
        r"Here are the available commands:"
        "\n"
        r"\- /start: Start the bot and see the welcome message\."
        "\n"
        r"\- /help: Show this help message\."
        "\n"
        r"\- /commands: List all available commands\."
        "\n"
        r"\- /status: Get detailed system status \(CPU, RAM, processes\)\."
        "\n"
        r"\- /topcpu: Show the top CPU\-consuming processes\."
        "\n"
        r"\- /topram: Show the top RAM\-consuming processes\."
        "\n"
        r"\- /killall \<process\_name\>: Kill all processes with the given name\."
        "\n"
        r"\- /killuser: Kill all processes for the configured user\."
        "\n\n"
        r"For more information, visit the "
        r"[GitHub repository](https://github\.com/fchinu/server\_status\_bot)\."
    )
    await update.message.reply_text(
        help_text, parse_mode="MarkdownV2",
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )


@restricted
async def commands(update: Update, _: CallbackContext):
    """List all available commands with brief descriptions."""
    commands_text = (
        r"📜 *Available Commands*"
        "\n\n"
        r"\- /start: Start the bot and see the welcome message\."
        "\n"
        r"\- /help: Show the help message\."
        "\n"
        r"\- /commands: List all available commands\."
        "\n"
        r"\- /status: Get detailed system status \(CPU, RAM, processes\)\."
        "\n"
        r"\- /topcpu: Show the top CPU\-consuming processes\."
        "\n"
        r"\- /topram: Show the top RAM\-consuming processes\."
        "\n"
        r"\- /killall \<process\_name\>: Kill all processes with the given name\."
        "\n"
        r"\- /killuser: Kill all processes for the configured user\."
        "\n\n"
    )
    await update.message.reply_text(commands_text, parse_mode="MarkdownV2")


@restricted
async def status(update: Update, _: CallbackContext):
    """Get detailed system status."""

    total_cpu = get_total_cpu_usage()
    ram_usage = get_total_ram_usage()
    user_usage = get_user_resource_usage()

    # Send a message with total system information
    status_message = (
        f"📊 *System Status (Updated):*\n"
        f"🔥 *Total CPU Usage:* {total_cpu:.2f}%\n"
        f"🧠 *Total RAM Usage:* {ram_usage:.2f}%\n\n"
        f"👥 *CPU/RAM Usage per User:*\n```\n{user_usage}\n```\n"
    )

    await update.message.reply_text(status_message, parse_mode="MarkdownV2")


@restricted
async def topcpu(update: Update, _: CallbackContext):
    """Get top CPU-consuming processes."""

    top_cpu = get_top_processes(by="cpu", limit=10)  # You can adjust the limit here

    top_cpu_message = (
        f"🚀 *Top CPU-consuming Processes:*\n"
        f"```\n{top_cpu}\n```"
    )

    await update.message.reply_text(top_cpu_message, parse_mode="MarkdownV2")


@restricted
async def topram(update: Update, _: CallbackContext):
    """Get top RAM-consuming processes."""

    top_memory = get_top_processes(by="memory", limit=10)  # You can adjust the limit here

    top_memory_message = (
        f"🧠 *Top RAM-consuming Processes:*\n"
        f"```\n{top_memory}\n```"
    )

    await update.message.reply_text(top_memory_message, parse_mode="MarkdownV2")


@restricted
async def killall(update: Update, context: CallbackContext):
    """Kill processes by name for the configured user."""
    if not context.args:
        await update.message.reply_text("Usage: /killall <process_name>")
        return

    process_name = context.args[0]
    result = kill_processes_by_name(process_name, USERNAME)
    await update.message.reply_text(result)


@restricted
async def killuser(update: Update, _: CallbackContext):
    """Kill all processes for the configured user."""
    result = kill_processes_by_user(USERNAME)
    await update.message.reply_text(result)

@restricted
async def sensors(update: Update, context: CallbackContext):
    """Send sensor data (e.g., temperatures, fan speeds)."""
    sensors_data = get_sensors_data()
    await update.message.reply_text(f"📊 *Sensor Data:*\n```\n{sensors_data}\n```", parse_mode="Markdown")
