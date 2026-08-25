import streamlit as st

from agent import (
    ask_agent,
    execute_tool,
    generate_recommendations
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ERP AI Command Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "conversation" not in st.session_state:

    st.session_state.conversation = []


if "memory" not in st.session_state:

    st.session_state.memory = {
        "last_products": [],
        "last_customers": [],
        "last_tool": None,
        "last_topic": None,
        "last_period": None
    }


if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* Metric styling */

    div[data-testid="stMetric"] {

        background: rgba(255, 255, 255, 0.03);

        border: 1px solid rgba(255, 255, 255, 0.08);

        padding: 18px;

        border-radius: 12px;

    }


    /* Section spacing */

    .section-title {

        font-size: 1.35rem;

        font-weight: 700;

        margin-top: 1rem;

        margin-bottom: 1rem;

    }


    /* Risk cards */

    .risk-card {

        background: rgba(255, 70, 70, 0.08);

        border-left: 4px solid #ff4b4b;

        padding: 15px;

        border-radius: 8px;

        margin-bottom: 10px;

    }


    .high-risk-card {

        background: rgba(255, 165, 0, 0.08);

        border-left: 4px solid #ffa500;

        padding: 15px;

        border-radius: 8px;

        margin-bottom: 10px;

    }


    /* Recommendation cards */

    .recommendation-card {

        background: rgba(50, 120, 255, 0.08);

        border-left: 4px solid #3278ff;

        padding: 15px;

        border-radius: 8px;

        margin-bottom: 10px;

    }


    /* Sidebar */

    section[data-testid="stSidebar"] {

        border-right: 1px solid rgba(255, 255, 255, 0.08);

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_float(value):

    try:

        return float(value)

    except:

        return None


def format_currency(value):

    try:

        return f"₹{float(value):,.2f}"

    except:

        return str(value)


def format_number(value):

    try:

        return f"{int(value):,}"

    except:

        return str(value)


def format_decimal(value, decimals=2):

    try:

        return f"{float(value):.{decimals}f}"

    except:

        return str(value)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 ERP AI")

    st.caption(
        "Command Center"
    )

    st.divider()

    st.subheader("Navigation")

    st.write("📊 Executive Dashboard")

    st.write("💰 Revenue")

    st.write("📦 Inventory")

    st.write("📈 Profitability")

    st.write("⚠️ Business Risks")

    st.write("🎯 Recommendations")

    st.write("🤖 AI Agent")

    st.divider()

    st.subheader("System Status")

    st.success(
        "ERP Agent Online"
    )

    st.info(
        "15 business tools registered"
    )

    st.divider()

    st.caption(
        "PostgreSQL • OpenAI • ERP Analytics"
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 ERP AI Command Center"
)

st.caption(
    "AI-powered ERP analytics, business intelligence "
    "and decision support"
)


# ============================================================
# LOAD EXECUTIVE DATA
# ============================================================

with st.spinner(
    "Loading ERP analytics..."
):

    executive_result = execute_tool(
        "get_executive_insights",
        {}
    )


# ============================================================
# VALIDATE EXECUTIVE DATA
# ============================================================
# ============================================================
# VALIDATE EXECUTIVE DATA
# ============================================================

# ============================================================
# VALIDATE EXECUTIVE DATA
# ============================================================

if (
    not isinstance(executive_result, dict)
    or executive_result.get("error")
):

    st.error("Unable to load executive ERP data.")

    st.subheader("Debug Information")

    st.code(
        str(executive_result),
        language="text"
    )

    st.stop()

# ============================================================
# EXTRACT HEALTH DATA
# ============================================================

# ============================================================
# EXTRACT EXECUTIVE DATA
# ============================================================

executive_data = executive_result.get(
    "data",
    {}
)

# ============================================================
# EXTRACT HEALTH DATA
# ============================================================

health = executive_data.get(
    "health",
    {}
)

health_score_data = health.get(
    "health_score",
    {}
)


overall_health = health_score_data.get(
    "overall_score",
    "N/A"
)


inventory_score = health_score_data.get(
    "inventory_score",
    "N/A"
)


customer_score = health_score_data.get(
    "customer_score",
    "N/A"
)


profitability_score = health_score_data.get(
    "profitability_score",
    "N/A"
)


total_revenue = health.get(
    "total_revenue",
    "N/A"
)


completed_orders = health.get(
    "completed_orders",
    "N/A"
)


total_products = health.get(
    "total_products",
    "N/A"
)


low_stock_products = health.get(
    "low_stock_products",
    "N/A"
)


total_customers = health.get(
    "total_customers",
    "N/A"
)


inactive_customers = health.get(
    "inactive_customers",
    "N/A"
)


products_with_sales = health.get(
    "products_with_sales",
    "N/A"
)


low_margin_products = health.get(
    "low_margin_products",
    "N/A"
)


low_stock_percentage = health.get(
    "low_stock_percentage",
    "N/A"
)


low_margin_percentage = health.get(
    "low_margin_percentage",
    "N/A"
)


# ============================================================
# REVENUE TREND
# ============================================================

revenue_trend = executive_data.get(
    "revenue_trend",
    {}
)


current_mtd_revenue = revenue_trend.get(
    "current_mtd_revenue",
    "N/A"
)


previous_mtd_revenue = revenue_trend.get(
    "previous_mtd_revenue",
    "N/A"
)


growth_percentage = revenue_trend.get(
    "growth_percentage",
    "N/A"
)


trend = revenue_trend.get(
    "trend",
    "N/A"
)


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

st.divider()

st.header(
    "📊 Executive Dashboard"
)


# ============================================================
# PRIMARY METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Business Health",
        f"{overall_health}/100"
    )


with col2:

    st.metric(
        "Total Revenue",
        format_currency(
            total_revenue
        )
    )


with col3:

    st.metric(
        "Completed Orders",
        format_number(
            completed_orders
        )
    )


with col4:

    st.metric(
        "Products",
        format_number(
            total_products
        )
    )


# ============================================================
# SECONDARY METRICS
# ============================================================

col5, col6, col7, col8 = st.columns(4)


with col5:

    st.metric(
        "Low Stock",
        format_number(
            low_stock_products
        )
    )


with col6:

    st.metric(
        "Low Margin",
        format_number(
            low_margin_products
        )
    )


with col7:

    st.metric(
        "Customers",
        format_number(
            total_customers
        )
    )


with col8:

    st.metric(
        "Inactive Customers",
        format_number(
            inactive_customers
        )
    )


# ============================================================
# REVENUE OVERVIEW
# ============================================================

st.divider()

st.header(
    "💰 Revenue Overview"
)


revenue_col1, revenue_col2, revenue_col3 = st.columns(3)


with revenue_col1:

    st.metric(
        "Total Revenue",
        format_currency(
            total_revenue
        )
    )


with revenue_col2:

    st.metric(
        "August MTD Revenue",
        format_currency(
            current_mtd_revenue
        )
    )


with revenue_col3:

    st.metric(
        "MTD Growth",
        f"{growth_percentage}%"
    )


if str(trend).upper() == "DECLINING":

    st.warning(
        f"Revenue is currently **declining** "
        f"by {abs(float(growth_percentage)):.2f}% "
        f"versus the equivalent previous period."
    )

elif str(trend).upper() == "GROWING":

    st.success(
        f"Revenue is currently growing by "
        f"{float(growth_percentage):.2f}%."
    )

else:

    st.info(
        f"Current revenue trend: {trend}"
    )


# ============================================================
# BUSINESS HEALTH SCORES
# ============================================================

st.divider()

st.header(
    "❤️ Business Health"
)


health_col1, health_col2, health_col3, health_col4 = (
    st.columns(4)
)


with health_col1:

    st.metric(
        "Overall",
        f"{overall_health}/100"
    )


with health_col2:

    st.metric(
        "Inventory",
        f"{inventory_score}/100"
    )


with health_col3:

    st.metric(
        "Customers",
        f"{customer_score}/100"
    )


with health_col4:

    st.metric(
        "Profitability",
        f"{profitability_score}/100"
    )


# ============================================================
# INVENTORY AND RISKS
# ============================================================

st.divider()

inventory_col, risk_col = st.columns(2)


# ============================================================
# CRITICAL INVENTORY RISKS
# ============================================================

with inventory_col:

    st.header(
        "🚨 Critical Inventory Risks"
    )

    cross_domain_risks = executive_data.get(
    "cross_domain_risks",
    []
)


    if cross_domain_risks:

        for risk in cross_domain_risks[:7]:

            product_name = risk.get(
                "product_name",
                "Unknown Product"
            )

            stock = risk.get(
                "stock_quantity",
                "N/A"
            )

            reorder_level = risk.get(
                "reorder_level",
                "N/A"
            )

            days = risk.get(
                "estimated_days_of_stock",
                "N/A"
            )

            daily_sales = risk.get(
                "estimated_daily_sales",
                "N/A"
            )

            margin = risk.get(
                "profit_margin",
                "N/A"
            )

            risk_level = risk.get(
                "risk_level",
                "UNKNOWN"
            )


            if str(risk_level).upper() == "CRITICAL":

                st.markdown(
                    f"""
                    <div class="risk-card">

                    <strong>{product_name}</strong>

                    <br><br>

                    🔴 Risk: <strong>{risk_level}</strong>

                    <br>

                    Stock: {stock} units

                    <br>

                    Reorder level: {reorder_level} units

                    <br>

                    Stock coverage: {days} days

                    <br>

                    Daily sales: {daily_sales}

                    <br>

                    Profit margin: {margin}%

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="high-risk-card">

                    <strong>{product_name}</strong>

                    <br><br>

                    🟠 Risk: <strong>{risk_level}</strong>

                    <br>

                    Stock: {stock} units

                    <br>

                    Stock coverage: {days} days

                    <br>

                    Profit margin: {margin}%

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.success(
            "No critical inventory risks detected."
        )


# ============================================================
# PRIORITY ALERTS
# ============================================================

with risk_col:

    st.header(
        "⚠️ Priority Alerts"
    )

    alerts = executive_data.get(
    "priority_alerts",
    []
)


    if alerts:

        for alert in alerts:

            priority = alert.get(
                "priority",
                "UNKNOWN"
            )

            category = alert.get(
                "category",
                "GENERAL"
            )

            message = alert.get(
                "message",
                ""
            )


            if priority == "HIGH":

                st.error(
                    f"**{priority} | {category}**\n\n"
                    f"{message}"
                )

            elif priority == "MEDIUM":

                st.warning(
                    f"**{priority} | {category}**\n\n"
                    f"{message}"
                )

            else:

                st.info(
                    f"**{priority} | {category}**\n\n"
                    f"{message}"
                )

    else:

        st.success(
            "No priority alerts."
        )


# ============================================================
# REORDER PRIORITIES
# ============================================================

st.divider()

st.header(
    "📦 Reorder Priorities"
)


reorder_priorities = executive_data.get(
    "reorder_priorities",
    []
)


if reorder_priorities:

    reorder_rows = []


    for index, product in enumerate(
        reorder_priorities,
        start=1
    ):

        reorder_rows.append({

            "Priority":
                index,

            "Product":
                product.get(
                    "product_name",
                    "Unknown"
                ),

            "Category":
                product.get(
                    "category",
                    "N/A"
                ),

            "Stock":
                product.get(
                    "stock_quantity",
                    "N/A"
                ),

            "Reorder Level":
                product.get(
                    "reorder_level",
                    "N/A"
                ),

            "Daily Sales":
                format_decimal(
                    product.get(
                        "estimated_daily_sales",
                        "N/A"
                    )
                ),

            "Stock Coverage (Days)":
                format_decimal(
                    product.get(
                        "estimated_days_of_stock",
                        "N/A"
                    )
                )

        })


    st.dataframe(
        reorder_rows,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No reorder priorities available."
    )


# ============================================================
# PROFITABILITY
# ============================================================

st.divider()

st.header(
    "📈 Profitability Risks"
)


profitability_gaps = executive_data.get(
    "profitability_gaps",
    []
)


if profitability_gaps:

    profitability_rows = []


    for product in profitability_gaps:

        profitability_rows.append({

            "Product":
                product.get(
                    "product_name",
                    "Unknown"
                ),

            "Category":
                product.get(
                    "category",
                    "N/A"
                ),

            "Units Sold":
                product.get(
                    "units_sold",
                    "N/A"
                ),

            "Revenue":
                format_currency(
                    product.get(
                        "revenue",
                        "N/A"
                    )
                ),

            "Profit":
                format_currency(
                    product.get(
                        "profit",
                        "N/A"
                    )
                ),

            "Profit Margin":
                f"{format_decimal(product.get('profit_margin', 'N/A'))}%"

        })


    st.dataframe(
        profitability_rows,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No profitability gaps available."
    )


# ============================================================
# AI RECOMMENDATIONS
# ============================================================

st.divider()

st.header(
    "🎯 AI Recommendations"
)


recommendations = generate_recommendations(
    executive_result
)


if recommendations:

    recommendation_col1, recommendation_col2 = (
        st.columns(2)
    )


    for index, recommendation in enumerate(
        recommendations[:10]
    ):

        priority = recommendation.get(
            "priority",
            "GENERAL"
        )

        category = recommendation.get(
            "category",
            "BUSINESS"
        )

        product = recommendation.get(
            "product",
            "Business"
        )

        action = recommendation.get(
            "action",
            ""
        )


        target_column = (
            recommendation_col1
            if index % 2 == 0
            else recommendation_col2
        )


        with target_column:

            st.markdown(
                f"""
                <div class="recommendation-card">

                <strong>
                {priority} | {category}
                </strong>

                <br><br>

                <strong>
                {product}
                </strong>

                <br>

                {action}

                </div>
                """,
                unsafe_allow_html=True
            )

else:

    st.info(
        "No recommendations available."
    )


# ============================================================
# AI AGENT CHAT
# ============================================================

st.divider()

st.header(
    "🤖 Ask Your ERP Agent"
)


st.caption(
    "Ask questions about revenue, inventory, "
    "profitability, customers, sales and business risks."
)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask your ERP Agent..."
)


if question:

    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------

    st.session_state.messages.append({

        "role":
            "user",

        "content":
            question

    })


    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    # --------------------------------------------------------
    # Ask AI Agent
    # --------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Analyzing ERP data..."
        ):

            try:

                answer = ask_agent(

                    question,

                    conversation=(
                        st.session_state.conversation
                    ),

                    memory=(
                        st.session_state.memory
                    )

                )

            except Exception as e:

                answer = (

                    "An error occurred while "
                    "processing your request.\n\n"

                    f"`{str(e)}`"

                )


        st.markdown(
            answer
        )


    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append({

        "role":
            "assistant",

        "content":
            answer

    })


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ERP AI Agent • 15 Business Tools • "
    "PostgreSQL • OpenAI • AI-Powered Decision Support"
)