from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from mcp_server.routes import router
import uvicorn
import os

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
    return FileResponse("dashboard/index.html")

@app.get("/api")
def api_info():
    return {
        "name": "ArmBench MCP Server",
        "version": "1.0.0",
        "description": "Arm64-optimized LLM inference with KleidiAI",
        "docs": "/docs",
        "endpoints": ["/generate", "/benchmark", "/health", "/models"],
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("mcp_server.main:app", host="0.0.0.0", port=port, reload=True)
