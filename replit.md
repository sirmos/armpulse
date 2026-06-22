# ArmBench

ArmBench is an Arm64-optimized LLM inference benchmark suite and MCP (Model Context Protocol) compatible server. It is designed to leverage KleidiAI and llama.cpp optimizations on Arm64 cloud infrastructure.

## Project Overview

- **Backend**: FastAPI server (`mcp_server/`) serving the API and dashboard on port 5000
- **Frontend**: Static HTML dashboard (`dashboard/index.html`) served via FastAPI
- **Benchmark logic**: `benchmark/` package (runner, metrics, model configs)
- **Inference**: Uses `llama.cpp` when available; falls back to simulation mode for dev/testing

## Running the App

The app runs on port 5000 via uvicorn in development. The workflow command is:
```
python -m uvicorn mcp_server.main:app --host 0.0.0.0 --port 5000 --reload
```

## API Endpoints

- `GET /` — Dashboard (HTML)
- `GET /health` — Server health and platform info
- `GET /models` — List configured models
- `POST /generate` — Run LLM inference
- `POST /benchmark` — Run full benchmark suite
- `GET /mcp/tools` — MCP-compatible tools listing
- `GET /docs` — Interactive API docs (Swagger)

## Key Files

- `mcp_server/main.py` — FastAPI app entry point
- `mcp_server/routes.py` — API route handlers
- `benchmark/runner.py` — Inference and benchmark execution logic
- `benchmark/metrics.py` — BenchmarkResult dataclass and platform info
- `benchmark/models.py` — Model configurations (Llama 3.2 3B Q4/Q8)
- `dashboard/index.html` — Frontend dashboard

## Notes

- When `llama.cpp` is not built, the server uses simulated inference for development/testing
- Models are downloaded from HuggingFace Hub on demand into the `models/` directory
- Built for the Arm AI Optimization Challenge 2026

## User Preferences

(No preferences set yet)
