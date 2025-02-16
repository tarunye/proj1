import pytest
from app.services.file_service import file_service
from app.services.database_service import database_service
from app.services.llm_service import llm_service
import os
import json
import sqlite3
from pathlib import Path

# Create test data directory
TEST_DATA_DIR = Path("test_data")
TEST_DATA_DIR.mkdir(exist_ok=True)

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup
    os.environ["DATA_DIR"] = str(TEST_DATA_DIR)
    
    yield
    
    # Teardown
    for file in TEST_DATA_DIR.glob("*"):
        file.unlink()
    TEST_DATA_DIR.rmdir()

class TestFileService:
    def test_read_write_file(self):
        content = "Test content"
        file_service.write_file("test.txt", content)
        
        result = file_service.read_file("test.txt")
        assert result == content

    def test_safe_path_validation(self):
        with pytest.raises(ValueError):
            file_service.read_file("../outside.txt")

    def test_extract_markdown_titles(self):
        # Create test markdown files
        (TEST_DATA_DIR / "docs").mkdir(exist_ok=True)
        (TEST_DATA_DIR / "docs" / "test.md").write_text("# Test Title\nContent")
        
        titles = file_service.extract_markdown_titles("docs")
        assert titles == {"test.md": "Test Title"}

class TestDatabaseService:
    @pytest.fixture
    def setup_test_db(self):
        db_path = TEST_DATA_DIR / "test.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE tickets (
                type TEXT,
                units INTEGER,
                price REAL
            )
        """)
        
        cursor.execute("INSERT INTO tickets VALUES (?, ?, ?)", ("Gold", 2, 100.0))
        conn.commit()
        conn.close()
        
        return "test.db"

    def test_calculate_ticket_sales(self, setup_test_db):
        total = database_service.calculate_ticket_sales(setup_test_db, "Gold")
        assert total == 200.0

class TestLLMService:
    @pytest.mark.asyncio
    async def test_get_completion(self):
        response = await llm_service.get_completion("What is 2+2?")
        assert isinstance(response, str)
        assert len(response) > 0

    @pytest.mark.asyncio
    async def test_get_embeddings(self):
        texts = ["Hello", "World"]
        embeddings = await llm_service.get_embeddings(texts)
        assert len(embeddings) == 2
        assert len(embeddings[0]) > 0