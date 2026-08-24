from database import execute_query


def get_total_revenue():

    query = """
        SELECT
            SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
    """

    return execute_query(query)

def get_top_products(limit=10):

    query = """
        SELECT
            p.product_id,
            p.product_name,
            SUM(oi.quantity) AS units_sold,
            SUM(oi.quantity * oi.unit_price) AS revenue
        FROM products p
        JOIN order_items oi
            ON p.product_id = oi.product_id
        JOIN orders o
            ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT %s
    """

    return execute_query(query, (limit,))

def get_top_customers(limit=10):

    query = """
        SELECT
            c.customer_id,
            c.customer_name,
            SUM(oi.quantity * oi.unit_price) AS total_spending,
            COUNT(DISTINCT o.order_id) AS number_of_orders
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spending DESC
        LIMIT %s
    """

    return execute_query(query, (limit,))

def get_monthly_sales():

    query = """
        SELECT
            DATE_FORMAT(o.order_date, '%Y-%m') AS month,
            SUM(oi.quantity * oi.unit_price) AS revenue,
            COUNT(DISTINCT o.order_id) AS orders
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
        ORDER BY month;
    """

    return execute_query(query)

def get_inventory_risks():

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            i.stock_quantity,
            i.reorder_level,
            (i.reorder_level - i.stock_quantity) AS stock_deficit
        FROM products p
        JOIN inventory i
            ON p.product_id = i.product_id
        WHERE i.stock_quantity < i.reorder_level
        ORDER BY stock_deficit DESC;
    """

    return execute_query(query)

def get_customer_activity():

    query = """
        SELECT
            c.customer_id,
            c.customer_name,
            MAX(o.order_date) AS last_ordered_date,
            DATEDIFF(
                CURRENT_DATE,
                MAX(o.order_date)
            ) AS days_since_last_order,
            COUNT(DISTINCT o.order_id) AS completed_orders,
            SUM(oi.quantity * oi.unit_price) AS total_spending
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY c.customer_id, c.customer_name
        ORDER BY days_since_last_order DESC;
    """

    return execute_query(query)

def get_product_profitability(limit=10):

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,

            SUM(oi.quantity) AS units_sold,

            SUM(oi.quantity * oi.unit_price) AS revenue,

            SUM(
                oi.quantity * (oi.unit_price - p.cost)
            ) AS profit,

            ROUND(
                SUM(
                    oi.quantity * (oi.unit_price - p.cost)
                )
                /
                SUM(oi.quantity * oi.unit_price)
                * 100,
                2
            ) AS profit_margin

        FROM products p

        JOIN order_items oi
            ON p.product_id = oi.product_id

        JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.status = 'Completed'

        GROUP BY
            p.product_id,
            p.product_name,
            p.category

        ORDER BY profit DESC

        LIMIT %s
    """

    return execute_query(query, (limit,))

def get_supplier_performance():

    query = """
        SELECT
            s.supplier_id,
            s.supplier_name,

            COUNT(DISTINCT p.product_id) AS products_supplied,

            SUM(oi.quantity) AS units_sold,

            SUM(
                oi.quantity * oi.unit_price
            ) AS revenue,

            SUM(
                oi.quantity * (oi.unit_price - p.cost)
            ) AS profit

        FROM suppliers s

        JOIN products p
            ON s.supplier_id = p.supplier_id

        JOIN order_items oi
            ON p.product_id = oi.product_id

        JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.status = 'Completed'

        GROUP BY
            s.supplier_id,
            s.supplier_name

        ORDER BY profit DESC;
    """

    return execute_query(query)

