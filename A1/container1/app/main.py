from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import requests
import os

app = FastAPI()

class InputData(BaseModel):
    file: Optional[str]  # Optional file name because file name can be None/null
    product: str

@app.post("/calculate")
async def calculate(data: InputData):
    file_name = data.file
    product = data.product
    
    file_path = f"/shared_volume/{file_name}"

    # TEST 1: Null Check
    # Check if the file name is None and return an error if it is
    if file_name == None:
        return {"file": None, "error": "Invalid JSON input."}

    # TEST 2: File not found
    # Check if the file does not exist at the specified path and return an error if it doesn't
    if not os.path.exists(file_path):
        return {"file": file_name, "error": "File not found."}

    # Sending a POST request to another container's endpoint to perform the sum calculation
    response = requests.post("http://container2:7000/sum", json={"file": file_name, "product": product})
    return response.json()
