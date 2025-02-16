import os
from datetime import datetime
import json
import pandas as pd
from app.services.llm_service import llm_service
from app.services.file_service import file_service
from app.config import settings

class TaskExecutor:
    async def execute_task(self, task_info: dict) -> bool:
        try:
            if task_info["task_type"] == "count_weekdays":
                return await self._handle_weekday_count(task_info)
            elif task_info["task_type"] == "sort_json":
                return await self._handle_json_sort(task_info)
            elif task_info["task_type"] == "extract_email":
                return await self._handle_email_extraction(task_info)
            # Add handlers for other task types...
            
            return True
        except Exception as e:
            print(f"Error executing task: {str(e)}")
            return False

    async def _handle_weekday_count(self, task_info):
        input_file = task_info["input_files"][0]
        output_file = task_info["output_files"][0]
        
        dates = pd.read_csv(input_file, header=None)[0]
        weekday_count = sum(pd.to_datetime(dates).dt.weekday == 2)  # 2 = Wednesday
        
        with open(output_file, 'w') as f:
            f.write(str(weekday_count))
        return True

    async def _handle_json_sort(self, task_info):
        input_file = task_info["input_files"][0]
        output_file = task_info["output_files"][0]
        
        with open(input_file, 'r') as f:
            data = json.load(f)
            
        sorted_data = sorted(data, key=lambda x: (x["last_name"], x["first_name"]))
        
        with open(output_file, 'w') as f:
            json.dump(sorted_data, f, indent=2)
        return True

    async def _handle_email_extraction(self, task_info):
        input_file = task_info["input_files"][0]
        output_file = task_info["output_files"][0]
        
        with open(input_file, 'r') as f:
            email_content = f.read()
            
        prompt = f"Extract only the sender's email address from this email:\n\n{email_content}"
        email_address = await llm_service.get_completion(prompt)
        
        with open(output_file, 'w') as f:
            f.write(email_address.strip())
        return True

task_executor = TaskExecutor()