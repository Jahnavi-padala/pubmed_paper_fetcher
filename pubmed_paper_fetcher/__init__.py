"""
pubmed_paper_fetcher - Fetch PubMed papers authored by non-academic authors.
"""

__version__ = "0.1.0"

from .cli import app
from .fetcher import fetch_papers

__all__ = ["app", "fetch_papers"]
