#!/bin/bash
# Run the full ArmBench benchmark suite
set -e

source .venv/bin/activate 2>/dev/null || true

echo "⚡ Starting ArmBench Benchmark..."
echo "Platform: $(uname -m)"
echo ""

python3 -c "
from benchmark.runner import run_full_benchmark
from benchmark.models import MODELS
import json, datetime

results = run_full_benchmark(MODELS)
output = {
    'timestamp': datetime.datetime.utcnow().isoformat(),
    'results': [r.to_dict() for r in results]
}
with open('benchmark_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print('')
print('✅ Results saved to benchmark_results.json')
"
