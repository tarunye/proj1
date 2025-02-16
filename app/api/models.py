from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    detail: str

class FileResponse(BaseModel):
    content: str