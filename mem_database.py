import sqlite3
from fastapi.responses import JSONResponse

import helper
from scripts import *

# Description: Create memory database connection and transactions SQL table
# Return: Database connection
def load_mem_db():
    # Establish memory database connection
    conn_db = sqlite3.connect("file::memory:?cache=shared", uri=True, check_same_thread=False)
    curs_db = conn_db.cursor()

    # Create table with given specifications from SQL Script
    curs_db.execute(CREATE_TABLE_SCRIPT)
    conn_db.commit()
    curs_db.close()
    return conn_db


# Description: Adds transaction to transactions table
# Parameters: 
#   -transaction: request body from POST
#   -conn_db: database connection used to alter transactions table
# Return: JSONReponse with message in body and HTTP status code
def add_transaction(transaction, conn_db):
    total = transaction.points * -1
    success_message = str(transaction.points) + " points successfully added for payer: " + transaction.payer
    ret_val = {"message": success_message}
    code = 200
    curs_db = conn_db.cursor()
    check_rec = (transaction.payer, )

    # Check if transaction with payer already exists
    current_val = curs_db.execute(CHECK_EXISTS_SCRIPT, check_rec).fetchone()[0]
    
    # If payer doesn't exist in DB
    if not current_val:

        # If transaction is negative and payer doesn't exist in database
        # we return 403 as action would be Forbidden.
        if transaction.points < 0:
            code = 403
            ret_val.update({"message": "Accepting this transaction would result in negative points for payer"})
        
        # If this is the first transaction for payer and transaction
        # is positive, add to database.
        else:
            record = helper.convert_request(transaction)
            curs_db.execute(INSERT_TRANSACTION_SCRIPT, record)
    
    # If payer already exists in database
    else:
        if transaction.points < 0:

            # Grab all existing transactions for given payer
            existing_points = curs_db.execute(GET_EXISTING_POINTS_SCRIPT, check_rec).fetchall()
            new_points = int(existing_points[0][2]) + transaction.points
            i = 0

            # Loop until total negative points are completely subtracted 
            while total > 0 and existing_points:
                if new_points < 0:

                    # If negative points exceeds amount of points left for payer
                    if len(existing_points) == i: 
                        ret_val.update({"message": "Could not subtract all points."})
                        code = 403
                        break

                    # Subtract points from given transaction and update database accordingly
                    points_taken = int(existing_points[i][2]) * -1
                    record = [existing_points[i][0]]
                    record.insert(0, 0)
                    curs_db.execute(IF_EXISTS_UPDATE_SCRIPT, tuple(record))
                    total += points_taken
                    i += 1

                    # Try catch for IndexOutOfBounds Exception, while loop will end
                    try:
                        new_points = int(existing_points[i][2]) - total
                    except Exception as e:
                        new_points = transaction.points - points_taken
                        continue

                # If amount of negative points remaining no longer exceeds the record's
                # point total, perform final database update and end loop.               
                else:
                    record = [existing_points[i][0]]
                    record.insert(0, new_points)
                    curs_db.execute(IF_EXISTS_UPDATE_SCRIPT, tuple(record))
                    total = 0
        
        # If non-negative add new transaction as usual 
        else:
            record = helper.convert_request(transaction)
            curs_db.execute(INSERT_TRANSACTION_SCRIPT, record)

    # Commit database changes and close cursor
    conn_db.commit()
    curs_db.close()
    return JSONResponse(content=ret_val, status_code=code)
 

# Description: Performs changes to 'points' value in database based on input
# Parameters: 
#   -points: amount of points requested to spend
#   -conn_db: database connection used to alter transactions table
# Return: JSONReponse with message in body and HTTP status code
def spend_points(points, conn_db):
    curs_db = conn_db.cursor()
    total = points
    track_record = []
    code = 200

    # Check that user has enough points to spend 
    if points > (curs_db.execute(GET_TOTAL_POINTS).fetchone()[0] or 0):
        ret_val = {"message": "Insufficient points"}
        conn_db.commit()
        curs_db.close()
        return JSONResponse(content=ret_val, status_code=403)

    # Check that the number of points is positive
    if points < 0:
        ret_val = {"message": "Cannot spend negative points"}
        conn_db.commit()
        curs_db.close()
        return JSONResponse(content=ret_val, status_code=403)
    
    # Pull all transactions from database in order of timestamp ascending
    records = curs_db.execute(SELECT_ALL_RECORDS).fetchall()
    i = 0

    # Loop through transactions subtracting points until total value is met
    while total > 0:

        # Check if remaining total is greater than next transaction's points
        if total > records[i][2]:

            # Track the payer and points being spent
            track_record.append({records[i][1]: records[i][2] * -1})
            curs_db.execute(IF_EXISTS_UPDATE_SCRIPT, (0, records[i][0]))
            total -= records[i][2]
        
        # Case when remaining total can be spent in next transaction
        else:

            # Track the payer and points being spent
            track_record.append({records[i][1]: total * -1})

            # Update database and end loop
            curs_db.execute(IF_EXISTS_UPDATE_SCRIPT, (records[i][2] - total, records[i][0]))
            total = 0
        i += 1
    
    # Sum points for each payer, commit connection and closee cursor
    ret_val = helper.spend_points_response(track_record)
    conn_db.commit()
    curs_db.close()
    return JSONResponse(content=ret_val, status_code=code)


# Description: Gets all unique payers with a some of their total points
# Parameters: 
#   -conn_db: database connection used to alter transactions table
# Return: JSONReponse with message in body and HTTP status code
def get_points(conn_db):
    curs_db = conn_db.cursor()
    response_body = curs_db.execute(SUM_UNIQUE_COLUMNS).fetchall() or {"message": "You have no points"}
    response_body = dict(response_body)
    conn_db.commit()
    curs_db.close()
    return JSONResponse(content=response_body)
