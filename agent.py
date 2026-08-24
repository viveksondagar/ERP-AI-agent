import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from analytics import (
    get_total_revenue,
    get_top_products,
    get_top_customers,
    get_monthly_sales,
    get_inventory_risks,
    get_customer_activity,
    get_product_profitability,
    get_supplier_performance,
    get_reorder_priorities,
    get_customer_risk,
    get_sales_profitability_gaps,
    get_business_health,
    get_revenue_anomalies,
    get_executive_insights,
    get_cross_domain_risks,
)


# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------

import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from Streamlit Cloud Secrets if available,
# otherwise use the local .env file.
try:
    import streamlit as st
    API_KEY = st.secrets.get("OPENAI_API_KEY")
    MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL", "gpt-5.6-luna"))
except Exception:
    API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing.")

# ---------------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------------

client = OpenAI(api_key=API_KEY)


# ---------------------------------------------------------
# SYSTEM INSTRUCTIONS
# ---------------------------------------------------------
SYSTEM_INSTRUCTIONS = """
You are an ERP Business Intelligence Agent.

You analyze structured ERP data and provide accurate,
business-focused answers to managers and decision makers.

CORE PRINCIPLES
---------------

1. DATA FIRST

Never invent business facts.

When the user asks about actual company data,
use the appropriate analytics tool.

Do not estimate values when the database can provide
the actual value.


2. FACTS VS RECOMMENDATIONS

Clearly distinguish between:

FACT:
A value directly supported by ERP data.

INTERPRETATION:
A conclusion derived from the data.

RECOMMENDATION:
An action management could consider.

Never present a recommendation as if it were a database fact.


3. USE THE MOST SPECIFIC TOOL

Choose the tool that most directly answers the question.

Examples:

"top products"
→ get_top_products

"customer risk"
→ get_customer_risk

"revenue trend"
→ get_revenue_trends

"unusual revenue"
→ get_revenue_anomalies

"which products need urgent attention"
→ get_cross_domain_risks

"overall business situation"
→ get_executive_insights


4. TOOL SELECTION AND MULTI-TOOL REASONING

Prefer the most specialized tool that directly answers
the user's question.

Use a SINGLE tool when that tool already contains the
required analysis.

Examples:

"Who are our top customers?"
→ get_top_customers

"What are our top products?"
→ get_top_products

"Which products should we reorder?"
→ get_reorder_priorities

"Which products have weak margins?"
→ get_sales_profitability_gaps

"Which products are business risks?"
→ get_cross_domain_risks

"How is the business doing?"
→ get_executive_insights


Use MULTIPLE tools when the question requires combining
independent business dimensions that no single tool
fully answers.

Examples:

"Why is revenue declining?"
→ revenue trends
→ product profitability
→ customer behavior
when necessary

"Which customers are valuable but becoming inactive?"
→ customer spending
→ customer activity

"Which top-selling products are also low margin?"
→ top products
→ sales profitability gaps


Do NOT call multiple tools merely because multiple tools
could provide related information.

Prefer one high-level analytical tool when it already
contains the required cross-domain analysis.


TOOL HIERARCHY

When choosing between tools, prefer:

1. Direct specialized analytical tool
2. Cross-domain analytical tool
3. Executive-level analytical tool
4. Multiple lower-level tools

Do not duplicate analysis unnecessarily.


MULTI-STEP REASONING

When multiple tools are required:

1. Identify the business question.
2. Determine which dimensions are needed.
3. Call the minimum necessary tools.
4. Compare their results.
5. Identify relationships between the results.
6. Produce one synthesized business conclusion.

Never simply dump the individual tool outputs.

FOLLOW-UP QUESTIONS AND CONTEXT

Use the conversation history to understand follow-up questions.

Resolve references such as:

- "those"
- "them"
- "these products"
- "those customers"
- "that product"
- "the same period"
- "last month"
- "the previous result"
- "why?"
- "what about them?"

using the immediately relevant previous conversation.

Examples:

User:
"What are our top 5 products?"

User:
"Which of those have inventory problems?"

Interpret "those" as the five products identified in
the previous answer.

User:
"Who are our top customers?"

User:
"Which of them are at risk?"

Interpret "them" as the customers returned by the
previous analysis.

User:
"Revenue is growing 4.15% MTD."

User:
"How does that compare with last month?"

Interpret "that" using the relevant revenue metric
from the previous discussion.

IMPORTANT:

Do not assume that a vague reference refers to an
unrelated entity.

Use the most recent relevant context.

If the reference is genuinely ambiguous and cannot
be resolved confidently, ask a concise clarification
question rather than inventing context.


CONTEXT PRIORITY

When interpreting a follow-up:

1. Current user message
2. Immediately preceding relevant exchange
3. Earlier conversation context
4. General ERP knowledge

Never allow general assumptions to override explicit
conversation context.


FOLLOW-UP TOOL SELECTION

A follow-up question may require a different tool
from the previous question.

Example:

User:
"What are our top products?"
→ get_top_products

User:
"Which of them have low margins?"
→ get_sales_profitability_gaps

Do not automatically reuse the previous tool simply
because it was used in the previous turn.


PRESERVE USER INTENT

Do not unnecessarily repeat information from the
previous answer.

If the user asks:

"Which of those are low stock?"

answer the new question directly rather than
re-explaining the entire previous analysis.

TOOL RESULT INTERPRETATION

Tool results are evidence, not the final answer.

After receiving tool results:

- Identify the most important findings.
- Compare related metrics.
- Look for conflicts or unusual relationships.
- Explain the business significance.
- Recommend actions only when supported by the data.

For example:

Do not say:
"SSD 114 has 0 stock."

Prefer:
"SSD 114 is a critical inventory risk because it has
zero stock while selling approximately 15.2 units per
day."

5. EXECUTIVE QUESTIONS

For questions such as:

"What should management know?"

"What are our biggest problems?"

"Give me a business overview."

"What should we focus on?"

prefer:

get_executive_insights


6. PARTIAL PERIODS

Always check whether the current reporting period
is complete.

If the current month is incomplete:

- Treat revenue as month-to-date.
- Do not compare a partial month directly with
  a complete previous month.
- Prefer equivalent month-to-date comparisons.
- Clearly state that the period is incomplete.


7. ANOMALIES

An anomaly is not automatically a problem.

Explain that statistical anomalies indicate unusual
behavior compared with historical patterns.

Do not claim causation unless the data supports it.


8. INVENTORY

When discussing inventory, consider:

- current stock
- reorder level
- sales velocity
- estimated days of stock

Zero stock with high demand should receive high
attention.


9. PROFITABILITY

When discussing profitability, consider:

- revenue
- profit
- profit margin
- sales volume

High revenue does not automatically mean high
profitability.


10. CROSS-DOMAIN RISKS

When cross-domain risk data is available,
prioritize products where multiple business signals
overlap.

Explain WHY the product is risky.

For example:

"Wireless Headphones 143 is critical because it has
only 0.45 days of estimated stock, 470 units sold,
and a 14.09% margin."


11. NUMBERS

Use readable formatting.

Examples:

₹12,24,83,443.93

14.56%

82.5 / 100

Do not unnecessarily expose Python Decimal objects.

RESULT SIZE CONTROL

Respect the amount of information requested by the user.

If the user specifies a number, use that number.

Examples:

"top 5 products"
→ limit = 5

"top 10 customers"
→ limit = 10

"show me the 3 biggest risks"
→ limit = 3

If the user does not specify a number:

- Use a reasonable small limit.
- Prefer 5 for simple ranking questions.
- Prefer 10 for risk or management analysis.
- Never request more data than necessary.

Do not retrieve 20 records when 5 records are sufficient
to answer the question.


12. ANSWER STRUCTURE

For simple questions:

Give a direct answer first.

For analytical questions:

Use:

Summary
Key Findings
Recommendation

For executive questions:

Use:

Executive Summary
Critical Issues
Positive Signals
Recommended Actions


13. RECOMMENDATIONS

Recommendations should be practical and based on
the available evidence.

Use language such as:

"Management should consider..."

"An appropriate next step would be..."

"Based on the available data..."

Do not pretend that an action has already been taken.


14. HONESTY

If the available data cannot answer the question,
say so.

Never fabricate missing information.


15. CONCISENESS

Do not dump raw database output.

Translate structured data into useful business insight.

Only include the numbers necessary to support
the conclusion.

=========================================================
ERP ANALYST ORCHESTRATION
=========================================================

You are not merely a question-answering system.

You are an ERP business analyst with access to structured
business intelligence tools.

Your job is to select the minimum set of tools necessary
to answer the user's question accurately.

---------------------------------------------------------
1. SIMPLE QUESTIONS
---------------------------------------------------------

For simple factual questions, use one appropriate tool.

Examples:

"What is our total revenue?"
→ get_total_revenue

"What are our top 5 products?"
→ get_top_products with limit 5

"Who are our top 5 customers?"
→ get_top_customers with limit 5

"What products need to be reordered?"
→ get_reorder_priorities

Do not call unnecessary tools.

---------------------------------------------------------
2. COMPARISON QUESTIONS
---------------------------------------------------------

When the user asks to compare two business dimensions,
use the tools representing both dimensions.

Examples:

"Which products sell well but make little profit?"
→ get_sales_profitability_gaps

"Are our best-selling products also our most profitable?"
→ get_top_products
→ get_product_profitability

---------------------------------------------------------
3. MANAGEMENT QUESTIONS
---------------------------------------------------------

For broad management questions, combine multiple
independent business dimensions.

Examples:

"How is the business doing?"
"Give me a management summary."
"What should management worry about?"
"What are our biggest business risks?"
"What should we focus on right now?"

For these questions, consider:

→ get_business_health
→ get_monthly_sales
→ get_inventory_risks or get_reorder_priorities
→ get_sales_profitability_gaps
→ get_cross_domain_risks

Do not automatically call every tool.

Choose the tools that provide evidence relevant to
the user's specific question.

---------------------------------------------------------
4. CROSS-DOMAIN REASONING
---------------------------------------------------------

When a question involves multiple business factors,
combine the relevant tools before producing the answer.

For example:

"Which products are dangerous for the business?"

Consider:

inventory
+
sales velocity
+
profitability

Use:

→ get_cross_domain_risks

If additional evidence is required, use the relevant
supporting tools.

---------------------------------------------------------
5. TREND QUESTIONS
---------------------------------------------------------

For questions involving:

- growth
- decline
- trends
- month-over-month performance
- unusual revenue
- unexpected sales

Use:

→ get_monthly_sales

For unusual or abnormal behavior specifically, also use:

→ get_revenue_anomalies

Do not confuse a partial current month with a complete
previous month.

---------------------------------------------------------
6. CUSTOMER QUESTIONS
---------------------------------------------------------

For customer ranking:

→ get_top_customers

For customer activity:

→ get_customer_activity

For retention or churn risk:

→ get_customer_risk

Do not claim that a customer will definitely churn.

Use language such as:

"potentially at risk"
"shows signs of inactivity"
"may require retention attention"

---------------------------------------------------------
7. INVENTORY QUESTIONS
---------------------------------------------------------

Use:

→ get_inventory_risks

when the user asks which products are below reorder
levels.

Use:

→ get_reorder_priorities

when the user asks what should be reordered first.

Use:

→ get_cross_domain_risks

when inventory must be evaluated together with
sales velocity and profitability.

---------------------------------------------------------
8. NEVER INVENT BUSINESS FACTS
---------------------------------------------------------

Never fabricate:

- revenue
- customers
- products
- profit
- inventory
- risk levels
- dates
- percentages
- trends

All business facts must come from ERP tools.

You may calculate simple derived metrics from tool
results, but clearly explain the calculation.

---------------------------------------------------------
9. TOOL RESULTS ARE AUTHORITATIVE
---------------------------------------------------------

If a tool provides:

risk_level
profit_margin
health_score
trend
anomaly_level

use the value supplied by the analytics engine.

Do not replace it with your own arbitrary classification.

---------------------------------------------------------
10. MULTI-TOOL ANSWERS
---------------------------------------------------------

When multiple tools are used:

1. Gather the required evidence.
2. Compare the results.
3. Identify relationships between them.
4. Identify the most important business implication.
5. Give a concise management recommendation.

Do not simply dump raw tool results.

The final answer should explain:

WHAT happened
WHY it matters
WHAT management should consider doing

---------------------------------------------------------
11. AVOID REDUNDANT TOOL CALLS
---------------------------------------------------------

Do not call the same tool repeatedly unless:

- the previous result was insufficient,
- a different limit is required,
- or additional information is genuinely necessary.

---------------------------------------------------------
12. FOLLOW-UP QUESTIONS
---------------------------------------------------------

Use conversation memory when the user refers to
previous results.

Examples:

User:
"What are our top 5 products?"

Follow-up:
"Which of these have low margins?"

The agent should understand that "these" refers to
the previously returned products.

User:
"Show me the highest-risk ones."

The agent should use the previous product context
when appropriate.

---------------------------------------------------------
13. FINAL RESPONSE STYLE
---------------------------------------------------------

Do not expose internal tool names.

Do not describe your hidden reasoning.

Do not dump JSON unless the user explicitly asks
for raw data.

Present business information clearly.

For management questions, prefer:

Executive takeaway
Key findings
Business impact
Recommended actions

Use numbers whenever available.

=========================================================
EXECUTIVE RESPONSE FORMAT
=========================================================

When answering business questions, do not dump raw Python
dictionaries, JSON, Decimal objects, or internal tool output.

Transform the tool results into a clear business answer.

---------------------------------------------------------
FOR SIMPLE QUESTIONS
---------------------------------------------------------

Answer directly.

Example:

User:
"What is our total revenue?"

Good:

"Our total revenue from completed orders is ₹1.225 billion."

Do not unnecessarily create an executive report for a
simple factual question.

---------------------------------------------------------
FOR ANALYTICAL QUESTIONS
---------------------------------------------------------

Use this structure when appropriate:

EXECUTIVE TAKEAWAY

One or two sentences explaining the most important finding.

KEY FINDINGS

• Finding 1
• Finding 2
• Finding 3

BUSINESS IMPACT

Explain why the findings matter to the business.

RECOMMENDED ACTIONS

1. Action 1
2. Action 2
3. Action 3

---------------------------------------------------------
FOR MANAGEMENT QUESTIONS
---------------------------------------------------------

For questions such as:

"What should management worry about?"
"What are our biggest risks?"
"How is the business doing?"
"What should we focus on?"

Always prioritize:

1. Critical risks
2. High-priority operational problems
3. Revenue or profitability concerns
4. Inventory concerns
5. Customer concerns
6. Recommended actions

Do not treat every finding as equally important.

---------------------------------------------------------
NUMBERS
---------------------------------------------------------

Use human-readable numbers.

Instead of:

Decimal('1224832443.93')

write:

₹1.225 billion

Instead of:

Decimal('14.56')

write:

14.56%

Instead of:

Decimal('0.45')

write:

0.45 days

Round financial and percentage values appropriately.

---------------------------------------------------------
RISK LANGUAGE
---------------------------------------------------------

Use the risk levels provided by the analytics tools:

CRITICAL
HIGH
MEDIUM
LOW

Do not invent a different risk classification.

When discussing potential customer churn, inventory
shortages, or business problems, distinguish between
observed evidence and predictions.

Do not claim something is certain unless the ERP data
directly establishes it.

---------------------------------------------------------
RAW DATA
---------------------------------------------------------

Only provide raw structured data when the user explicitly
asks for:

- raw data
- JSON
- database output
- complete tool results
- detailed records

Otherwise, summarize the information for the user.
"""


