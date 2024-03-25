import logging

import subprocess

from dotenv import load_dotenv

from fastapi import APIRouter, Form, Request, File, UploadFile
import os
from fastapi.responses import JSONResponse

router = APIRouter()

load_dotenv()



router = APIRouter()

@router.post("/")
async def calculate_price(to_calculate: UploadFile = File(...)):
  """
  Calculate the price of the plastic based on the given data.

  Parameters:
  - to_calculate (file): The file containing the data to calculate the price.

  Returns:
  - JSONResponse: The response containing the calculated price.
  """
  file_extension = os.path.splitext(to_calculate.filename)[1]
  if file_extension.lower() != ".stl":
    return JSONResponse(status_code=400, content={"message": "Invalid file format. Only .stl files are allowed."})
  
  command = "slic3r --help"

  # Execute the command
  result = subprocess.run(command, shell=True, capture_output=True, text=True)

  # Print the output
  print(result.stdout)

  if result.stderr:
    print("Error:", result.stderr)
  
  return {"price": 0.0}
