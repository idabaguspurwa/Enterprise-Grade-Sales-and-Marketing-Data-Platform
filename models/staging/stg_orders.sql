SELECT
    order_id,
    user_id,
    status AS order_status,    
    gender,
    created_at AS order_created_at,
    returned_at,
    shipped_at,
    delivered_at,
    num_of_item
FROM
    {{ source('staging', 'orders') }}