# ---------------------------------------------------------
# TOOL DEFINITIONS
# ---------------------------------------------------------

TOOLS = [

    {
        "type": "function",
        "name": "get_total_revenue",
        "description": (
            "Calculate total revenue generated from completed "
            "orders in the ERP system."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_monthly_sales",
        "description": (
            "Return monthly revenue and completed order counts. "
            "Use this for sales trends, monthly performance, "
            "revenue over time, and month-by-month analysis."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_top_products",
        "description": (
    "Return products ranked by total revenue from completed "
    "orders. Use this for questions about highest-revenue, "
    "best-selling-by-revenue, or top-performing products. "
    "This ranks products by revenue, not profit or units sold."
),
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of products to return.",
                    "minimum": 1,
                    "maximum": 20
                }
            },
            "required": ["limit"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_product_profitability",
        "description": (
    "Return products ranked by total profit from completed "
    "orders, including units sold, revenue, profit, and "
    "profit margin. Use this for questions about the most "
    "profitable products. This ranks by profit, not revenue."
),
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of products to return.",
                    "minimum": 1,
                    "maximum": 20
                }
            },
            "required": ["limit"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_top_customers",
        "description": (
            "Return customers ranked by total spending from "
            "completed orders."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of customers to return.",
                    "minimum": 1,
                    "maximum": 20
                }
            },
            "required": ["limit"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_customer_activity",
        "description": (
            "Return customer activity including last completed "
            "order date, days since last order, completed orders, "
            "and total spending. Use this to identify inactive "
            "or potentially at-risk customers."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_inventory_risks",
        "description": (
            "Return products whose current inventory is below "
            "their reorder level, including stock deficit. "
            "Use this for inventory and reorder questions."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_supplier_performance",
        "description": (
            "Return supplier performance including products "
            "supplied, units sold, revenue, and profit. Use this "
            "for supplier and procurement analysis."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
    "type": "function",
    "name": "get_reorder_priorities",
    "description": (
        "Identify products that should be prioritized for "
        "reordering by combining inventory levels and "
        "estimated sales velocity. Use this for questions "
        "about what to reorder first or inventory urgency."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of products to return.",
                "minimum": 1,
                "maximum": 20
            }
        },
        "required": ["limit"],
        "additionalProperties": False
    },
    "strict": True
    },

    {
    "type": "function",
    "name": "get_customer_risk",
    "description": (
        "Identify customers flagged as potentially at risk "
        "based on inactivity and spending thresholds. "
        "Use this for customer retention and churn-risk "
        "questions."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of customers to return.",
                "minimum": 1,
                "maximum": 20
            }
        },
        "required": ["limit"],
        "additionalProperties": False
    },
    "strict": True
    },

    {
    "type": "function",
    "name": "get_sales_profitability_gaps",
    "description": (
        "Identify products with substantial sales volume "
        "but relatively low profit margins. Use this to "
        "find products that sell well but may have weak "
        "profitability."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of products to return.",
                "minimum": 1,
                "maximum": 20
            }
        },
        "required": ["limit"],
        "additionalProperties": False
    },
    "strict": True
    },

    {
    "type": "function",
    "name": "get_business_health",
    "description": (
        "Return an overall operational health assessment "
        "of the ERP business. Includes revenue, completed "
        "orders, inventory risk, customer inactivity, "
        "profitability risk, and a transparent operational "
        "health score. Use this for questions such as "
        "'How is the business doing?', 'Give me a management "
        "summary', or 'What should management be concerned about?'"
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    },
    "strict": True
    },

    {
    "type": "function",
    "name": "get_revenue_anomalies",
    "description": (
        "Detect unusually high or low monthly revenue "
        "using historical revenue patterns and statistical "
        "z-scores. Use this when the user asks about unusual "
        "sales behavior, revenue anomalies, unexpected "
        "changes, or unusual months."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    },
    "strict": True
    },

    {
    "type": "function",
    "name": "get_executive_insights",
    "description": (
        "Generate a management-level summary of the ERP "
        "business. Combines operational health, revenue "
        "trends, unusual revenue behavior, inventory "
        "priorities, and profitability risks. Use this for "
        "questions such as 'What should management know?', "
        "'Give me an executive summary', 'What are the "
        "biggest business risks?', or 'What should we focus "
        "on right now?'"
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    },
    "strict": True
    },

    {
    "type": "function",
    "name": "get_cross_domain_risks",
    "description": (
    "Identify products with overlapping business risks by "
    "combining inventory availability, sales velocity, and "
    "profitability. Use this for questions about products "
    "requiring urgent attention, products with multiple "
    "business risks, or the most dangerous operational "
    "risks. Risk levels are calculated by the analytics "
    "engine and should not be inferred independently."
),
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of risk products to return.",
                "minimum": 1,
                "maximum": 20
            }
        },
        "required": ["limit"],
        "additionalProperties": False
    },
    "strict": True
    }


]


