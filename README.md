# Fetch Coding Assessment: Points
Coding assessment for backend software engineer position at Fetch Rewards

# Getting Started

## Prerequisities
- Python3 installed

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

# Testing
pytest is used for automated testing. Automated testing was written based off corner cases and the example provided in the instruction.
