from fastapi import FastAPI, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from typing import List
import pandas as pd

import logging
import multiprocessing
import os
import sys
import tempfile
import threading
import time
import uvicorn
import webbrowser
import platform
import subprocess
    
from process import format_files, process_dataframes

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Update static files mount
app.mount("/static", StaticFiles(directory=os.path.join(get_base_path(), "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(get_base_path(), "static/index.html")) as f:
        return f.read()

@app.post("/api/process-files")
async def process_files(files: List[UploadFile]):
    sorted_files = sorted(files, key=lambda x: x.filename)
    formatted_dfs = await format_files(sorted_files)
    
    sorted_file_names = [x.filename for x in sorted_files]
    output_dfs = process_dataframes(formatted_dfs, sorted_file_names)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        with pd.ExcelWriter(tmp.name) as writer:
            for sheet_name, output_df in output_dfs.items():
                output_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
        return FileResponse(tmp.name, filename="output.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    return {"results": results}


logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Global error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred"}
    )

if __name__ == '__main__':
    def open_browser():
        try:
            time.sleep(1.5)  # Wait for the server to start
            print("Attempting to open browser...")
            
            system = platform.system().lower()
            try:
                if system == 'darwin':  # macOS
                    subprocess.run(['open', 'http://localhost:3333'])
                elif system == 'windows':
                    subprocess.run(['cmd', '/c', 'start', 'http://localhost:3333'])
                elif system == 'linux':
                    subprocess.run(['xdg-open', 'http://localhost:3333'])
                print(f"Attempted to open browser using {system} system command")
            except Exception as e:
                print(f"System command failed: {e}")
                
        except Exception as e:
            print(f"Error in open_browser function: {e}")
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    multiprocessing.freeze_support()
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=3333, reload=False, workers=1)