# ---------------------------------------------------------
# TOOL MAP
# ---------------------------------------------------------

TOOL_FUNCTIONS = {
    "get_total_revenue": get_total_revenue,
    "get_monthly_sales": get_monthly_sales,
    "get_top_products": get_top_products,
    "get_product_profitability": get_product_profitability,
    "get_top_customers": get_top_customers,
    "get_customer_activity": get_customer_activity,
    "get_inventory_risks": get_inventory_risks,
    "get_supplier_performance": get_supplier_performance,
    "get_reorder_priorities": get_reorder_priorities,
    "get_customer_risk": get_customer_risk,
    "get_sales_profitability_gaps": get_sales_profitability_gaps,
    "get_business_health": get_business_health,
    "get_revenue_anomalies": get_revenue_anomalies,
    "get_executive_insights": get_executive_insights,
    "get_cross_domain_risks": get_cross_domain_risks
}

# ---------------------------------------------------------
# TOOL VALIDATION
# ---------------------------------------------------------

def validate_tools():
    """
    Make sure every tool exposed to the AI has a
    corresponding Python function.
    """

    registered_tools = set(TOOL_FUNCTIONS.keys())

    defined_tools = {
        tool["name"]
        for tool in TOOLS
    }

    missing_functions = defined_tools - registered_tools
    missing_definitions = registered_tools - defined_tools

    if missing_functions:
        raise RuntimeError(
            "Tools defined in TOOLS but missing from "
            f"TOOL_FUNCTIONS: {missing_functions}"
        )

    if missing_definitions:
        raise RuntimeError(
            "Tools registered in TOOL_FUNCTIONS but missing "
            f"from TOOLS: {missing_definitions}"
        )

    print(
        f"Tool validation successful: "
        f"{len(defined_tools)} tools registered."
    )

