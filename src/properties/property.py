from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class PropertyData(BaseModel):
    id: str
    parent_url: str
    url: str
    created_timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_timestamp: str = None
    data: Dict = None