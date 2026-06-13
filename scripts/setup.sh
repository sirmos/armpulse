#!/bin/bash
# ArmBench Setup Script for Arm64 (Oracle Cloud, AWS Graviton, etc.)
set -e

echo "⚡ ArmBench Setup — Arm64 Optimized"
echo "====================================="
echo "Platform: $(uname -m) | $(uname -s)"
echo ""

# 1. System dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y \
    git cmake build-essential \
    python3 python3-pip python3-venv \
    wget curl libgomp1

# 2. Python virtual environment
echo ""
echo "🐍 Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install huggingface-hub -q
echo "✅ Python environment ready"

# 3. Build llama.cpp with Arm optimizations
echo ""
echo "🔨 Building llama.cpp with Arm64 optimizations..."
if [ ! -d "llama.cpp" ]; then
    git clone https://github.com/ggerganov/llama.cpp.git --depth=1
fi
cd llama.cpp
cmake -B build \
    -DLLAMA_NATIVE=ON \
    -DLLAMA_ARM_SVE=ON \
    -DLLAMA_BLAS=OFF \
    -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j$(nproc)
cd ..
echo "✅ llama.cpp built with Arm64 optimizations"

# 4. Verify Arm features
echo ""
echo "🔍 Detected Arm CPU features:"
grep -m1 "model name" /proc/cpuinfo || echo "  CPU info unavailable"
grep "Features" /proc/cpuinfo | head -1 || true
python3 -c "
import platform, psutil
print(f'  Machine : {platform.machine()}')
print(f'  CPUs    : {psutil.cpu_count()}')
print(f'  RAM     : {psutil.virtual_memory().total // (1024**3)} GB')
"

echo ""
echo "✅ Setup complete! Run the benchmark:"
echo "   source .venv/bin/activate"
echo "   bash scripts/run_benchmark.sh"
