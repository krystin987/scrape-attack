import fetch_rss_data

class TestClass:
    
    def test_rss(self):
        posts = fetch_rss_data.fetch_url("tests")
        assert isinstance(posts, list)