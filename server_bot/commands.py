"""Command handlers for the Telegram bot."""
from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext
import yaml
from server_bot.utils import (
    get_total_cpu_usage,
    get_total_ram_usage,
    get_top_processes,
    get_user_resource_usage,
    run_command
)

# Load config
with open("config.yaml", "r", encoding="utf-8") as file:
    CONFIG = yaml.safe_load(file)

ALLOWED_USERS = CONFIG["bot"]["allowed_users"]


def check_permission(update: Update):
    """Check if the user is allowed to use the bot."""
    user_id = update.message.from_user.id
    return user_id in ALLOWED_USERS


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
async def status(update: Update, _: CallbackContext):
    """Get detailed system status."""

    total_cpu = get_total_cpu_usage()
    ram_usage = get_total_ram_usage()
    user_usage = get_user_resource_usage()

    # Send a message with total system information
    status_message = (
        f"📊 *System Status (Updated):*\n"
        f"🔥 *Total CPU Usage:* {total_cpu:.2f}%\n\n"
        f"🧠 *RAM Usage:* {ram_usage:.2f}%\n\n"
        f"👥 *CPU/RAM Usage per User:*\n```\n{user_usage}\n```\n"
    )

    await update.message.reply_text(status_message, parse_mode="Markdown")


@restricted
async def topcpu(update: Update, _: CallbackContext):
    """Get top CPU-consuming processes."""

    top_cpu = get_top_processes(by="cpu", limit=10)  # You can adjust the limit here

    top_cpu_message = (
        f"🚀 *Top CPU-consuming Processes:*\n"
        f"```\n{top_cpu}\n```"
    )

    await update.message.reply_text(top_cpu_message, parse_mode="Markdown")


@restricted
async def topram(update: Update, _: CallbackContext):
    """Get top RAM-consuming processes."""

    top_memory = get_top_processes(by="memory", limit=10)  # You can adjust the limit here

    top_memory_message = (
        f"🧠 *Top RAM-consuming Processes:*\n"
        f"```\n{top_memory}\n```"
    )

    await update.message.reply_text(top_memory_message, parse_mode="Markdown")


@restricted
async def killall(update: Update, _: CallbackContext):
    """Kill a process (defined in config)."""
    process = CONFIG["commands"]["killall"]
    output = run_command(f"killall -9 {process}")
    await update.message.reply_text(f"Killed {process}:\n{output}")
