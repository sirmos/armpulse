#!/bin/bash
# Start the ArmBench MCP Server
set -e

source .venv/bin/activate 2>/dev/null || true

PORT=${PORT:-8000}
echo "⚡ Starting ArmBench MCP Server on port $PORT..."
echo "   Docs: http://localhost:$PORT/docs"
echo "   MCP tools: http://localhost:$PORT/mcp/tools"
echo ""

python3 -m uvicorn mcp_server.main:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 2
