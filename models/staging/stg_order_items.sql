SELECT
    -- IDs
    CAST(id AS INT64) AS order_item_id,
    CAST(order_id AS INT64) AS order_id,
    CAST(user_id AS INT64) AS user_id,
    CAST(product_id AS INT64) AS product_id,

    -- Timestamps
    CAST(created_at AS TIMESTAMP) AS created_at,
    CAST(shipped_at AS TIMESTAMP) AS shipped_at,
    CAST(delivered_at AS TIMESTAMP) AS delivered_at,
    CAST(returned_at AS TIMESTAMP) AS returned_at,

    -- Financials
    CAST(sale_price AS FLOAT64) AS sale_price
FROM
    {{ source('staging', 'order_items') }}