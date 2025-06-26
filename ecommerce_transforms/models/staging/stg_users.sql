SELECT
    id AS user_id,
    first_name,
    last_name,
    email,
    age,
    gender,
    state,
    street_address,
    postal_code,
    city,
    country,
    traffic_source,
    created_at
FROM
    {{ source('staging', 'users') }}