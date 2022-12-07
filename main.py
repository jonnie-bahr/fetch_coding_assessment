import fastapi
from fastapi.responses import JSONResponse

from models import *
import mem_database as db

# Start API
app = fastapi.FastAPI()

# Load global memory DB connection to be passed through methods
conn_db = db.load_mem_db()


# Endpoint for add-transaction
# Request: {"payer": string, "points": int, "timestamp": string}
# Response: {"message": string}
# Response is message indicating result of transaction
@app.post('/add-transaction/')
async def add_transaction(request: AddTransactionRequest):
    response = JSONResponse
    try:
        response = db.add_transaction(request, conn_db)
    except Exception as e:
        response.status_code = 500
        response.content = str(e)
    return response


# Endpoint for spend-points
# Request: {"points": int}
# Response: {string: int, ...} -> {payer: points spent, ...}
# Response is dictionary where key is payer and value is how many points
# were spent from that payer. 
@app.post('/spend-points/')
async def spend_points(request: SpendPointsRequest):
    response = JSONResponse
    try:
        response = db.spend_points(request.points, conn_db)
    except Exception as e:
        response.status_code = 500
        response.content = str(e)
    return response

# Endpoint for spend-points
# Request: GET with no body
# Response: {string: int, ...} -> {payer: points remaining, ...}
# Response is dictionary where key is payer and value is how many points
# are remaining for payer. Payers ordered by most points remaining first. 
@app.get('/get-points/')
async def get_points():
    response = JSONResponse
    try:
        response = db.get_points(conn_db)
    except Exception as e:
        response.content = str(e)
        response.status_code = 500
    return response