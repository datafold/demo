WITH users AS (
    SELECT
        user_id
    FROM {{ ref('user__created') }}
)
SELECT
    user_id
FROM users
