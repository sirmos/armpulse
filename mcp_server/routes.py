from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import time
import json
from pathlib import Path
from benchmark.models import MODELS, BENCHMARK_PROMPTS
from benchmark.runner import run_inference, run_full_benchmark
from benchmark.metrics import get_platform_info

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = "Llama-3.2-3B-Q4_K_M"
    max_tokens: Optional[int] = 200

class GenerateResponse(BaseModel):
    model: str
    prompt: str
    output: str
    tokens_per_second: float
    time_to_first_token_ms: float
    total_time_sec: float
    platform: str

class MCPTool(BaseModel):
    name: str
    description: str
    input_schema: dict

@router.get("/health")
def health():
    return {"status": "ok", "platform": get_platform_info()}

@router.get("/models")
def list_models():
    return {
        "models": [
            {
                "name": m.name,
                "quant_level": m.quant_level,
                "size_gb": m.size_gb,
                "description": m.description,
            }
            for m in MODELS
        ]
    }

@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    model_cfg = next((m for m in MODELS if m.name == request.model), MODELS[0])
    model_path = Path("models") / model_cfg.filename

    result = run_inference(model_path, request.prompt, model_cfg, request.max_tokens)

    if result.error:
        raise HTTPException(status_code=500, detail=result.error)

    return GenerateResponse(
        model=result.model_name,
        prompt=result.prompt,
        output=result.output,
        tokens_per_second=result.tokens_per_second,
        time_to_first_token_ms=result.time_to_first_token_ms,
        total_time_sec=result.total_time_sec,
        platform=result.platform,
    )

@router.post("/benchmark")
def run_benchmark():
    results = run_full_benchmark(MODELS)
    return {
        "platform": get_platform_info(),
        "total_runs": len(results),
        "results": [r.to_dict() for r in results],
        "summary": _summarize(results),
    }

@router.get("/mcp/tools")
def mcp_tools():
    """MCP-compatible tools listing endpoint."""
    return {
        "tools": [
            MCPTool(
                name="generate",
                description="Run LLM inference on Arm64 with KleidiAI optimization",
                input_schema={
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "The prompt to send to the model"},
                        "model": {"type": "string", "description": "Model name to use", "default": "Llama-3.2-3B-Q4_K_M"},
                        "max_tokens": {"type": "integer", "description": "Max tokens to generate", "default": 200},
                    },
                    "required": ["prompt"],
                },
            ),
            MCPTool(
                name="benchmark",
                description="Run full benchmark suite across all quantization levels",
                input_schema={"type": "object", "properties": {}},
            ),
        ]
    }

def _summarize(results) -> dict:
    if not results:
        return {}
    valid = [r for r in results if not r.error]
    if not valid:
        return {"error": "No valid results"}
    best = max(valid, key=lambda r: r.tokens_per_second)
    worst = min(valid, key=lambda r: r.tokens_per_second)
    avg_tps = sum(r.tokens_per_second for r in valid) / len(valid)
    return {
        "average_tokens_per_second": round(avg_tps, 2),
        "best_model": best.model_name,
        "best_tokens_per_second": round(best.tokens_per_second, 2),
        "slowest_model": worst.model_name,
        "slowest_tokens_per_second": round(worst.tokens_per_second, 2),
        "speedup_factor": round(best.tokens_per_second / worst.tokens_per_second, 2),
    }
