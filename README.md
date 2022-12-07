# Fetch Coding Assessment: Points
Coding assessment for backend software engineer position at Fetch Rewards

# Getting Started

## Prerequisities
- Python3 installed with pip

## Install packages in shell
```
bash
cd fetch_coding_assessment
make setup
```

## Run API in shell
```
bash
cd fetch_coding_assessment
make run
```

## Run tests in shell
```
bash
cd fetch_coding_assessment
make test
```

# Documentation

## OpenAPI Documentation
With API running, visit http://localhost:8000/docs or http://127.0.0.1:8000/docs to view FastAPI's automatically generated Documentation.

## Manual Documentation

Using makefile to run API above will automatically host the API at http://localhost:8000/ or http://127.0.0.1:8000 <br />
See endpoint details below for specific API interaction examples using curl. <br />
Expected responses for examples assume you executed only the example API calls and that they were executed in the order presented.

### /add-transaction/
Method: POST <br />
Parameters: None <br />
Request Body:
```
  {
    "payer": "string",
    "points": int,
    "timestamp": "string"
  }
```
Response Body:
```
  {
    "message": "string"
  }
```
Example:
```
curl -X POST http://localhost:8000/add-transaction/ -H 'Content-Type: application/json' -d '{"payer":"DANNON","points":100, "timestamp": "2022-11-02T14:00:00Z"}'
```
Expected Response:

```
{"message":"100 points successfully added for payer: DANNON"}
```

### /spend-points/
Method: POST <br />
Parameters: None <br />
Request Body:
```
  {
    "points": int
  }
```
Response Body: response body is a dictionary with keys = payer and value = points spent
```
  {
    payer: int
    ...
  }
```
Example:
```
curl -X POST http://localhost:8000/spend-points/ -H 'Content-Type: application/json' -d '{"points":50}'  
```
Expected Response:
```
{"DANNON":-50}
```

### /get-points/
Method: GET <br />
Parameters: None <br />
Request Body: None <br />
Response Body: response body is a dictionary with keys = payer and value = points remaining
```
  {
    payer: int
    ...
  }
```
Example:
```
curl -X GET http://localhost:8000/get-points/ 
```
Expected Response:
```
{"DANNON":50}
```

# Testing
pytest is used for automated testing. Automated testing was written based off corner cases and the example provided in the instruction.