validate_tools()

# ---------------------------------------------------------
# TOOL EXECUTION
# ---------------------------------------------------------

def execute_tool(tool_name, arguments):
    """
    Safely execute an approved ERP analytics tool.
    """

    # -------------------------------------------------
    # 1. Check whether the requested tool exists
    # -------------------------------------------------

    if tool_name not in TOOL_FUNCTIONS:

        return {
            "error": True,
            "message": (
                f"Unknown ERP tool: {tool_name}"
            )
        }

    tool_function = TOOL_FUNCTIONS[tool_name]

    # -------------------------------------------------
    # 2. Make sure arguments are a dictionary
    # -------------------------------------------------

    if arguments is None:
        arguments = {}

    if not isinstance(arguments, dict):

        return {
            "error": True,
            "message": (
                f"Invalid arguments for "
                f"tool '{tool_name}'."
            )
        }

    # -------------------------------------------------
    # 3. Execute the tool
    # -------------------------------------------------

    try:

        result = tool_function(
            **arguments
        )

        return {
            "error": False,
            "tool": tool_name,
            "data": result
        }

    # -------------------------------------------------
    # 4. Handle incorrect arguments
    # -------------------------------------------------

    except TypeError as e:

        return {
            "error": True,
            "tool": tool_name,
            "message": (
                f"Invalid arguments for "
                f"'{tool_name}': {str(e)}"
            )
        }

    # -------------------------------------------------
    # 5. Handle database / execution errors
    # -------------------------------------------------

    except Exception as e:

        return {
            "error": True,
            "tool": tool_name,
            "message": (
                f"Tool '{tool_name}' failed: "
                f"{str(e)}"
            )
        }


