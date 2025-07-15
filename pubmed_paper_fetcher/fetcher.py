from .models import Paper
from .utils import extract_email
from typing import List
import requests
import xml.etree.ElementTree as ET

def fetch_papers(query: str, debug: bool = False) -> List[Paper]:
    if debug:
        print(f"Searching PubMed for: {query}")

    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esearch_params = {
        "db": "pubmed",
        "term": query,
        "retmax": 10,
        "retmode": "json"
    }
    esearch_resp = requests.get(esearch_url, params=esearch_params)
    esearch_resp.raise_for_status()
    id_list = esearch_resp.json()["esearchresult"]["idlist"]

    if debug:
        print(f"Found PubMed IDs: {id_list}")

    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    efetch_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"
    }
    efetch_resp = requests.get(efetch_url, params=efetch_params)
    efetch_resp.raise_for_status()

    root = ET.fromstring(efetch_resp.text)
    papers: List[Paper] = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "N/A"
        authors = []
        companies = []
        corresponding_email = ""

        for author in article.findall(".//Author"):
            affiliation = author.findtext(".//AffiliationInfo/Affiliation") or ""
            lastname = author.findtext("LastName") or ""
            firstname = author.findtext("ForeName") or ""
            name = f"{firstname} {lastname}".strip()

            if is_non_academic(affiliation):
                authors.append(name)
                companies.append(affiliation)

            if "@" in affiliation and not corresponding_email:
                corresponding_email = extract_email(affiliation)

        papers.append(
            Paper(
                pubmed_id=pmid,
                title=title,
                publication_date=pub_date,
                non_academic_authors=authors,
                company_affiliations=companies,
                corresponding_email=corresponding_email
            )
        )

    return papers

def is_non_academic(affiliation: str) -> bool:
    affiliation_lower = affiliation.lower()
    academic_words = ["university", "college", "institute", "school", "hospital", "center", "centre"]
    return not any(word in affiliation_lower for word in academic_words)
