import json
import sys
import io
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.core.kernel import NV001Kernel

app = FastAPI(title="NV001 Dashboard")

# Paths
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "web" / "static"

# Kernel Instance
kernel = NV001Kernel()

@app.on_event("startup")
async def startup_event():
    kernel.start()

@app.on_event("shutdown")
async def shutdown_event():
    kernel.stop()

@app.get("/")
async def get_index():
    index_file = STATIC_DIR / "index.html"
    return HTMLResponse(index_file.read_text(encoding="utf-8"))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    await websocket.send_json({
        "type": "log", 
        "content": "NV001 Kernel Initialized (Web Mode).\nType 'help' to see commands, or 'goal <text>' to use reasoning."
    })
    
    # Send initial state
    recent_mem = kernel.memory.get_recent_history(limit=10)
    await websocket.send_json({"type": "memory_update", "content": recent_mem})
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "command":
                cmd = message.get("content", "").strip()
                if not cmd: 
                    continue
                
                await websocket.send_json({"type": "log", "content": f"\nUSER > {cmd}"})
                
                # Execute in kernel and capture stdout
                old_stdout = sys.stdout
                sys.stdout = mystdout = io.StringIO()
                
                try:
                    kernel.execute_command(cmd)
                except Exception as e:
                    print(f"Error: {e}")
                    
                sys.stdout = old_stdout
                output = mystdout.getvalue()
                
                if output:
                    await websocket.send_json({"type": "log", "content": output.strip("\n")})
                    
                # Update frontend state
                tasks = [{"id": t.task_id, "cmd": t.command, "status": t.status} for t in kernel.tasks[-8:]]
                await websocket.send_json({"type": "tasks_update", "content": tasks})
                
                new_mem = kernel.memory.get_recent_history(limit=10)
                await websocket.send_json({"type": "memory_update", "content": new_mem})
                
    except WebSocketDisconnect:
        pass

def start_web_server(host="127.0.0.1", port=8000):
    print(f"Starting NV001 Web Dashboard at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