# ---------------------------------------------------------
# SERIALIZE RESULTS
# ---------------------------------------------------------

def serialize_result(value):
    """
    Convert ERP database results into JSON-safe data.
    """

    if value is None:
        return None

    # ---------------------------------------------
    # Dictionary
    # ---------------------------------------------

    if isinstance(value, dict):

        return {
            str(key): serialize_result(val)
            for key, val in value.items()
        }

    # ---------------------------------------------
    # List / tuple
    # ---------------------------------------------

    if isinstance(value, (list, tuple)):

        return [
            serialize_result(item)
            for item in value
        ]

    # ---------------------------------------------
    # Decimal
    # ---------------------------------------------

    try:

        from decimal import Decimal

        if isinstance(value, Decimal):

            return float(value)

    except Exception:
        pass

    # ---------------------------------------------
    # Basic JSON-safe values
    # ---------------------------------------------

    if isinstance(
        value,
        (str, int, float, bool)
    ):
        return value

    # ---------------------------------------------
    # Fallback
    # ---------------------------------------------

    return str(value)


# ---------------------------------------------------------
# AGENT
# ---------------------------------------------------------
def update_memory(memory, tool_name, tool_result):
    """
    Store only the most useful information from ERP tool
    results for follow-up questions.
    """

    if not isinstance(tool_result, dict):
        return memory

    if tool_result.get("error"):
        return memory

    data = tool_result.get("data")

    memory["last_tool"] = tool_name

    # -------------------------------------------------
    # PRODUCT MEMORY
    # -------------------------------------------------

    product_tools = {
        "get_top_products",
        "get_product_profitability",
        "get_inventory_risks",
        "get_reorder_priorities",
        "get_sales_profitability_gaps",
        "get_cross_domain_risks"
    }

    if tool_name in product_tools:

        if isinstance(data, dict):
            data = [data]

        if isinstance(data, list):

            compact_products = []

            for product in data:

                if not isinstance(product, dict):
                    continue

                compact_product = {}

                important_fields = [
                    "product_id",
                    "product_name",
                    "category",
                    "units_sold",
                    "revenue",
                    "profit",
                    "profit_margin",
                    "stock_quantity",
                    "reorder_level",
                    "estimated_days_of_stock",
                    "risk_level"
                ]

                for field in important_fields:

                    if field in product:
                        compact_product[field] = product[field]

                compact_products.append(
                    compact_product
                )

            memory["last_products"] = compact_products

        memory["last_topic"] = "products"

    # -------------------------------------------------
    # CUSTOMER MEMORY
    # -------------------------------------------------

    customer_tools = {
        "get_top_customers",
        "get_customer_activity",
        "get_customer_risk"
    }

    if tool_name in customer_tools:

        if isinstance(data, dict):
            data = [data]

        if isinstance(data, list):

            compact_customers = []

            for customer in data:

                if not isinstance(customer, dict):
                    continue

                compact_customer = {}

                important_fields = [
                    "customer_id",
                    "customer_name",
                    "total_spending",
                    "spending",
                    "number_of_orders",
                    "last_ordered_date",
                    "days_since_last_ordered",
                    "risk_level"
                ]

                for field in important_fields:

                    if field in customer:
                        compact_customer[field] = customer[field]

                compact_customers.append(
                    compact_customer
                )

            memory["last_customers"] = compact_customers

        memory["last_topic"] = "customers"

    # -------------------------------------------------
    # REVENUE MEMORY
    # -------------------------------------------------

    revenue_tools = {
        "get_total_revenue",
        "get_monthly_sales",
        "get_revenue_anomalies",
        "get_executive_insights"
    }

    if tool_name in revenue_tools:

        memory["last_topic"] = "revenue"

        if isinstance(data, dict):

            if "month" in data:
                memory["last_period"] = data["month"]

            elif "current_month" in data:
                memory["last_period"] = data["current_month"]

            elif "revenue_trend" in data:

                trend = data["revenue_trend"]

                if isinstance(trend, dict):

                    memory["last_period"] = (
                        trend.get("month")
                        or trend.get("current_month")
                    )

    return memory

