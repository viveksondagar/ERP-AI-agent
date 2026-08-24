# 🤖 ERP AI Agent

> An AI-powered ERP business intelligence and decision-support system that enables users to interact with enterprise data using natural language.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.x-blue?logo=mysql)](https://www.mysql.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/)

---

## 📌 Overview

ERP AI Agent is an AI-powered enterprise analytics assistant designed to make ERP data accessible through natural-language conversations.

Instead of requiring users to write SQL queries or navigate multiple ERP reports, users can ask business questions such as:

> "What are our top 5 products by revenue?"

> "Which products should we reorder first?"

> "What are the biggest risks facing our business?"

The AI Agent determines which business tools are required, retrieves the relevant ERP data, analyzes the results, and generates a business-oriented response.

The system combines:

- AI-powered reasoning
- Tool/function calling
- ERP database analytics
- Conversational context
- Inventory intelligence
- Profitability analysis
- Business risk detection
- Management recommendations
- Cloud database infrastructure
- Interactive Streamlit UI

---

# 🚀 Live Demo

**Live Application:**  
[Add your Streamlit URL here]

**GitHub Repository:**  
[Add your GitHub repository URL here]

> ⚠️ The live application uses demonstration ERP data. Access and usage may be restricted depending on deployment configuration.

---

# 🎯 Project Objectives

The primary objectives of the project are:

1. Enable non-technical users to interact with ERP data using natural language.
2. Reduce dependency on manually written SQL queries.
3. Provide real-time business insights from ERP data.
4. Combine multiple ERP domains into a single AI-powered assistant.
5. Provide actionable recommendations instead of only raw data.
6. Demonstrate how AI agents can be integrated with enterprise databases.
7. Build a deployable cloud-based ERP intelligence system.

---

# 🧠 Key Features

## 1. Natural Language ERP Queries

Users can ask questions in plain English without knowing SQL.

Examples:

```text
What is our total revenue?

What are our top 5 products by revenue?

Which products have the highest profit margins?

Who are our most valuable customers?
````

---

## 2. AI Agent with Tool Calling

The system uses an AI agent capable of selecting specialized ERP tools based on the user's question.

Instead of directly generating an answer from static knowledge, the agent can:

```text
User Question
      ↓
AI Agent
      ↓
Select Required Tool(s)
      ↓
Execute ERP Query
      ↓
Retrieve Data
      ↓
Analyze Results
      ↓
Generate Business Response
```

This allows the system to perform multi-step reasoning over live ERP data.

---

## 3. Multiple ERP Business Tools

The system contains specialized tools for different business domains, including:

* Revenue analysis
* Product performance
* Customer analysis
* Inventory analysis
* Reorder prioritization
* Profitability analysis
* Sales analysis
* Cross-domain risk analysis
* Executive business insights
* And additional ERP analytics tools

The agent can select one or multiple tools depending on the complexity of the question.

---

# 📊 Business Intelligence Capabilities

The system can answer questions across several ERP domains.

### Revenue

* Total revenue
* Revenue trends
* Product revenue contribution
* Revenue performance

### Products

* Top products by revenue
* Product sales performance
* Product profitability
* High-volume products

### Inventory

* Current stock levels
* Stock coverage
* Reorder levels
* Stockout risks
* Reorder priorities

### Profitability

* Profit margins
* Low-margin products
* High-sales / low-margin products
* Profitability risks

### Customers

* Customer purchasing behavior
* High-value customers
* Order activity
* Customer performance

### Suppliers

* Supplier relationships
* Product supply
* Supply-chain risks

### Employees & Departments

* Employee distribution
* Department analysis
* Organizational information

---

# 🔥 Example Questions

The following questions demonstrate the capabilities of the agent:

```text
Give me an executive summary of the current business performance.

What is our total revenue?

What are our top 5 products by revenue?

Which products have the highest profit margins?

Which products have high sales but low profit margins?

Which products are currently at risk of stockout?

Which products should we reorder first?

Who are our most valuable customers?

Which suppliers provide the most products?

What are the biggest risks facing our business right now?

What are the biggest opportunities for improving profitability?

Which products have low inventory, high demand, and strong profit margins?

Based on the ERP data, what should management prioritize right now?
```

---

# 🧩 Conversational Memory

The agent maintains conversational context to support follow-up questions.

For example:

```text
User:
What are our top 5 products by revenue?

Agent:
[Returns top 5 products]

User:
Which of those have the lowest profit margins?

Agent:
[Uses the previous context to analyze those products]

User:
What should management do about them?

Agent:
[Provides recommendations]
```

This allows users to have a natural conversation instead of repeating the context in every question.

---

# 🔄 Multi-Tool Reasoning

One of the key capabilities of the system is its ability to use multiple tools for complex business questions.

For example:

> "Which products should we prioritize for reordering, and among those products which ones have the weakest profit margins?"

The agent can determine that it needs both:

```text
Reorder Priority Tool
        +
Sales / Profitability Tool
        ↓
Combined Analysis
        ↓
Business Recommendation
```

This allows the system to move beyond simple database retrieval.

---

# 🏗️ System Architecture

```text
                     ┌───────────────────┐
                     │       USER        │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │   STREAMLIT UI    │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │    AI AGENT       │
                     │                   │
                     │ OpenAI API        │
                     │ Tool Selection    │
                     │ Reasoning         │
                     │ Memory            │
                     └─────────┬─────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
           ┌─────────────────┐   ┌─────────────────┐
           │   ERP TOOLS     │   │  Conversation   │
           │                 │   │    Memory       │
           │ Revenue         │   │                 │
           │ Products        │   │ Previous        │
           │ Inventory       │   │ Context         │
           │ Customers       │   │ Topics          │
           │ Profitability   │   │ Results         │
           │ Risk Analysis   │   │                 │
           └────────┬────────┘   └─────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │  DATABASE LAYER │
           │   database.py   │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │   AIVEN MYSQL   │
           │                 │
           │ ERP Database    │
           └─────────────────┘
```

---

# 🗄️ Database Architecture

The ERP database contains eight primary tables:

```text
customers
departments
employees
inventory
order_items
orders
products
suppliers
```

### Core relationships

```text
CUSTOMERS
    │
    │ 1:N
    ▼
ORDERS
    │
    │ 1:N
    ▼
ORDER_ITEMS
    │
    │ N:1
    ▼
PRODUCTS
    │
    ├─────────────── INVENTORY
    │
    └─────────────── SUPPLIERS

DEPARTMENTS
    │
    │ 1:N
    ▼
EMPLOYEES
```

The database acts as the source of truth for the AI agent's business analysis.

---

# 🛠️ Technology Stack

| Technology                | Purpose                             |
| ------------------------- | ----------------------------------- |
| Python                    | Core application and business logic |
| OpenAI API                | AI reasoning and tool calling       |
| Streamlit                 | Interactive web interface           |
| MySQL                     | ERP relational database             |
| Aiven                     | Cloud-hosted MySQL infrastructure   |
| mysql-connector-python    | Database connectivity               |
| python-dotenv             | Local environment configuration     |
| Git                       | Version control                     |
| GitHub                    | Source code hosting                 |
| Streamlit Community Cloud | Application deployment              |

---

# 📁 Project Structure

```text
erp-ai-agent/
│
├── app.py
│       └── Streamlit application / user interface
│
├── agent.py
│       └── AI agent logic and tool calling
│
├── database.py
│       └── MySQL connection and query execution
│
├── analytics.py
│       └── ERP analytics and business calculations
│
├── requirements.txt
│       └── Python dependencies
│
├── .gitignore
│       └── Sensitive files and local artifacts
│
├── README.md
│       └── Project documentation
│
└── .env
        └── Local environment variables
        └── NOT committed to GitHub
```

---

# 🔐 Security

Sensitive credentials are not stored directly in the source code.

Local development uses environment variables:

```text
.env
```

Production deployment uses:

```text
Streamlit Secrets
```

Sensitive information includes:

* OpenAI API keys
* Database passwords
* Database connection credentials
* SSL certificates

These values should never be committed to GitHub.

### Example `.gitignore`

```text
.env
ca.pem
erp_ai_backup.sql
__pycache__/
*.pyc
```

---

# ☁️ Deployment Architecture

The application is deployed using Streamlit Community Cloud.

```text
                 INTERNET
                    │
                    ▼
          ┌──────────────────┐
          │ Streamlit Cloud  │
          │                  │
          │    app.py        │
          │    agent.py      │
          │    tools         │
          └────────┬─────────┘
                   │
          ┌────────┴─────────┐
          │                  │
          ▼                  ▼
    OpenAI API          Aiven MySQL
                            │
                            ▼
                       ERP Database
```

This allows the application to be accessed through a web browser without requiring the user's local machine to run the application.

---

# ⚙️ Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/erp-ai-agent.git
cd erp-ai-agent
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.6-luna

DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```

Do not commit `.env` to GitHub.

---

## 5. Run the application

```bash
python -m streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 🧪 Example Agent Workflow

A complex question such as:

> "Which products should we prioritize for reordering, and among those products which ones have the weakest profit margins?"

can result in the following workflow:

```text
User Question
      │
      ▼
AI Agent
      │
      ├───────────────┐
      ▼               ▼
Reorder Tool     Profitability Tool
      │               │
      ▼               ▼
Inventory Data   Margin Data
      │               │
      └───────┬───────┘
              ▼
        Cross Analysis
              │
              ▼
       Business Insight
              │
              ▼
        Final Response
```

---

# 📈 Example Output

For example, the agent can identify products such as:

```text
Multifunction Printer 92
SSD 114
Network Switch 129
Wireless Headphones 150
27-inch Monitor 34
```

and combine inventory information with sales velocity and profitability to determine which products require management attention.

The goal is not simply to return database rows, but to convert ERP data into actionable business insights.

---

# 💡 Business Value

The ERP AI Agent can help organizations:

* Reduce time spent searching ERP reports
* Make ERP data accessible to non-technical users
* Identify inventory risks earlier
* Detect profitability problems
* Analyze customer behavior
* Identify business risks
* Support management decision-making
* Automate repetitive analytical queries
* Interact with enterprise data using natural language

---

# 🔮 Future Improvements

Potential future enhancements include:

* Role-based access control
* Multi-company / multi-tenant architecture
* User authentication
* Advanced dashboards
* Automated alerts
* Sales forecasting
* Demand forecasting
* Supplier performance scoring
* Automated purchase recommendations
* Financial forecasting
* ERP API integrations
* SAP integration
* Oracle ERP integration
* Microsoft Dynamics integration
* CSV/Excel data ingestion
* Automated ETL pipelines
* Audit logging
* Query and usage monitoring
* Fine-grained database permissions

---

# 🎓 Project Learning Outcomes

This project demonstrates practical implementation of:

* AI agents
* LLM tool calling
* Function calling
* Prompt engineering
* Conversational memory
* Relational database design
* SQL analytics
* ERP business intelligence
* Data-driven decision support
* Cloud databases
* Streamlit application development
* API integration
* Environment and secret management
* Git/GitHub
* Cloud deployment

---

# 👨‍💻 Author

**Vivek Sondagar**

Computer Science / Data Science Student

### Areas of Interest

* Artificial Intelligence
* AI Agents
* Data Science
* Cybersecurity
* Enterprise Software
* Business Intelligence
* Machine Learning

---

# ⭐ Project Summary

**ERP AI Agent** demonstrates how modern AI agents can be connected to enterprise databases to transform natural-language business questions into actionable insights.

Instead of requiring users to understand SQL, database schemas, or complex ERP reporting systems, the system provides a conversational interface where users can ask questions naturally and receive data-backed business recommendations.

```text
Natural Language
       ↓
     AI Agent
       ↓
  Tool Selection
       ↓
    ERP Data
       ↓
    Analysis
       ↓
Business Insights
       ↓
Actionable Decisions
```

---

## 📜 License

This project is intended for educational, demonstration, and portfolio purposes.

Add an appropriate open-source license if you plan to distribute the source code publicly.


