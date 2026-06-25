---
title: Arm Pulse
emoji: ⚡
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---
# ⚡ Arm Pulse — Arm64 LLM Inference Benchmark Suite + MCP Server

> KleidiAI-optimized LLM benchmarking and inference server for Arm64 cloud infrastructure.
> Built for the **Arm AI Optimization Challenge 2026**.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Arm64-orange.svg)](https://www.arm.com)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)

---

## 🎯 What is Arm Pulse?

Arm Pulse is a one-command benchmarking tool that:

1. **Deploys LLMs** (Llama 3.2) on Arm64 cloud instances using llama.cpp + KleidiAI
2. **Measures real performance** — tokens/sec, time-to-first-token, memory usage across quantization levels (Q4_K_M vs Q8_0)
3. **Serves results** via an MCP-compatible FastAPI server any agent framework can call
4. **Visualizes everything** in a clean real-time dashboard

---

## 🏗️ Architecture
arm-pulse/

├── benchmark/        # llama.cpp + KleidiAI inference engine + metrics

├── mcp_server/       # FastAPI MCP-compatible LLM endpoint

├── dashboard/        # Real-time results dashboard (HTML)

├── scripts/          # One-command setup + benchmark + server scripts

└── docker/           # Arm64-optimized Docker configuration
---

## 🚀 Quick Start (Arm64 Instance)

### 1. Clone and setup
```bash
git clone https://github.com/sirmos/arm-pulse.git
cd arm-pulse
bash scripts/setup.sh
```

### 2. Run benchmark
```bash
bash scripts/run_benchmark.sh
```

### 3. Start MCP server
```bash
bash scripts/start_mcp.sh
```

### 4. Open dashboard
Navigate to `http://your-instance-ip:8000` in your browser.

---

## ☁️ Tested Arm64 Platforms

| Platform | Instance | Arm CPU |
|---|---|---|
| Oracle Cloud | VM.Standard.A1.Flex | Ampere Altra |
| AWS | c7g.large | Graviton3 |
| GCP | c4a-standard-4 | Axion |

---

## 📊 What We Benchmark

| Metric | Description |
|---|---|
| Tokens/sec | Inference throughput |
| Time to First Token | Latency from prompt to first output token |
| Memory (MB) | RAM consumed during inference |
| Model size (GB) | Disk footprint per quantization level |

### Models
| Model | Quant | Size | Use case |
|---|---|---|---|
| Llama-3.2-3B-Instruct | Q4_K_M | 1.9 GB | Speed-optimized |
| Llama-3.2-3B-Instruct | Q8_0 | 3.4 GB | Quality-optimized |

---

## 🔌 MCP Server API

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Server info |
| `/health` | GET | Health + platform info |
| `/models` | GET | List available models |
| `/generate` | POST | Run inference |
| `/benchmark` | POST | Full benchmark suite |
| `/mcp/tools` | GET | MCP-compatible tools listing |
| `/docs` | GET | Interactive API docs |

### Example: Generate
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is KleidiAI?", "model": "Llama-3.2-3B-Q4_K_M"}'
```

---

## ⚙️ Arm-Specific Optimizations

- **KleidiAI**: Arm's optimized kernel library for ML workloads
- **llama.cpp Arm SVE**: Scalable Vector Extension support enabled at build time
- **Native CPU tuning**: `-DLLAMA_NATIVE=ON` compiles for exact CPU microarchitecture
- **Thread optimization**: Automatically uses all available Arm cores

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

*Built for the Arm AI Optimization Challenge 2026*
