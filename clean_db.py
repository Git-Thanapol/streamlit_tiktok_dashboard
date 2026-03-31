import logging
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import toml
import os

# ==========================================
# 0. Logger Setup
# ==========================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_engine():
    """Reads secrets from .streamlit/secrets.toml and returns a SQLAlchemy engine."""
    try:
        secrets_path = os.path.join(".streamlit", "secrets.toml")
        if not os.path.exists(secrets_path):
            logger.error("secrets.toml not found at %s", secrets_path)
            return None
        
        secrets = toml.load(secrets_path)
        pg_secrets = secrets.get("postgresql")
        if not pg_secrets:
            logger.error("Missing [postgresql] section in secrets.toml")
            return None
            
        url_object = URL.create(
            "postgresql",
            username=pg_secrets["username"],
            password=pg_secrets["password"],
            host=pg_secrets.get("host", "localhost"),
            port=pg_secrets.get("port", 5432),
            database=pg_secrets["databasename"],
        )
        return create_engine(url_object)
    except Exception as e:
        logger.error("Failed to initialize database engine: %s", e)
        return None

def clean_database() -> None:
    """
    Connects to PostgreSQL and deletes garbage rows in the 'orders' table.
    Targets rows where 'Order ID' or 'Shipped Time' are null or empty.
    """
    engine = get_engine()
    if not engine:
        return

    try:
        with engine.connect() as conn:
            # 1. ลบแถวที่ Order ID เป็นค่าว่าง (NULL)
            res1 = conn.execute(text('DELETE FROM orders WHERE "Order ID" IS NULL'))
            logger.info("Deleted %d rows where 'Order ID' was NULL.", res1.rowcount)

            # 2. ลบแถวที่ Order ID เป็นแค่ช่องว่าง ("")
            res2 = conn.execute(text('DELETE FROM orders WHERE "Order ID" = \'\''))
            logger.info("Deleted %d rows where 'Order ID' was empty.", res2.rowcount)
            
            # 3. ลบแถวที่ Shipped Time เป็นค่าว่าง (NULL)
            res3 = conn.execute(text('DELETE FROM orders WHERE "Shipped Time" IS NULL'))
            logger.info("Deleted %d rows where 'Shipped Time' was NULL.", res3.rowcount)

            # 4. ลบแถวที่ Shipped Time เป็นแค่ช่องว่าง ("")
            res4 = conn.execute(text('DELETE FROM orders WHERE "Shipped Time" = \'\''))
            logger.info("Deleted %d rows where 'Shipped Time' was empty.", res4.rowcount)

            conn.commit()
            logger.info("Database cleanup completed successfully!")

    except Exception as e:
        logger.error("An error occurred during cleanup: %s", e)

if __name__ == "__main__":
    clean_database()
