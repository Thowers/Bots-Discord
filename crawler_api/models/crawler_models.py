from pydantic import BaseModel

class Criptomonedas(BaseModel):
    nombre: str
    logo: str
    precio: str
    market_cap: str