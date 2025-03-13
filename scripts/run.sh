#!/bin/bash

# Change to the project root directory
cd "$(dirname "$0")/.."

# Run the bot
python3 -m server_bot.bot
