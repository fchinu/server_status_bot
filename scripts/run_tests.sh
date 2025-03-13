#!/bin/bash

run_all() {
    echo "Running all tests..."
    echo "Running unit tests with pytest..."
    pytest tests/
    echo "Running pylint for code quality..."
    pylint server_bot/
    echo "Running flake8 for code quality..."
    flake8 server_bot/
}

if [ $# -eq 0 ]; then
    run_all
    exit 0
fi

case "$1" in
    pytest)
        echo "Running unit tests with pytest..."
        pytest tests/
        ;;
    pylint)
        echo "Running pylint for code quality..."
        pylint server_bot/
        ;;
    flake8)
        echo "Running flake8 for code quality..."
        flake8 server_bot/
        ;;
    *)
        echo "Invalid argument. Usage: $0 {pytest|pylint|flake8}"
        exit 1
        ;;
esac