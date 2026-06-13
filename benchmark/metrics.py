import time
import psutil
import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BenchmarkResult:
    model_name: str
    quant_level: str
    prompt: str
    output: str = ""
    prompt_tokens: int = 0
    output_tokens: int = 0
    time_to_first_token_ms: float = 0.0
    total_time_sec: float = 0.0
    tokens_per_second: float = 0.0
    memory_used_mb: float = 0.0
    model_size_gb: float = 0.0
    platform: str = ""
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "model_name": self.model_name,
            "quant_level": self.quant_level,
            "prompt_preview": self.prompt[:60] + "...",
            "output_tokens": self.output_tokens,
            "time_to_first_token_ms": round(self.time_to_first_token_ms, 2),
            "total_time_sec": round(self.total_time_sec, 2),
            "tokens_per_second": round(self.tokens_per_second, 2),
            "memory_used_mb": round(self.memory_used_mb, 2),
            "model_size_gb": self.model_size_gb,
            "platform": self.platform,
            "error": self.error,
        }

def get_memory_usage_mb() -> float:
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def get_platform_info() -> str:
    import platform
    machine = platform.machine()
    processor = platform.processor()
    system = platform.system()
    cpu_count = psutil.cpu_count()
    return f"{system} | {machine} | {processor} | {cpu_count} CPUs"
