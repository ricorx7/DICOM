from typing import Union

from fastapi import FastAPI
import redis
import json
from dicom_read import DicomReader

redis_db = redis.Redis(host='localhost', port=6379, db=0)
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """
    @param: item_id: [Required] Item ID
    @param: q: [Optional] String
    @return: Dict containing the ID and Q. 
    """
    return {"item_id": item_id, "q": q}

@app.get("/dicom_info")
def get_dicom_info(slice_file_path: str):
        """
        Get information about the DICOM image specified.
        """
        redis_key = slice_file_path + "_info"
        if redis_db.exists(redis_key):
             return json.loads(redis_db.get(redis_key))
        else:
            dicom_reader = DicomReader(slice_file_path)
            dicom_reader.display_details()
            result = dicom_reader.ds.to_json_dict()
            redis_db.set(redis_key, json.dumps(result))
            return result


# To start API server
# uvicorn dicom_api:app --reload