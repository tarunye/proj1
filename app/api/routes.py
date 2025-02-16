from fastapi import APIRouter, HTTPException
from app.core.task_parser import task_parser
from app.core.task_executor import task_executor
import os
from app.config import settings

router = APIRouter()

@router.post("/run")
async def run_task(task: str):
    try:
        # Parse the task
        task_info = await task_parser.parse_task(task)
        
        # Security check: ensure all paths are within /data
        for path in task_info["input_files"] + task_info["output_files"]:
            if not path.startswith(settings.DATA_DIR):
                raise HTTPException(status_code=400, message="Invalid file path")
        
        # Execute the task
        success = await task_executor.execute_task(task_info)
        
        if not success:
            raise HTTPException(status_code=500, detail="Task execution failed")
            
        return {"status": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/read")
async def read_file(path: str):
    if not path.startswith(settings.DATA_DIR):
        raise HTTPException(status_code=400, detail="Invalid file path")
        
    try:
        with open(path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))