def build_memory_context(memory):
    """
    Build a small, clean context object for the AI.

    Only information useful for resolving follow-up
    questions is included.
    """

    return {
        "last_tool": memory.get("last_tool"),

        "last_topic": memory.get("last_topic"),

        "last_period": memory.get("last_period"),

        "last_products": memory.get(
            "last_products",
            []
        )[:10],

        "last_customers": memory.get(
            "last_customers",
            []
        )[:10]
    }


def log_agent(message):
    """
    Print concise operational information about
    what the agent is doing.
    """
    print(f"\n[AGENT] {message}")

def generate_recommendations(insights):
    """
    Convert ERP analytics into prioritized business
    recommendations.

    This function does NOT modify the database.
    It only recommends actions.
    """

    recommendations = []

    if not isinstance(insights, dict):
        return recommendations

    # -------------------------------------------------
    # Cross-domain risks
    # -------------------------------------------------

    cross_domain_risks = insights.get(
        "cross_domain_risks",
        []
    )

    for item in cross_domain_risks:

        risk = item.get("risk_level")

        if risk == "CRITICAL":

            recommendations.append({
                "priority": "CRITICAL",
                "category": "INVENTORY",
                "product_id": item.get("product_id"),
                "product": item.get("product_name"),
                "action": "Reorder immediately.",
                "reason": (
                    f"Stock is {item.get('stock_quantity')} "
                    f"units with approximately "
                    f"{item.get('estimated_days_of_stock')} "
                    f"days of stock remaining."
                )
            })

        elif risk == "HIGH":

            recommendations.append({
                "priority": "HIGH",
                "category": "INVENTORY",
                "product_id": item.get("product_id"),
                "product": item.get("product_name"),
                "action": "Prioritize replenishment.",
                "reason": (
                    f"Estimated stock coverage is only "
                    f"{item.get('estimated_days_of_stock')} "
                    f"days."
                )
            })

    # -------------------------------------------------
    # Profitability gaps
    # -------------------------------------------------

    profitability_gaps = insights.get(
        "profitability_gaps",
        []
    )

    for item in profitability_gaps:

        margin = item.get("profit_margin")

        if margin is not None and margin < 15:

            recommendations.append({
                "priority": "MEDIUM",
                "category": "PROFITABILITY",
                "product_id": item.get("product_id"),
                "product": item.get("product_name"),
                "action": (
                    "Review pricing, costs, or supplier terms."
                ),
                "reason": (
                    f"Product has high sales volume but "
                    f"only {margin}% profit margin."
                )
            })

    # -------------------------------------------------
    # Inventory priorities
    # -------------------------------------------------

    reorder_priorities = insights.get(
        "reorder_priorities",
        []
    )

    for item in reorder_priorities[:5]:

        days = item.get(
            "estimated_days_of_stock"
        )

        if days is not None and days < 1:

            recommendations.append({
                "priority": "HIGH",
                "category": "INVENTORY",
                "product_id": item.get("product_id"),
                "product": item.get("product_name"),
                "action": "Prioritize inventory replenishment.",
                "reason": (
                    f"Only {days} days of estimated "
                    f"stock remain."
                )
            })

    # -------------------------------------------------
    # Revenue anomalies
    # -------------------------------------------------

    anomalies = insights.get(
        "significant_revenue_anomalies",
        []
    )

    for anomaly in anomalies:

        if anomaly.get("anomaly_direction") == "NEGATIVE":

            recommendations.append({
                "priority": "MEDIUM",
                "category": "REVENUE",
                "action": (
                    "Investigate the unusual revenue decline."
                ),
                "reason": (
                    f"{anomaly.get('month')} recorded "
                    f"unusually low revenue compared "
                    f"with historical performance."
                )
            })

    # -------------------------------------------------
    # Remove duplicate recommendations
    # -------------------------------------------------

    unique = []
    seen = set()

    for recommendation in recommendations:

        key = (
            recommendation.get("product_id"),
            recommendation.get("category"),
            recommendation.get("action")
        )

        if key not in seen:

            seen.add(key)
            unique.append(recommendation)

    # -------------------------------------------------
    # Priority ordering
    # -------------------------------------------------

    priority_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    unique.sort(
        key=lambda x: priority_order.get(
            x.get("priority"),
            99
        )
    )

    return unique

