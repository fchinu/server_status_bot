#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 {pytest|pylint|flake8}"
    exit 1
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