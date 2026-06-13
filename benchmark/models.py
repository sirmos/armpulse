from dataclasses import dataclass
from typing import List

@dataclass
class ModelConfig:
    name: str
    repo_id: str
    filename: str
    quant_level: str
    description: str
    size_gb: float

# Models we benchmark - from smallest to largest quantization
MODELS: List[ModelConfig] = [
    ModelConfig(
        name="Llama-3.2-3B-Q4_K_M",
        repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
        filename="Llama-3.2-3B-Instruct-Q4_K_M.gguf",
        quant_level="Q4_K_M",
        description="4-bit quantized - best speed/quality balance",
        size_gb=1.9,
    ),
    ModelConfig(
        name="Llama-3.2-3B-Q8_0",
        repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
        filename="Llama-3.2-3B-Instruct-Q8_0.gguf",
        quant_level="Q8_0",
        description="8-bit quantized - higher quality, more memory",
        size_gb=3.4,
    ),
]

BENCHMARK_PROMPTS = [
    "Explain what KleidiAI is and how it optimizes AI on Arm processors.",
    "What are the key advantages of running LLMs on Arm Neoverse servers?",
    "Write a short Python function to calculate fibonacci numbers.",
]
