import os
from typing import List, Dict, Any
import json
import numpy as np
from datetime import datetime
import pandas as pd

class Helpers:
    @staticmethod
    def find_most_similar_pair(texts: List[str]) -> tuple[str, str]:
        """Find the most similar pair of texts using cosine similarity of embeddings."""
        from app.services.llm_service import llm_service
        
        # Get embeddings for all texts
        embeddings = llm_service.get_embeddings(texts)
        
        # Calculate pairwise similarities
        max_similarity = -1
        most_similar_pair = None
        
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                similarity = np.dot(embeddings[i], embeddings[j])
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_pair = (texts[i], texts[j])
        
        return most_similar_pair

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Parse a date string in various formats."""
        formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%m-%d-%Y"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse date: {date_str}")

    @staticmethod
    def convert_markdown_to_html(markdown_content: str) -> str:
        """Convert markdown to HTML using a simple implementation."""
        import re
        
        # Convert headers
        markdown_content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', markdown_content, flags=re.M)
        markdown_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', markdown_content, flags=re.M)
        
        # Convert bold and italic
        markdown_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', markdown_content)
        markdown_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', markdown_content)
        
        # Convert links
        markdown_content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown_content)
        
        # Convert lists
        markdown_content = re.sub(r'^\- (.*?)$', r'<li>\1</li>', markdown_content, flags=re.M)
        markdown_content = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', markdown_content, flags=re.S)
        
        return markdown_content

helpers = Helpers()