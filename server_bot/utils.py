"""Provide utility functions for monitoring system resources and running shell commands."""

from collections import defaultdict
import os
import subprocess
import time
import psutil


def escape_markdown_v2(text: str) -> str:
    """Escape special characters for MarkdownV2 formatting.

    Parameters:
        text (str): The input text to escape.

    Returns:
        str: The escaped text.
    """
    # List of characters to escape
    escape_chars = r"_*[]()~`>#+-=|{}.!"

    # Escape each character
    for char in escape_chars:
        text = text.replace(char, f"\\{char}")

    return text


def run_command(cmd):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(cmd, shell=False, capture_output=True, text=True, check=False)
        return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
    except Exception as e:  # pylint: disable=broad-except
        return str(e)


def get_total_cpu_usage():
    """Returns total CPU usage as a percentage."""
    return psutil.cpu_percent(interval=0.1)  # Reduced interval for faster response


def get_total_ram_usage():
    """
    Returns RAM usage information.
    """
    ram = psutil.virtual_memory()
    return ram.percent


def get_ram_usage():
    """
    Returns RAM usage information.
    """
    ram = psutil.virtual_memory()
    return (
        f"Total: {ram.total / (1024 ** 3):.2f} GB\n"
        f"Used: {ram.used / (1024 ** 3):.2f} GB\n"
        f"Available: {ram.available / (1024 ** 3):.2f} GB\n"
        f"Usage: {ram.percent}%"
    )


def get_top_processes(by="cpu", limit=5):
    """
    Returns the top `limit` processes sorted by CPU or RAM usage, grouped by user and process name.
    :param by: "cpu" or "memory"
    """
    # Prime CPU usage tracking
    for proc in psutil.process_iter(attrs=["cpu_percent"]):
        try:
            proc.cpu_percent()  # Initialize CPU tracking
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    time.sleep(0.5)  # Allow time for CPU usage measurement

    # Collect and group process information by (username, process name)
    process_stats = defaultdict(lambda: {"cpu": 0.0, "memory": 0.0, "count": 0})
    for proc in psutil.process_iter(
        attrs=["username", "pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            user = proc.info["username"]
            name = proc.info["name"]
            key = (user, name)  # Group by (user, process)

            process_stats[key]["cpu"] += proc.info["cpu_percent"]
            process_stats[key]["memory"] += proc.info["memory_percent"]
            process_stats[key]["count"] += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Normalize CPU per number of cores
    num_cores = psutil.cpu_count(logical=True)
    for data in process_stats.values():
        data["cpu"] /= num_cores

    key = "cpu" if by == "cpu" else "memory"

    # Sort by CPU or memory usage
    top_processes = sorted(process_stats.items(), key=lambda x: x[1][key], reverse=True)[:limit]

    return "\n".join([
        f"{user} - {name} ({data['count']} instances): {data[key]:.2f}%"
        for (user, name), data in top_processes
    ])


def get_user_resource_usage():
    """
    Returns CPU and RAM usage per user, normalized properly.
    """
    user_stats = defaultdict(lambda: {"cpu": 0.0, "memory": 0.0})
    num_cores = psutil.cpu_count(logical=True)  # Get the number of logical CPU cores

    # Step 1: Prime CPU tracking (Initial call always returns 0%)
    processes = []
    for proc in psutil.process_iter(attrs=["username", "cpu_percent", "memory_percent"]):
        try:
            proc.cpu_percent()  # Initialize CPU usage tracking
            processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    time.sleep(0.5)  # Allow time for CPU usage measurement

    # Step 2: Collect per-user CPU and RAM usage
    for proc in processes:
        try:
            user = proc.info["username"]
            cpu_usage = proc.cpu_percent()  # Second call gets real values
            user_stats[user]["cpu"] += cpu_usage / num_cores  # Normalize per core
            user_stats[user]["memory"] += proc.info["memory_percent"]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Step 3: Format and return results
    return "\n".join(
        [
            f"{user}: CPU {data['cpu']:.2f}%, RAM {data['memory']:.2f}%"
            for user, data in user_stats.items()
        ]
    ) or r"No active processes found\."


def kill_processes_by_name(process_name, username):
    """Kill all processes with the given name, excluding the bot's PID."""
    try:
        # Get the bot's PID
        bot_pid = os.getpid()

        # Find all PIDs for the given process name and user
        result = subprocess.run(
            ["pgrep", "-u", username, process_name],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            return f"No processes found with name '{process_name}'."

        # Extract PIDs from the pgrep output
        pids = result.stdout.strip().split()
        pids = [pid for pid in pids if pid != str(bot_pid)]  # Exclude the bot's PID

        if not pids:
            return f"No processes found with name '{process_name}'."

        # Kill the remaining PIDs
        for pid in pids:
            subprocess.run(["kill", "-9", pid], capture_output=True, text=True, check=False)

        return f"Killed {len(pids)} processes with name '{process_name}'."
    except Exception as e:  # pylint: disable=broad-except
        return f"Error: {e}"


def kill_processes_by_user(username):
    """Kill all processes owned by the given user."""
    try:
        # Get the bot's PID
        bot_pid = os.getpid()

        # Find all PIDs for the given user
        result = subprocess.run(
            ["pgrep", "-u", username],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            return f"No processes found for user '{username}'."

        # Extract PIDs from the pgrep output
        pids = result.stdout.strip().split()
        pids = [pid for pid in pids if pid != str(bot_pid)]  # Exclude the bot's PID

        if not pids:
            return f"No processes found for user '{username}'."

        # Kill the remaining PIDs
        for pid in pids:
            subprocess.run(["kill", "-9", pid], capture_output=True, text=True, check=False)

        return f"Killed {len(pids)} processes for user '{username}'."
    except Exception as e:  # pylint: disable=broad-except
        return f"Error: {e}"


def get_sensors_data():
    """Run the 'sensors' command and return its output."""
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return result.stdout.strip()
        return "Error: Unable to retrieve sensor data. Ensure 'lm-sensors' is installed."
    except Exception as e:  # pylint: disable=broad-except
        return f"Error: {e}"
