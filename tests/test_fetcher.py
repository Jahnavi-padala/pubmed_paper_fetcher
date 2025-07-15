from pubmed_paper_fetcher import fetcher

def test_is_non_academic():
    assert fetcher.is_non_academic("Google Inc.") is True
    assert fetcher.is_non_academic("Stanford University") is False
