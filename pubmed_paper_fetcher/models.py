from dataclasses import dataclass
from typing import List

@dataclass
class Paper:
    pubmed_id: str
    title: str
    publication_date: str
    non_academic_authors: List[str]
    company_affiliations: List[str]
    corresponding_email: str
