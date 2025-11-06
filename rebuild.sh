#!/bin/bash
# Rebuild script for NIS2 ISMS Stack
# This only affects the NIS2 ISMS containers, not other Docker services

set -e

echo "=========================================="
echo "NIS2 ISMS Stack Rebuild"
echo "=========================================="
echo ""

echo "Step 1: Stopping NIS2 ISMS containers..."
docker-compose down

echo ""
echo "Step 2: Building images (without cache)..."
docker-compose build --no-cache

echo ""
echo "Step 3: Starting services..."
docker-compose up -d

echo ""
echo "Step 4: Waiting for services to start..."
sleep 5

echo ""
echo "Step 5: Checking container status..."
docker-compose ps

echo ""
echo "=========================================="
echo "Rebuild complete!"
echo "=========================================="
echo ""
echo "To view logs, run:"
echo "  docker-compose logs -f"
echo ""
echo "To view backend logs only:"
echo "  docker logs -f nis2-isms-backend"
echo ""
echo "To view frontend logs only:"
echo "  docker logs -f nis2-isms-frontend"
echo ""
