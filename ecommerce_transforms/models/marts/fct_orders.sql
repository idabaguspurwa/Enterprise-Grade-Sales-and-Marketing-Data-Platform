WITH order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
)

SELECT
    -- Key IDs
    order_items.order_item_id,
    order_items.order_id,
    orders.user_id AS customer_id,
    order_items.product_id,

    -- Order details
    orders.order_status,
    orders.order_created_at,

    -- Financials
    order_items.sale_price

FROM order_items
LEFT JOIN orders ON order_items.order_id = orders.order_id