def get_reorder_priorities(limit=20):

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,

            i.stock_quantity,
            i.reorder_level,

            COALESCE(
                SUM(
                    CASE
                        WHEN o.status = 'Completed'
                        THEN oi.quantity
                        ELSE 0
                    END
                ),
                0
            ) AS units_sold,

            ROUND(
                COALESCE(
                    SUM(
                        CASE
                            WHEN o.status = 'Completed'
                            THEN oi.quantity
                            ELSE 0
                        END
                    ),
                    0
                ) / 30,
                2
            ) AS estimated_daily_sales,

            CASE
                WHEN
                    COALESCE(
                        SUM(
                            CASE
                                WHEN o.status = 'Completed'
                                THEN oi.quantity
                                ELSE 0
                            END
                        ),
                        0
                    ) = 0
                THEN NULL

                ELSE ROUND(
                    i.stock_quantity /
                    (
                        COALESCE(
                            SUM(
                                CASE
                                    WHEN o.status = 'Completed'
                                    THEN oi.quantity
                                    ELSE 0
                                END
                            ),
                            0
                        ) / 30
                    ),
                    2
                )
            END AS estimated_days_of_stock

        FROM products p

        JOIN inventory i
            ON p.product_id = i.product_id

        LEFT JOIN order_items oi
            ON p.product_id = oi.product_id

        LEFT JOIN orders o
            ON oi.order_id = o.order_id

        GROUP BY
            p.product_id,
            p.product_name,
            p.category,
            i.stock_quantity,
            i.reorder_level

        HAVING
            i.stock_quantity < i.reorder_level

        ORDER BY
            estimated_days_of_stock ASC

        LIMIT %s
    """

    return execute_query(query, (limit,))

def get_customer_risk(limit=20):

    query = """
        SELECT
            c.customer_id,
            c.customer_name,

            COUNT(DISTINCT o.order_id) AS completed_orders,

            SUM(
                oi.quantity * oi.unit_price
            ) AS total_spending,

            MAX(o.order_date) AS last_order_date,

            DATEDIFF(
                CURRENT_DATE,
                MAX(o.order_date)
            ) AS days_since_last_order,

            CASE
                WHEN DATEDIFF(
                    CURRENT_DATE,
                    MAX(o.order_date)
                ) >= 180
                AND SUM(
                    oi.quantity * oi.unit_price
                ) >= 100000
                    THEN 'HIGH'

                WHEN DATEDIFF(
                    CURRENT_DATE,
                    MAX(o.order_date)
                ) >= 90
                    THEN 'MEDIUM'

                ELSE 'LOW'
            END AS risk_level

        FROM customers c

        JOIN orders o
            ON c.customer_id = o.customer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        WHERE o.status = 'Completed'

        GROUP BY
            c.customer_id,
            c.customer_name

        HAVING
            days_since_last_order >= 90

        ORDER BY
            CASE risk_level
                WHEN 'HIGH' THEN 1
                WHEN 'MEDIUM' THEN 2
                ELSE 3
            END,
            total_spending DESC

        LIMIT %s
    """

    return execute_query(query, (limit,))

def get_sales_profitability_gaps(limit=20):

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,

            SUM(oi.quantity) AS units_sold,

            SUM(
                oi.quantity * oi.unit_price
            ) AS revenue,

            SUM(
                oi.quantity * (oi.unit_price - p.cost)
            ) AS profit,

            ROUND(
                SUM(
                    oi.quantity * (oi.unit_price - p.cost)
                )
                /
                SUM(
                    oi.quantity * oi.unit_price
                )
                * 100,
                2
            ) AS profit_margin

        FROM products p

        JOIN order_items oi
            ON p.product_id = oi.product_id

        JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.status = 'Completed'

        GROUP BY
            p.product_id,
            p.product_name,
            p.category

        HAVING
            SUM(oi.quantity) >= 100
            AND
            (
                SUM(
                    oi.quantity * (oi.unit_price - p.cost)
                )
                /
                SUM(
                    oi.quantity * oi.unit_price
                )
            ) < 0.15

        ORDER BY
            revenue DESC

        LIMIT %s
    """

    return execute_query(query, (limit,))

