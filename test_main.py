from fastapi.testclient import TestClient

from main import app


# Testing app is based on example simulation from assessment instructions
client = TestClient(app)


# Test get points before any transactions added
# Expected response is 200 and message indicating no points
def test_get_points_when_empty():
    response = client.get("/get-points/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "You have no points"
    }


# Test add transaction that proper status code and response are returned.
# Expected response is 200 and message indicated success.
# Next 5 tests reflect the 5 transactions from assessment instructions.
def test_add_transaction_1():
    response = client.post("/add-transaction/", 
    json= { "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" })
    assert response.status_code == 200
    assert response.json() == {
        "message": "300 points successfully added for payer: DANNON"
    }


def test_add_transaction_2():
    response = client.post("/add-transaction/", 
    json= { "payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z" })
    assert response.status_code == 200
    assert response.json() == {
        "message": "200 points successfully added for payer: UNILEVER"
    }


def test_add_transaction_3():
    response = client.post("/add-transaction/", 
    json= { "payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z" })
    assert response.status_code == 200
    assert response.json() == {
        "message": "-200 points successfully added for payer: DANNON"
    }

def test_add_transaction_4():
    response = client.post("/add-transaction/", 
    json= { "payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z" })
    assert response.status_code == 200
    assert response.json() == {
        "message": "10000 points successfully added for payer: MILLER COORS"
    }


def test_add_transaction_5():
    response = client.post("/add-transaction/", 
    json= { "payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z" })
    assert response.status_code == 200
    assert response.json() == {
        "message": "1000 points successfully added for payer: DANNON"
    }
        

# Test spend points that proper status code and response are returned.
def test_spend_points():
    response = client.post("/spend-points/", json= {"points": 5000})
    assert response.status_code == 200
    assert response.json() == {
        'DANNON': -100,
        'UNILEVER': -200,
        'MILLER COORS': -4700 
    }


# Test get points that proper status code and response are returned.
def test_get_points():
    response = client.get("/get-points/")
    assert response.status_code == 200
    assert response.json() == {
        "MILLER COORS": 5300,
        "DANNON": 1000,
        "UNILEVER" : 0,
    }


# Test add transaction with negative value that would result in negative balance for payer
# Expected result is 403 (Forbidden Operation) and error message.
def test_add_negative_transaction():
    response = client.post("/add-transaction/", 
    json= { "payer": "APPLE", "points": -3000, "timestamp": "2022-10-31T10:00:00Z" })
    assert response.status_code == 403
    assert response.json() == {
        "message": "Accepting this transaction would result in negative points for payer"
    }


# Test spend points with negative value 
# Expected result is 403 (Forbidden Operation) and error message.
def test_spend_negative_points():
    response = client.post("/spend-points/", 
    json= { "points": -3000 })
    assert response.status_code == 403
    assert response.json() == {
        "message": "Cannot spend negative points"
    }


# Test spend too many points that would result in negative balance for payer
# Expected result is 403 (Forbidden Operation) and error message.
def test_spend_insufficient_points():
    response = client.post("/spend-points/", 
    json= { "points": 100000000 })
    assert response.status_code == 403
    assert response.json() == {
        "message": "Insufficient points"
    }
