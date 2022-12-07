from pydantic import BaseModel


class AddTransactionRequest(BaseModel):
    payer: str
    points: int
    timestamp: str

class SpendPointsRequest(BaseModel):
    points: int
