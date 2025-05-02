from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Producto(BaseModel):
    name: str
    imagen: str
    precio: str