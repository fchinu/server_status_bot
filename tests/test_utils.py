import pytest
import sys
from server_bot.utils import get_total_cpu_usage, get_total_ram_usage, get_ram_usage, get_top_processes, get_user_resource_usage

def test_get_total_cpu_usage():
    """Test that get_total_cpu_usage returns a valid CPU percentage."""
    cpu_usage = get_total_cpu_usage()
    assert isinstance(cpu_usage, float)
    assert 0 <= cpu_usage <= 100

def test_get_total_ram_usage():
    """Test that get_total_ram_usage returns a valid RAM percentage."""
    ram_usage = get_total_ram_usage()
    assert isinstance(ram_usage, float)
    assert 0 <= ram_usage <= 100

def test_get_ram_usage():
    """Test that get_ram_usage returns a valid RAM usage string."""
    ram_usage = get_ram_usage()
    assert isinstance(ram_usage, str)
    assert "Total:" in ram_usage
    assert "Used:" in ram_usage
    assert "Available:" in ram_usage
    assert "Usage:" in ram_usage

def test_get_top_processes():
    """Test that get_top_processes returns a valid string."""
    top_cpu = get_top_processes(by="cpu", limit=5)
    assert isinstance(top_cpu, str)
    assert "instances" in top_cpu or "No active processes found." in top_cpu

    top_memory = get_top_processes(by="memory", limit=5)
    assert isinstance(top_memory, str)
    assert "instances" in top_memory or "No active processes found." in top_memory

def test_get_user_resource_usage():
    """Test that get_user_resource_usage returns a valid string."""
    user_usage = get_user_resource_usage()
    assert isinstance(user_usage, str)
    assert "CPU" in user_usage or "No active processes found." in user_usage