CREATE_TABLE_SCRIPT="""
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payer TEXT,
    points INTEGER,
    timestamp TEXT
);
"""
INSERT_TRANSACTION_SCRIPT="""
INSERT INTO transactions(payer,points,timestamp)
VALUES(?,?,?)
"""
CHECK_EXISTS_SCRIPT="""
SELECT IIF(
    EXISTS (
            SELECT * FROM transactions WHERE payer = ?
        ), 
        1, 
        0)
"""
IF_EXISTS_UPDATE_SCRIPT="""
UPDATE transactions
SET points = ?
WHERE id = ?
"""
GET_EXISTING_POINTS_SCRIPT="""
SELECT * FROM transactions 
WHERE payer = ? 
ORDER BY timestamp ASC
"""
DELETE_USED_TANSACTIONS="""
DELETE FROM transactions
WHERE points = 0
"""
SUM_UNIQUE_COLUMNS="""
SELECT payer, SUM(points)
FROM transactions
GROUP BY payer
ORDER BY SUM(points) DESC
"""
SELECT_ALL_RECORDS="""
SELECT id, payer, points
FROM transactions
WHERE points != 0
ORDER BY timestamp ASC
"""
GET_TOTAL_POINTS="""
SELECT SUM(points)
FROM transactions
"""
GET_TOTAL_POINTS_BY_PAYER="""
SELECT SUM(points)
FROM transactions
where payer = ?
"""
