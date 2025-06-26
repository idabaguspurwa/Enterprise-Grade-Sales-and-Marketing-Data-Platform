SELECT
    id AS product_id,
    cost,
    category,
    name,
    brand,
    retail_price,
    department,
    sku AS product_sku,
    distribution_center_id
FROM
    {{ source('staging', 'products') }}