from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp_server.routes import router
import uvicorn

app = FastAPI(
    title="ArmBench MCP Server",
    description="KleidiAI-optimized LLM inference server for Arm64 — MCP compatible",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "name": "ArmBench MCP Server",
        "version": "1.0.0",
        "description": "Arm64-optimized LLM inference with KleidiAI",
        "docs": "/docs",
        "endpoints": ["/generate", "/benchmark", "/health", "/models"],
    }

if __name__ == "__main__":
    uvicorn.run("mcp_server.main:app", host="0.0.0.0", port=8000, reload=True)
