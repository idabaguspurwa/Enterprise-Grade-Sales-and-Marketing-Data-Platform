WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
)

SELECT
    -- IDs
    order_items.order_item_id,
    order_items.order_id,
    order_items.user_id AS customer_id,
    order_items.product_id,

    -- Timestamps
    orders.created_at AS order_created_at,
    order_items.shipped_at,
    order_items.delivered_at,
    order_items.returned_at,

    -- Order details
    orders.num_of_item AS items_in_order,
    orders.status AS order_status,

    -- Financials
    order_items.sale_price AS item_sale_price

FROM order_items
LEFT JOIN orders ON order_items.order_id = orders.order_id