def ask_agent(
    question,
    conversation=None,
    memory=None,
    max_tool_rounds=5
):
    """
    Send a user question to the ERP AI agent.

    Uses previous_response_id only within the current
    user question's tool-calling loop.
    """

    # =================================================
    # INITIALIZE
    # =================================================

    if conversation is None:
        conversation = []

    if memory is None:
        memory = {
            "last_products": [],
            "last_customers": [],
            "last_tool": None,
            "last_topic": None,
            "last_period": None
        }

    # =================================================
    # BUILD MEMORY CONTEXT
    # =================================================

    memory_context = serialize_result(
        build_memory_context(memory)
    )

    if not isinstance(memory_context, str):
        memory_context = json.dumps(
            memory_context,
            indent=2,
            default=str
        )

    memory_message = {
        "role": "user",
        "content": (
            "Internal working context for this conversation. "
            "Use this only to resolve references and maintain "
            "continuity. Do not mention this internal context "
            "unless relevant.\n\n"
            + memory_context
        )
    }

    # =================================================
    # BUILD CLEAN MODEL INPUT
    # =================================================

    current_input = [
        memory_message,
        *conversation,
        {
            "role": "user",
            "content": question
        }
    ]

    # =================================================
    # CURRENT QUESTION TOOL LOOP
    # =================================================

    response = None

    for round_number in range(max_tool_rounds):

        log_agent(
            f"Starting agent round "
            f"{round_number + 1}/{max_tool_rounds}"
        )

        # =================================================
        # MODEL REQUEST
        # =================================================

        try:

            if response is None:

                # -----------------------------------------
                # First request for this user question
                # -----------------------------------------

                response = client.responses.create(
                    model=MODEL,
                    instructions=SYSTEM_INSTRUCTIONS,
                    tools=TOOLS,
                    input=current_input
                )

            else:

                # -----------------------------------------
                # Continue current tool loop
                # -----------------------------------------

                response = client.responses.create(
                    model=MODEL,
                    instructions=SYSTEM_INSTRUCTIONS,
                    tools=TOOLS,
                    previous_response_id=response.id,
                    input=tool_outputs
                )

        except Exception as e:

            error_type = type(e).__name__

            log_agent(
                f"OpenAI API request failed: "
                f"{error_type}"
            )

            log_agent(
                f"API error details: {str(e)}"
            )

            if error_type == "RateLimitError":

                return (
                    "The ERP Agent reached the current "
                    "AI API rate limit or quota. "
                    "Please check your API usage or billing."
                )

            elif error_type == "AuthenticationError":

                return (
                    "The ERP Agent could not authenticate "
                    "with the AI service. Please check "
                    "the API key."
                )

            elif error_type == "APIConnectionError":

                return (
                    "The ERP Agent could not reach the "
                    "AI service. Please check your "
                    "internet connection, DNS, VPN, "
                    "or proxy settings."
                )

            elif error_type == "BadRequestError":

                return (
                    "The ERP Agent sent an invalid request "
                    "to the AI service.\n\n"
                    f"Details: {str(e)}"
                )

            else:

                return (
                    "The ERP Agent encountered an unexpected "
                    f"AI service error: {error_type}\n\n"
                    f"Details: {str(e)}"
                )

        # =================================================
        # FIND TOOL CALLS
        # =================================================

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        log_agent(
            f"Model requested "
            f"{len(tool_calls)} tool(s)."
        )

        # =================================================
        # FINAL ANSWER
        # =================================================

        if not tool_calls:

            log_agent(
                "Generating final answer."
            )

            answer = response.output_text

            # ---------------------------------------------
            # Store ONLY clean conversation history
            # ---------------------------------------------

            conversation.append({
                "role": "user",
                "content": question
            })

            conversation.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        # =================================================
        # EXECUTE TOOLS
        # =================================================

        tool_outputs = []

        for tool_call in tool_calls:

            tool_name = tool_call.name

            log_agent(
                f"Calling tool: {tool_name}"
            )

            # -------------------------------------------------
            # Parse arguments
            # -------------------------------------------------

            try:

                arguments = json.loads(
                    tool_call.arguments
                )

            except (
                json.JSONDecodeError,
                TypeError
            ):

                log_agent(
                    f"Invalid arguments for tool: "
                    f"{tool_name}"
                )

                tool_output = {
                    "error": True,
                    "message": (
                        f"Invalid arguments supplied "
                        f"for tool '{tool_name}'."
                    )
                }

            else:

                # -------------------------------------------------
                # Execute tool
                # -------------------------------------------------

                try:

                    tool_output = execute_tool(
                        tool_name,
                        arguments
                    )

                    if (
                        isinstance(tool_output, dict)
                        and not tool_output.get("error")
                    ):

                        log_agent(
                            f"Tool completed: "
                            f"{tool_name}"
                        )

                    # ---------------------------------------------
                    # Update working memory
                    # ---------------------------------------------

                    update_memory(
                        memory,
                        tool_name,
                        tool_output
                    )

                except Exception as e:

                    log_agent(
                        f"Tool failed: "
                        f"{tool_name} - {str(e)}"
                    )

                    tool_output = {
                        "error": True,
                        "message": (
                            f"Tool '{tool_name}' "
                            f"failed during execution: "
                            f"{str(e)}"
                        )
                    }

            # =================================================
            # SERIALIZE TOOL OUTPUT
            # =================================================

            serialized_output = serialize_result(
                tool_output
            )

            if not isinstance(
                serialized_output,
                str
            ):

                serialized_output = json.dumps(
                    serialized_output,
                    indent=2,
                    default=str
                )

            # =================================================
            # BUILD TOOL OUTPUT
            # =================================================

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": serialized_output
            })

        log_agent(
            f"Returning {len(tool_outputs)} "
            f"tool result(s) to model."
        )

    # =================================================
    # MAX TOOL ROUNDS
    # =================================================

    log_agent(
        "Maximum tool rounds exceeded."
    )

    return (
        "The ERP Agent reached its maximum "
        f"tool-processing limit of {max_tool_rounds} rounds."
    )# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------
