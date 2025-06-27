SELECT
    user_id AS customer_id,
    first_name,
    last_name,
    email,
    age,
    gender,
    city,
    state,
    country,
    traffic_source,
    EXTRACT(YEAR FROM created_at) AS registration_year
FROM
    {{ ref('stg_users') }}