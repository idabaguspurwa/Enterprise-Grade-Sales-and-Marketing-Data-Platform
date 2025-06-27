WITH order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
)

SELECT
    -- Key IDs
    order_items.order_item_id,
    order_items.order_id,
    order_items.product_id,
    orders.user_id AS customer_id,

    -- Product details
    products.name AS product_name,
    products.category AS product_category,
    products.department AS product_department,

    -- Order details
    orders.order_status,
    orders.order_created_at,
    
    -- Financials
    order_items.sale_price,
    products.cost AS item_cost,
    (order_items.sale_price - products.cost) AS item_profit,

    TIMESTAMP_DIFF(orders.shipped_at, orders.order_created_at, HOUR) AS hours_to_ship

FROM order_items
LEFT JOIN orders ON order_items.order_id = orders.order_id
LEFT JOIN products ON order_items.product_id = products.product_id