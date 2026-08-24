import os
import tempfile

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_secret(name, default=None):
    """
    Use Streamlit Cloud Secrets when running on Streamlit Cloud.
    Fall back to the local .env file when running locally.
    """

    try:
        import streamlit as st

        value = st.secrets.get(name)

        if value is not None:
            return value

    except Exception:
        pass

    return os.getenv(name, default)


def get_connection():

    host = get_secret("DB_HOST")
    port = int(get_secret("DB_PORT", 3306))
    user = get_secret("DB_USER")
    password = get_secret("DB_PASSWORD")
    database = get_secret("DB_NAME")

    ssl_ca = get_secret("DB_SSL_CA")

    connection_args = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
        "connection_timeout": 15
    }

    # ---------------------------------------------------------
    # Aiven SSL
    # ---------------------------------------------------------

    if ssl_ca:

        if os.path.exists(ssl_ca):

            connection_args["ssl_ca"] = ssl_ca

        else:

            cert_file = tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".pem",
                delete=False
            )

            cert_file.write(ssl_ca)
            cert_file.close()

            connection_args["ssl_ca"] = cert_file.name

    return mysql.connector.connect(
        **connection_args
    )


def execute_query(query, params=None):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            query,
            params or ()
        )

        results = cursor.fetchall()

        return results

    finally:

        cursor.close()
        connection.close()