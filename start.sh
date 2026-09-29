#!/bin/bash

echo "=== MAX_game_bot Bot Deploy ==="

echo "Updating repository..."
git pull

echo "Building containers..."
docker compose build

echo "Starting bot..."
docker compose up -d

echo "Checking containers..."
docker ps

echo "=== Bot started ==="