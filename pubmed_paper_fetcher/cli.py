import typer
from .fetcher import fetch_papers
import pandas as pd

app = typer.Typer()

@app.command()
def main(
    query: str,
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output"),
    file: str = typer.Option(None, "--file", "-f", help="Output CSV file name")
):
    """
    Fetch PubMed papers for the given QUERY.
    """
    papers = fetch_papers(query, debug=debug)

    rows = []
    for p in papers:
        rows.append({
            "PubmedID": p.pubmed_id,
            "Title": p.title,
            "Publication Date": p.publication_date,
            "Non-academic Author(s)": "; ".join(p.non_academic_authors),
            "Company Affiliation(s)": "; ".join(p.company_affiliations),
            "Corresponding Author Email": p.corresponding_email,
        })

    df = pd.DataFrame(rows)
    if file:
        df.to_csv(file, index=False)
        typer.echo(f"✅ Results saved to {file}")
    else:
        typer.echo(df)

if __name__ == "__main__":
    app()