def get_business_health():

    query = """
        SELECT

            /* Total Revenue */
            (
                SELECT COALESCE(
                    SUM(oi.quantity * oi.unit_price),
                    0
                )
                FROM orders o
                JOIN order_items oi
                    ON o.order_id = oi.order_id
                WHERE o.status = 'Completed'
            ) AS total_revenue,

            /* Completed Orders */
            (
                SELECT COUNT(*)
                FROM orders
                WHERE status = 'Completed'
            ) AS completed_orders,

            /* Total Products */
            (
                SELECT COUNT(*)
                FROM products
            ) AS total_products,

            /* Low Stock Products */
            (
                SELECT COUNT(*)
                FROM inventory
                WHERE stock_quantity < reorder_level
            ) AS low_stock_products,

            /* Total Customers */
            (
                SELECT COUNT(*)
                FROM customers
            ) AS total_customers,

            /* Inactive Customers */
            (
                SELECT COUNT(*)
                FROM (
                    SELECT
                        c.customer_id,
                        MAX(o.order_date) AS last_order_date
                    FROM customers c
                    JOIN orders o
                        ON c.customer_id = o.customer_id
                    WHERE o.status = 'Completed'
                    GROUP BY c.customer_id
                    HAVING DATEDIFF(
                        CURRENT_DATE,
                        MAX(o.order_date)
                    ) >= 90
                ) AS inactive
            ) AS inactive_customers,

            /* Products With Completed Sales */
            (
                SELECT COUNT(*)
                FROM (
                    SELECT
                        p.product_id
                    FROM products p
                    JOIN order_items oi
                        ON p.product_id = oi.product_id
                    JOIN orders o
                        ON oi.order_id = o.order_id
                    WHERE o.status = 'Completed'
                    GROUP BY p.product_id
                ) AS selling_products
            ) AS products_with_sales,

            /* High Volume Low Margin Products */
            (
                SELECT COUNT(*)
                FROM (
                    SELECT
                        p.product_id
                    FROM products p
                    JOIN order_items oi
                        ON p.product_id = oi.product_id
                    JOIN orders o
                        ON oi.order_id = o.order_id
                    WHERE o.status = 'Completed'
                    GROUP BY p.product_id
                    HAVING
                        SUM(oi.quantity) >= 100
                        AND
                        (
                            SUM(
                                oi.quantity *
                                (oi.unit_price - p.cost)
                            )
                            /
                            SUM(
                                oi.quantity *
                                oi.unit_price
                            )
                        ) < 0.15
                ) AS margin_risks
            ) AS low_margin_products;
    """

    result = execute_query(query)

    if not result:
        return {}

    health = result[0]

    # -----------------------------------------------------
    # Calculate meaningful percentages
    # -----------------------------------------------------

    total_products = health["total_products"]
    low_stock_products = health["low_stock_products"]

    total_customers = health["total_customers"]
    inactive_customers = health["inactive_customers"]

    products_with_sales = health["products_with_sales"]
    low_margin_products = health["low_margin_products"]

    health["low_stock_percentage"] = round(
        (low_stock_products / total_products) * 100,
        2
    ) if total_products else 0

    health["inactive_customer_percentage"] = round(
        (inactive_customers / total_customers) * 100,
        2
    ) if total_customers else 0

    health["low_margin_percentage"] = round(
        (low_margin_products / products_with_sales) * 100,
        2
    ) if products_with_sales else 0

    health["health_score"] = calculate_health_score(health)

    return health

