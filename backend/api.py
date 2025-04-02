from fastapi import FastAPI, HTTPException, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
import autoCVE
import logging
import uuid
from fastapi.middleware.cors import CORSMiddleware
import os

logger = logging.getLogger('uvicorn.error')

# Simulate task storage (in-memory)
tasks = {}

app = FastAPI()
origins = [
    os.getenv("FRONTEND_DOMAIN_FROM_BACKEND"),  # Allow Next.js app to make requests
]

CORS_POLICY = {"Access-Control-Allow-Origin": os.getenv("FRONTEND_DOMAIN_FROM_CLIENT")}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or use `["*"]` to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

def crawl_and_take_screenshot(packages, filename):
    zip_path = autoCVE.screenshot(packages.split(), filename, filename)
    tasks[filename]["zip_file"] = zip_path
    tasks[filename]["status"] = "completed" 


@app.post("/screenshot")
async def screenshot(file: UploadFile, background_tasks: BackgroundTasks):
    packages = await file.read()
    packages = packages.decode("utf-8")
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "in progress", "zip_file": None}
    logger.info("Task started with ID: %s", task_id)
    logger.info("Tasks %s", tasks)
    
    # Start the background task to crawl and create the zip file
    background_tasks.add_task(crawl_and_take_screenshot, packages, task_id)
    response_json = {"task_id": task_id, "message": "Task started. Check status to see when it's done."}
    return JSONResponse(content=response_json, media_type="application/json",headers=CORS_POLICY)


@app.get("/download/{task_id}")
async def download(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found",headers=CORS_POLICY)
    
    task = tasks[task_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task is not yet completed",headers=CORS_POLICY)
    
    zip_path = task["zip_file"]
    if zip_path and zip_path.exists():
        return FileResponse(zip_path, media_type='application/zip', filename=zip_path.name,headers=CORS_POLICY)
    else:
        raise HTTPException(status_code=404, detail="Zip file not found",headers=CORS_POLICY)
