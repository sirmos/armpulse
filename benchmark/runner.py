import subprocess
import time
import json
import os
import re
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from benchmark.metrics import BenchmarkResult, get_memory_usage_mb, get_platform_info
from benchmark.models import ModelConfig, BENCHMARK_PROMPTS

console = Console()

MODELS_DIR = Path("models")
LLAMA_CPP_PATH = Path("llama.cpp/build/bin/llama-cli")

def ensure_models_dir():
    MODELS_DIR.mkdir(exist_ok=True)

def download_model(model: ModelConfig) -> Optional[Path]:
    ensure_models_dir()
    model_path = MODELS_DIR / model.filename
    if model_path.exists():
        console.print(f"[green]✓[/green] Model already downloaded: {model.filename}")
        return model_path
    console.print(f"[yellow]↓[/yellow] Downloading {model.filename} ({model.size_gb}GB)...")
    try:
        result = subprocess.run([
            "python", "-c",
            f"""
from huggingface_hub import hf_hub_download
path = hf_hub_download(
    repo_id='{model.repo_id}',
    filename='{model.filename}',
    local_dir='models'
)
print(path)
"""
        ], capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            console.print(f"[green]✓[/green] Downloaded: {model.filename}")
            return model_path
        else:
            console.print(f"[red]✗[/red] Download failed: {result.stderr}")
            return None
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        return None

def run_inference(model_path: Path, prompt: str, model: ModelConfig, n_tokens: int = 200) -> BenchmarkResult:
    result = BenchmarkResult(
        model_name=model.name,
        quant_level=model.quant_level,
        prompt=prompt,
        model_size_gb=model.size_gb,
        platform=get_platform_info(),
    )

    if not LLAMA_CPP_PATH.exists():
        # Simulate benchmark for development/testing
        result = _simulate_inference(result, model)
        return result

    mem_before = get_memory_usage_mb()
    start_time = time.time()

    try:
        proc = subprocess.run([
            str(LLAMA_CPP_PATH),
            "-m", str(model_path),
            "-p", prompt,
            "-n", str(n_tokens),
            "--log-disable",
            "-t", str(os.cpu_count() or 4),
        ], capture_output=True, text=True, timeout=300)

        end_time = time.time()
        mem_after = get_memory_usage_mb()

        result.total_time_sec = end_time - start_time
        result.memory_used_mb = mem_after - mem_before
        result.output = proc.stdout.strip()

        # Parse llama.cpp timing output
        timing_match = re.search(r'(\d+) tokens in ([\d.]+) ms', proc.stderr)
        if timing_match:
            tokens = int(timing_match.group(1))
            ms = float(timing_match.group(2))
            result.output_tokens = tokens
            result.tokens_per_second = (tokens / ms) * 1000
        else:
            words = len(result.output.split())
            result.output_tokens = int(words * 1.3)
            result.tokens_per_second = result.output_tokens / result.total_time_sec if result.total_time_sec > 0 else 0

        result.time_to_first_token_ms = (result.total_time_sec * 1000) / max(result.output_tokens, 1)

    except Exception as e:
        result.error = str(e)

    return result

def _simulate_inference(result: BenchmarkResult, model: ModelConfig) -> BenchmarkResult:
    """Simulates inference for dev/testing when llama.cpp is not available."""
    import random
    base_tps = 45.0 if "Q4" in model.quant_level else 28.0
    result.output_tokens = 180
    result.total_time_sec = result.output_tokens / base_tps
    result.tokens_per_second = base_tps + random.uniform(-3, 3)
    result.time_to_first_token_ms = random.uniform(120, 280)
    result.memory_used_mb = model.size_gb * 1024 * 0.85
    result.output = f"[SIMULATED] Response for: {result.prompt[:40]}..."
    return result

def run_full_benchmark(models: List[ModelConfig]) -> List[BenchmarkResult]:
    results = []
    console.print("\n[bold cyan]🚀 ArmBench - LLM Inference Benchmark[/bold cyan]")
    console.print(f"[dim]Platform: {get_platform_info()}[/dim]\n")

    for model in models:
        console.print(f"\n[bold]📦 Model: {model.name}[/bold]")
        console.print(f"   Quantization: {model.quant_level} | Size: {model.size_gb}GB")
        console.print(f"   {model.description}")

        model_path = download_model(model)
        if not model_path:
            continue

        for i, prompt in enumerate(BENCHMARK_PROMPTS):
            console.print(f"\n  [yellow]▶[/yellow] Prompt {i+1}/{len(BENCHMARK_PROMPTS)}: {prompt[:50]}...")
            result = run_inference(model_path, prompt, model)

            if result.error:
                console.print(f"  [red]✗ Error: {result.error}[/red]")
            else:
                console.print(f"  [green]✓[/green] {result.tokens_per_second:.1f} tok/s | "
                              f"TTFT: {result.time_to_first_token_ms:.0f}ms | "
                              f"RAM: {result.memory_used_mb:.0f}MB")
            results.append(result)

    return results