def calculate_health_score(health):

    low_stock_pct = health["low_stock_percentage"]
    inactive_customer_pct = health["inactive_customer_percentage"]
    low_margin_pct = health["low_margin_percentage"]

    # ---------------------------------------------
    # Inventory score
    # ---------------------------------------------

    if low_stock_pct < 10:
        inventory_score = 100
    elif low_stock_pct < 20:
        inventory_score = 75
    elif low_stock_pct < 30:
        inventory_score = 50
    elif low_stock_pct < 40:
        inventory_score = 25
    else:
        inventory_score = 0

    # ---------------------------------------------
    # Customer score
    # ---------------------------------------------

    if inactive_customer_pct < 5:
        customer_score = 100
    elif inactive_customer_pct < 10:
        customer_score = 75
    elif inactive_customer_pct < 20:
        customer_score = 50
    elif inactive_customer_pct < 30:
        customer_score = 25
    else:
        customer_score = 0

    # ---------------------------------------------
    # Profitability score
    # ---------------------------------------------

    if low_margin_pct < 10:
        profitability_score = 100
    elif low_margin_pct < 20:
        profitability_score = 75
    elif low_margin_pct < 30:
        profitability_score = 50
    elif low_margin_pct < 40:
        profitability_score = 25
    else:
        profitability_score = 0

    # ---------------------------------------------
    # Overall score
    # ---------------------------------------------

    overall_score = (
        inventory_score * 0.35
        + customer_score * 0.30
        + profitability_score * 0.35
    )

    return {
        "inventory_score": inventory_score,
        "customer_score": customer_score,
        "profitability_score": profitability_score,
        "overall_score": round(overall_score, 2)
    }

def get_revenue_trends():

    query = """
        WITH monthly_sales AS (
            SELECT
                DATE_FORMAT(o.order_date, '%Y-%m') AS month,

                SUM(
                    oi.quantity * oi.unit_price
                ) AS revenue,

                COUNT(
                    DISTINCT o.order_id
                ) AS orders

            FROM orders o

            JOIN order_items oi
                ON o.order_id = oi.order_id

            WHERE o.status = 'Completed'

            GROUP BY
                DATE_FORMAT(o.order_date, '%Y-%m')
        ),

        monthly_comparison AS (
            SELECT
                month,
                revenue,
                orders,

                LAG(revenue) OVER (
                    ORDER BY month
                ) AS previous_month_revenue,

                LAG(orders) OVER (
                    ORDER BY month
                ) AS previous_month_orders

            FROM monthly_sales
        )

        SELECT
            month,
            revenue,
            orders,
            previous_month_revenue,
            previous_month_orders,

            ROUND(
                revenue - previous_month_revenue,
                2
            ) AS revenue_change,

            ROUND(
                (
                    revenue - previous_month_revenue
                )
                / NULLIF(previous_month_revenue, 0)
                * 100,
                2
            ) AS growth_percentage,

            CASE
                WHEN previous_month_revenue IS NULL
                    THEN 'BASELINE'

                WHEN revenue > previous_month_revenue
                    THEN 'GROWING'

                WHEN revenue < previous_month_revenue
                    THEN 'DECLINING'

                ELSE 'STABLE'
            END AS trend

        FROM monthly_comparison

        ORDER BY month;
    """

    return execute_query(query)

def get_revenue_anomalies():

    query = """
        WITH monthly_sales AS (
            SELECT
                DATE_FORMAT(
                    o.order_date,
                    '%Y-%m'
                ) AS month,

                SUM(
                    oi.quantity * oi.unit_price
                ) AS revenue

            FROM orders o

            JOIN order_items oi
                ON o.order_id = oi.order_id

            WHERE o.status = 'Completed'

            GROUP BY
                DATE_FORMAT(
                    o.order_date,
                    '%Y-%m'
                )
        ),

        statistics AS (
            SELECT
                AVG(revenue) AS average_revenue,
                STDDEV_POP(revenue) AS revenue_stddev
            FROM monthly_sales
        )

        SELECT
            m.month,
            m.revenue,

            ROUND(
                s.average_revenue,
                2
            ) AS average_revenue,

            ROUND(
                s.revenue_stddev,
                2
            ) AS revenue_stddev,

            ROUND(
                (
                    m.revenue - s.average_revenue
                ) / NULLIF(s.revenue_stddev, 0),
                2
            ) AS z_score,

            CASE

                WHEN ABS(
                    (
                        m.revenue - s.average_revenue
                    ) / NULLIF(s.revenue_stddev, 0)
                ) >= 2

                THEN 'ANOMALY'

                WHEN ABS(
                    (
                        m.revenue - s.average_revenue
                    ) / NULLIF(s.revenue_stddev, 0)
                ) >= 1

                THEN 'UNUSUAL'

                ELSE 'NORMAL'

            END AS anomaly_level,

            CASE

                WHEN m.revenue > s.average_revenue
                    THEN 'POSITIVE'

                WHEN m.revenue < s.average_revenue
                    THEN 'NEGATIVE'

                ELSE 'NEUTRAL'

            END AS anomaly_direction

        FROM monthly_sales m

        CROSS JOIN statistics s

        ORDER BY
            ABS(
                (
                    m.revenue - s.average_revenue
                ) / NULLIF(s.revenue_stddev, 0)
            ) DESC;
    """

    return execute_query(query)

