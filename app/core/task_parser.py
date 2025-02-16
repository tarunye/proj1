from app.services.llm_service import llm_service

class TaskParser:
    async def parse_task(self, task_description: str) -> dict:
        prompt = f"""
        Analyze the following task and break it down into structured steps:
        {task_description}
        
        Return a JSON object with:
        1. task_type: The type of task (file_operation, llm_analysis, database_query, etc.)
        2. steps: Array of steps to execute
        3. input_files: Array of input file paths
        4. output_files: Array of output file paths
        """
        
        response = await llm_service.get_completion(prompt)
        return eval(response)  # In production, use proper JSON parsing with error handling

task_parser = TaskParser()