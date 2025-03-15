# Server Monitoring Bot

A Telegram bot for monitoring server resources and managing processes.

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![CI Tests](https://github.com/fchinu/server_status_bot/actions/workflows/config_test.yml/badge.svg)

---

## **Features**

- **System Monitoring**:
  - Check CPU and RAM usage.
  - View top CPU and RAM-consuming processes.
  - Monitor hardware sensors (e.g., temperatures, fan speeds).

- **Process Management**:
  - Kill processes by name or user.

---

## **Commands**

| Command           | Description                                      |
|-------------------|--------------------------------------------------|
| `/start`          | Start the bot and see the welcome message.       |
| `/help`           | Show the help message.                           |
| `/commands`       | List all available commands.                     |
| `/status`         | Get detailed system status (CPU, RAM, processes).|
| `/topcpu`         | Show the top CPU-consuming processes.            |
| `/topram`         | Show the top RAM-consuming processes.            |
| `/killall <name>` | Kill all processes with the given name.          |
| `/killuser`       | Kill all processes for the configured user.      |
| `/sensors`        | Show hardware sensor data (e.g., temperatures).  |

---

## **Setup**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/fchinu/server_status_bot.git
   cd server_status_bot

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt

3. **Configure the Bot**:

    Modify the config.yaml file:

    ```yaml
    bot:
        token: "YOUR_BOT_TOKEN"
        allowed_user_ID: YOUR_USER_ID
        user_username: YOUR_USERNAME

4. Run the Bot:

    ```bash
    bash scripts/run.sh