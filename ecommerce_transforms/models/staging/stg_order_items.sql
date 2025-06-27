SELECT
    id AS order_item_id,
    order_id,
    user_id,
    product_id,
    sale_price
FROM
    {{ source('staging', 'order_items') }}