def get_executive_insights():

    health = get_business_health()
    trends = get_revenue_trends()
    anomalies = get_revenue_anomalies()

    reorder_priorities = get_reorder_priorities(10)
    profitability_gaps = get_sales_profitability_gaps(10)
    cross_domain_risks = get_cross_domain_risks(10)
    
    month_status = get_current_month_status()
    mtd_trend = get_month_to_date_trend()
    
    latest_trend = None

    if month_status["is_partial_month"]:
        latest_trend = mtd_trend
    else:
        if trends:
            latest_trend = trends[-1]

    # -------------------------------------------------
    # Revenue trend
    # -------------------------------------------------

    latest_trend = None

    if month_status["is_partial_month"]:
        latest_trend = mtd_trend
    else:
        if trends:
            latest_trend = trends[-1]

    # -------------------------------------------------
    # Revenue anomaly
    # -------------------------------------------------

    significant_anomalies = []

    for anomaly in anomalies:

        if anomaly.get("anomaly_level") in (
            "ANOMALY",
            "UNUSUAL"
        ):
            significant_anomalies.append(anomaly)

    # -------------------------------------------------
    # Build prioritized alerts
    # -------------------------------------------------

    alerts = []

    # Inventory alert
    if health["low_stock_percentage"] >= 20:

        alerts.append({
            "priority": "HIGH",
            "category": "INVENTORY",
            "message": (
                f"{health['low_stock_products']} products "
                f"({health['low_stock_percentage']}%) are "
                "below their reorder level."
            )
        })

    elif health["low_stock_percentage"] >= 10:

        alerts.append({
            "priority": "MEDIUM",
            "category": "INVENTORY",
            "message": (
                f"{health['low_stock_products']} products "
                f"({health['low_stock_percentage']}%) are "
                "below their reorder level."
            )
        })

    # Profitability alert
    if health["low_margin_percentage"] >= 20:

        alerts.append({
            "priority": "HIGH",
            "category": "PROFITABILITY",
            "message": (
                f"{health['low_margin_products']} products "
                f"({health['low_margin_percentage']}%) have "
                "high sales volume but profit margins below 15%."
            )
        })

    elif health["low_margin_percentage"] >= 10:

        alerts.append({
            "priority": "MEDIUM",
            "category": "PROFITABILITY",
            "message": (
                f"{health['low_margin_products']} products "
                f"({health['low_margin_percentage']}%) have "
                "high sales volume but profit margins below 15%."
            )
        })
    # Cross-domain risk alert

    critical_cross_domain = [
        item
        for item in cross_domain_risks
        if item["risk_level"] == "CRITICAL"
    ]

    high_cross_domain = [
        item
        for item in cross_domain_risks
        if item["risk_level"] == "HIGH"
    ]

    if critical_cross_domain:

        alerts.append({
            "priority": "HIGH",
            "category": "CROSS_DOMAIN",
            "message": (
                f"{len(critical_cross_domain)} products have "
                "critical combined inventory and demand risks."
            )
    })

    elif high_cross_domain:

        alerts.append({
        "priority": "MEDIUM",
        "category": "CROSS_DOMAIN",
        "message": (
            f"{len(high_cross_domain)} products have "
            "significant combined inventory and demand risks."
        )
    })

    # Customer alert
    if health["inactive_customer_percentage"] >= 20:

        alerts.append({
            "priority": "HIGH",
            "category": "CUSTOMERS",
            "message": (
                f"{health['inactive_customers']} customers "
                f"({health['inactive_customer_percentage']}%) "
                "meet the current inactivity-risk threshold."
            )
        })

    elif health["inactive_customer_percentage"] >= 5:

        alerts.append({
            "priority": "MEDIUM",
            "category": "CUSTOMERS",
            "message": (
                f"{health['inactive_customers']} customers "
                f"({health['inactive_customer_percentage']}%) "
                "meet the current inactivity-risk threshold."
            )
        })

    # Revenue anomaly alert
    if significant_anomalies:

        alerts.append({
            "priority": "MEDIUM",
            "category": "REVENUE",
            "message": (
    f"{len(significant_anomalies)} historical month(s) show "
    "unusual revenue behavior based on the statistical "
    "anomaly model."
)
        })

    # -------------------------------------------------
    # Sort alerts
    # -------------------------------------------------

    priority_order = {
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    alerts.sort(
        key=lambda x: priority_order[x["priority"]]
    )

    # -------------------------------------------------
    # Final result
    # -------------------------------------------------

    return {
    "health": health,
    "month_status": month_status,
    "revenue_trend": latest_trend,
    "significant_revenue_anomalies": significant_anomalies,
    "priority_alerts": alerts,
    "reorder_priorities": reorder_priorities,
    "profitability_gaps": profitability_gaps,
    "cross_domain_risks": cross_domain_risks
}

def get_current_month_status():

    query = """
        SELECT
            DATE_FORMAT(CURRENT_DATE, '%Y-%m') AS current_month,
            DAY(CURRENT_DATE) AS current_day,
            DAY(
                LAST_DAY(CURRENT_DATE)
            ) AS days_in_month
    """

    result = execute_query(query)

    if not result:
        return {}

    data = result[0]

    data["is_partial_month"] = (
        data["current_day"] < data["days_in_month"]
    )

    return data

def get_month_to_date_trend():

    query = """
        SELECT

            /* Current month revenue */
            (
                SELECT COALESCE(
                    SUM(oi.quantity * oi.unit_price),
                    0
                )
                FROM orders o
                JOIN order_items oi
                    ON o.order_id = oi.order_id
                WHERE o.status = 'Completed'
                AND YEAR(o.order_date) = YEAR(CURRENT_DATE)
                AND MONTH(o.order_date) = MONTH(CURRENT_DATE)
                AND DAY(o.order_date) <= DAY(CURRENT_DATE)
            ) AS current_mtd_revenue,

            /* Previous month same-period revenue */
            (
                SELECT COALESCE(
                    SUM(oi.quantity * oi.unit_price),
                    0
                )
                FROM orders o
                JOIN order_items oi
                    ON o.order_id = oi.order_id
                WHERE o.status = 'Completed'
                AND DATE(o.order_date) >=
                    DATE_FORMAT(
                        DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH),
                        '%Y-%m-01'
                    )
                AND DATE(o.order_date) <=
                    DATE_ADD(
                        DATE_FORMAT(
                            DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH),
                            '%Y-%m-01'
                        ),
                        INTERVAL DAY(CURRENT_DATE) - 1 DAY
                    )
            ) AS previous_mtd_revenue;
    """

    result = execute_query(query)

    if not result:
        return {}

    data = result[0]

    current = float(data["current_mtd_revenue"] or 0)
    previous = float(data["previous_mtd_revenue"] or 0)

    if previous == 0:
        growth = None
    else:
        growth = round(
            ((current - previous) / previous) * 100,
            2
        )

    if growth is None:
        trend = "INSUFFICIENT_DATA"
    elif growth > 0:
        trend = "GROWING"
    elif growth < 0:
        trend = "DECLINING"
    else:
        trend = "STABLE"

    data["growth_percentage"] = growth
    data["trend"] = trend
    data["comparison_type"] = "MONTH_TO_DATE"

    return data

def get_cross_domain_risks(limit=20):

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,

            i.stock_quantity,
            i.reorder_level,

            SUM(oi.quantity) AS units_sold,

            ROUND(
                SUM(oi.quantity) / 30,
                2
            ) AS estimated_daily_sales,

            ROUND(
                i.stock_quantity /
                NULLIF(SUM(oi.quantity) / 30, 0),
                2
            ) AS estimated_days_of_stock,

            SUM(
                oi.quantity * oi.unit_price
            ) AS revenue,

            SUM(
                oi.quantity *
                (oi.unit_price - p.cost)
            ) AS profit,

            ROUND(
                SUM(
                    oi.quantity *
                    (oi.unit_price - p.cost)
                )
                /
                NULLIF(
                    SUM(
                        oi.quantity * oi.unit_price
                    ),
                    0
                )
                * 100,
                2
            ) AS profit_margin,

            CASE

    /* -----------------------------------------
       CRITICAL
       ----------------------------------------- */

    WHEN
        i.stock_quantity = 0
        AND SUM(oi.quantity) >= 300
        THEN 'CRITICAL'

    WHEN
        (
            i.stock_quantity /
            NULLIF(SUM(oi.quantity) / 30, 0)
        ) < 1
        AND SUM(oi.quantity) >= 300
        AND
        (
            SUM(
                oi.quantity *
                (oi.unit_price - p.cost)
            )
            /
            NULLIF(
                SUM(
                    oi.quantity * oi.unit_price
                ),
                0
            )
        ) < 0.15
        THEN 'CRITICAL'


 

    WHEN
        (
            i.stock_quantity /
            NULLIF(SUM(oi.quantity) / 30, 0)
        ) < 1
        AND SUM(oi.quantity) >= 300
        THEN 'HIGH'

    WHEN
        i.stock_quantity < i.reorder_level
        AND
        (
            SUM(
                oi.quantity *
                (oi.unit_price - p.cost)
            )
            /
            NULLIF(
                SUM(
                    oi.quantity * oi.unit_price
                ),
                0
            )
        ) < 0.15
        THEN 'HIGH'



    WHEN
        i.stock_quantity < i.reorder_level
        THEN 'MEDIUM'



    ELSE 'LOW'

END AS risk_level

        FROM products p

        JOIN inventory i
            ON p.product_id = i.product_id

        JOIN order_items oi
            ON p.product_id = oi.product_id

        JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.status = 'Completed'

        GROUP BY
            p.product_id,
            p.product_name,
            p.category,
            i.stock_quantity,
            i.reorder_level

        HAVING
            i.stock_quantity < i.reorder_level

        ORDER BY
            CASE risk_level
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                ELSE 4
            END,

            estimated_days_of_stock ASC

        LIMIT %s
    """

    return execute_query(query, (limit,))




if __name__ == "__main__":

    print("\nTOTAL REVENUE:")
    print(get_total_revenue())

    print("\nTOP PRODUCTS:")
    print(get_top_products())

    print("\nTOP CUSTOMERS:")
    print(get_top_customers())

    print("\nMONTHLY SALES:")
    print(get_monthly_sales())

    print("\nINVENTORY RISKS:")
    print(get_inventory_risks())

    print("\nCUSTOMER ACTIVITY:")
    print(get_customer_activity())

    print("\nPRODUCT PROFITABILITY:")
    print(get_product_profitability())

    print("\nSUPPLIER PERFORMANCE:")
    print(get_supplier_performance())

    print("\nREORDER PRIORITIES:")
    print(get_reorder_priorities())

    print("\nCUSTOMER RISK:")
    print(get_customer_risk())

    print("\nSALES PROFITABILITY GAPS:")
    print(get_sales_profitability_gaps())

    print("\nBUSINESS HEALTH:")
    print(get_business_health())

    print("\nREVENUE TRENDS:")
    print(get_revenue_trends())

    print("\nREVENUE ANOMALIES:")
    print(get_revenue_anomalies())

    print("\nEXECUTIVE INSIGHTS:")
    print(get_executive_insights())

    print("\nCROSS DOMAIN RISKS:")
    print(get_cross_domain_risks())

