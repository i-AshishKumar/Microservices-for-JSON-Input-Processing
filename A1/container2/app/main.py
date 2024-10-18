from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import csv

app = FastAPI()

class InputData(BaseModel):
    file: Optional[str] 
    product: str

@app.post("/sum")
async def sum_product(data: InputData):
    file_name = data.file
    product = data.product

    file_path = f"/shared_volume/{file_name}"

    sum = 0
    try:
        with open(file_path, newline='') as csvfile:
            # TEST 4: Invalid CSV format check
            csv_reader = csv.reader(csvfile, delimiter=',')
            header = next(csv_reader)
            # Checking if the header matches the expected format
            if header != ["product", "amount"]:
                return {"file": file_name, "error": "Input file not in CSV format." }
            
            # TEST 3: Calculate Sum
            # Iterate over the remaining rows in the CSV file
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if(row[0] == product):
                    sum = sum + int(row[1])
            return { "file": file_name, "sum": sum}
    except Exception as e:
        pass