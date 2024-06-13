WITH users AS (
    SELECT
        user_id
    FROM {{ ref('user_created') }}
)
SELECT
    user_id
FROM users