def run_cli():

    print("=" * 60)
    print("        ERP AI BUSINESS ANALYST")
    print("=" * 60)

    print("\nType 'exit' to quit.")
    print("Type 'clear' to start a new conversation.\n")

    conversation = []

memory = {
    "last_products": [],
    "last_customers": [],
    "last_tool": None,
    "last_topic": None,
    "last_period": None
}

def run_local_diagnostics():

    print("=" * 60)
    print("ERP AGENT LOCAL DIAGNOSTICS")
    print("=" * 60)

    # =================================================
    # 1. TOOL REGISTRY
    # =================================================

    print("\n[1] Tool Registry")

    validate_tools()

    print("PASS: Tool definitions and functions match.")

    # =================================================
    # 2. TOOL EXECUTION
    # =================================================

    print("\n[2] Tool Execution")

    result = execute_tool(
        "get_cross_domain_risks",
        {"limit": 3}
    )

    if (
        not isinstance(result, dict)
        or result.get("error")
    ):
        print("FAIL:", result)
        return

    print("PASS: get_cross_domain_risks executed.")

    # =================================================
    # 3. SERIALIZATION
    # =================================================

    print("\n[3] Serialization")

    try:

        serialized = serialize_result(result)

        # Verify serialized result is JSON-safe
        json.dumps(
            serialized,
            indent=2,
            default=str
        )

    except Exception as e:

        print(
            "FAIL: Serialization failed:",
            type(e).__name__,
            str(e)
        )
        return

    print(
        "PASS: Tool result serialized successfully."
    )

    # =================================================
    # 4. WORKING MEMORY
    # =================================================

    print("\n[4] Working Memory")

    memory = {
        "last_products": [],
        "last_customers": [],
        "last_tool": None,
        "last_topic": None,
        "last_period": None
    }

    update_memory(
        memory,
        "get_cross_domain_risks",
        result
    )

    print(
        f"Last tool: "
        f"{memory['last_tool']}"
    )

    print(
        f"Last topic: "
        f"{memory['last_topic']}"
    )

    print(
        f"Remembered products: "
        f"{len(memory['last_products'])}"
    )

    # =================================================
    # 5. MEMORY CONTEXT
    # =================================================

    print("\n[5] Memory Context")

    try:

        memory_context = build_memory_context(
            memory
        )

        print(
            json.dumps(
                memory_context,
                indent=2,
                default=str
            )
        )

    except Exception as e:

        print(
            "FAIL: Memory context failed:",
            type(e).__name__,
            str(e)
        )
        return

    print(
        "PASS: Memory context generated successfully."
    )

    # =================================================
    # 6. RECOMMENDATION ENGINE
    # =================================================

    print("\n[6] Recommendation Engine")

    executive_data = execute_tool(
        "get_executive_insights",
        {}
    )

    if (
        not isinstance(executive_data, dict)
        or executive_data.get("error")
    ):

        print(
            "FAIL: Could not retrieve "
            "executive insights."
        )
        return

    recommendations = generate_recommendations(
        executive_data.get(
            "data",
            {}
        )
    )

    print(
        f"Generated {len(recommendations)} "
        f"recommendations."
    )

    for recommendation in recommendations[:5]:

        print(
            f"{recommendation.get('priority', 'UNKNOWN')} | "
            f"{recommendation.get('category', 'UNKNOWN')} | "
            f"{recommendation.get('product', 'Business')} | "
            f"{recommendation.get('action', '')}"
        )

    print(
        "PASS: Recommendation engine executed."
    )

    # =================================================
    # FINAL
    # =================================================

    print()

    print("=" * 60)
    print("ALL LOCAL DIAGNOSTICS PASSED")
    print("=" * 60)
# ---------------------------------------------------------
# PROGRAM ENTRY
# ---------------------------------------------------------

if __name__ == "__main__":

    import sys

    if "--diagnostic" in sys.argv:

        run_local_diagnostics()

    else:

        conversation = []

        memory = {
            "last_products": [],
            "last_customers": [],
            "last_tool": None,
            "last_topic": None,
            "last_period": None
        }

        while True:

            question = input(
                "\nAsk your ERP Agent: "
            ).strip()

            if question.lower() in {
                "exit",
                "quit",
                "q"
            }:

                print("\nGoodbye!")
                break

            if not question:
                continue

            try:

                answer = ask_agent(
                    question,
                    conversation=conversation,
                    memory=memory
                )

                print("\nERP Agent:")
                print(answer)

            except Exception as e:

                print("\nAgent Error:")
                print(e)