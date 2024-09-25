from snowflake.connector import connect
import random


# %% Execute query without reading data

def run_query_in_sf(sql_query):

    conn = connect(
        user = os.environ['SNOWFLAKE_USER'],
        password = os.environ['SNOWFLAKE_PASSWORD'],
        account = os.environ['SNOWFLAKE_ACCOUNT'],
        role = os.environ['SNOWFLAKE_ROLE']
        )

    cursor = conn.cursor()
    cursor.execute(sql_query)
    cursor.close()
    conn.close()



q1 = """
create or replace table demo.diff.transaction_history as (
  select * from demo.diff.transactions_v1_10m where "transaction_id" <= 1000000
);
"""

q2 = """
create or replace table demo.diff.transaction_history as (

select
    CASE 
        WHEN uniform(1, 100, random()) <= 1 THEN FLOOR(RANDOM() * (1000000 - 1 + 1)) + 1
        WHEN uniform(1, 100, random()) <= 1 THEN null
        ELSE "transaction_id"
    END AS "transaction_id"

    , CASE 
        WHEN uniform(1, 100, random()) <= 1
            THEN
                UPPER(
                    CHR(65 + MOD(ABS(HASH(RANDOM())), 26)) ||
                    CHR(65 + MOD(ABS(HASH(RANDOM())), 26)) ||
                    CHR(65 + MOD(ABS(HASH(RANDOM())), 26)) ||
                    CHR(65 + MOD(ABS(HASH(RANDOM())), 26)) ||
                    CHR(65 + MOD(ABS(HASH(RANDOM())), 26)) 
                )
        WHEN uniform(1, 100, random()) <= 1 THEN null
        ELSE "first_name"
    END AS "first_name"
    
    , "last_name"
    , CASE 
        WHEN uniform(1, 100, random()) <= 1 THEN dateadd(day, -1, "created_at")
        WHEN uniform(1, 100, random()) <= 1 THEN null
        ELSE "created_at"
    END AS "created_at"
    , "updated_at"
    , CASE 
        WHEN uniform(1, 100, random()) <= 1 THEN "amount" * 2
        WHEN uniform(1, 100, random()) <= 1 THEN null
        ELSE "amount"
    END AS "amount"
    , "amount_base"
    , "discount"
    , "number_of_attempts"
    , "number_of_products"
    , "score"
from (select * from demo.diff.transactions_v1_10m where "transaction_id" <= 1000000)

);
"""


if random.randint(1, 100) <= 10:
    print('broken')
    run_query_in_sf(q2)
else:
    print('healthy')
    run_query_in_sf(q1)
