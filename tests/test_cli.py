from typer.testing import CliRunner
from pubmed_paper_fetcher.cli import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Fetch PubMed papers" in result.output
