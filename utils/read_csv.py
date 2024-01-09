from fastapi import HTTPException, UploadFile, status
from database import models
import io, csv
import pandas as pd

COLUMNS = list(models.Items.model_fields.keys())


def csv_reader(binary_data: bytes):
    """file object"""

    file_stream = io.StringIO(binary_data.decode())
    file_data = csv.DictReader(file_stream)
    dict_items = [row for row in file_data]

    return dict_items


def panda_reader(binary_data: bytes, file: UploadFile):
    """using pands to read data"""

    file_stream = io.BytesIO(binary_data)

    if file.content_type == "text/csv":
        try:
            df = pd.read_csv(file_stream, usecols=COLUMNS)

        except ValueError as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"could not find {COLUMNS} in file",
            )

    else:
        try:
            df = pd.read_excel(file_stream, usecols=COLUMNS)

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"could not find {COLUMNS} in file",
            )

    return df.to_dict(orient="records")
