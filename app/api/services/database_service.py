import sqlite3
import duckdb
from typing import List, Dict, Any
import pandas as pd
from app.config import settings

class DatabaseService:
    def __init__(self):
        self.data_dir = settings.DATA_DIR

    def execute_sqlite_query(self, db_path: str, query: str) -> List[Dict[str, Any]]:
        """Execute a query on a SQLite database."""
        full_path = os.path.join(self.data_dir, db_path.lstrip('/'))
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Database not found: {db_path}")

        with sqlite3.connect(full_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results]

    def execute_duckdb_query(self, query: str, input_files: List[str] = None) -> pd.DataFrame:
        """Execute a query using DuckDB, optionally loading input files."""
        conn = duckdb.connect(database=':memory:')
        
        if input_files:
            for file in input_files:
                full_path = os.path.join(self.data_dir, file.lstrip('/'))
                table_name = os.path.splitext(os.path.basename(file))[0]
                if file.endswith('.csv'):
                    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{full_path}')")
                elif file.endswith('.parquet'):
                    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{full_path}')")

        result = conn.execute(query).fetchdf()
        conn.close()
        return result

    def calculate_ticket_sales(self, db_path: str, ticket_type: str) -> float:
        """Calculate total sales for a specific ticket type."""
        query = """
        SELECT SUM(units * price) as total_sales
        FROM tickets
        WHERE type = ?
        """
        
        full_path = os.path.join(self.data_dir, db_path.lstrip('/'))
        with sqlite3.connect(full_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (ticket_type,))
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0.0

database_service = DatabaseService()