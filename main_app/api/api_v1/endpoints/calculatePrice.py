import logging

import uuid

import subprocess

from dotenv import load_dotenv

from fastapi import APIRouter, Form, Request, File, UploadFile
import os
import re
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

import shutil
from tempfile import mkdtemp

from main_app.db_models import PotentialOrdersFromEstimate

from main_app.schemas import calculatePriceResponse

router = APIRouter()

templates = Jinja2Templates(directory="templates")

load_dotenv()

router = APIRouter()


@router.post("/")
async def calculate_price(
    request: Request, to_calculate: UploadFile = File(...)
) -> calculatePriceResponse:
    file_extension = os.path.splitext(to_calculate.filename)[1]
    if file_extension.lower() != ".stl":
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid file format. Only .stl files are allowed."},
        )

    unique_dir = mkdtemp()
    stl_file_path = os.path.join(unique_dir, f"{uuid.uuid4()}.stl")
    gcode_file_path = os.path.join(unique_dir, f"{uuid.uuid4()}.gcode")

    with open(stl_file_path, "wb") as tmp_stl_file:
        shutil.copyfileobj(to_calculate.file, tmp_stl_file)

    command = f"prusaslicer --load /usr/src/app/config.ini --export-gcode --layer-height 0.2 --output {gcode_file_path} {stl_file_path}"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error:", result.stderr)
        shutil.rmtree(unique_dir)
        return JSONResponse(
            status_code=500, content={"message": "Error processing the file."}
        )

    filament_used = 0.0
    total_hours = 0.0

    try:
        with open(gcode_file_path, "r") as gcode_file:
            for line in gcode_file:
                if "filament used [g]" in line:
                    filament_used_match = re.search(r"(\d+(\.\d+)?)", line)
                    if filament_used_match:
                        filament_used = float(filament_used_match.group(1))
                elif "estimated printing time" in line:
                    try:
                        time_match = re.search(r"(\d+)h (\d+)m (\d+)s", line)
                        if time_match:
                            hours = int(time_match.group(1))
                            minutes = int(time_match.group(2))
                            seconds = int(time_match.group(3))
                            total_hours = hours + minutes / 60 + seconds / 3600
                        else:
                            time_match = re.search(r"(\d+)m (\d+)s", line)
                            if time_match:
                                minutes = int(time_match.group(1))
                                seconds = int(time_match.group(2))
                                total_hours = minutes / 60 + seconds / 3600
                            else:
                                time_match = re.search(r"(\d+)s", line)
                                if time_match:
                                    seconds = int(time_match.group(1))
                                    total_hours = seconds / 3600
                    except:
                        raise Exception("Error parsing the estimated printing time.")
    finally:
        shutil.rmtree(unique_dir)

    price = 6 + (total_hours * 1.75)+ (filament_used * 0.05)

    price = round(price, 1)
    total_hours = round(total_hours, 2)
    filament_used = round(filament_used, 2)

    new_order = PotentialOrdersFromEstimate(
        orderValue=price,
        printTime=total_hours,
        filamentUsed=filament_used,
    )
    await new_order.save().run()

    return calculatePriceResponse(
        price=price,
        filament_used=filament_used,
        total_hours=total_hours,
        order_id=str(new_order.orderID),
    )
