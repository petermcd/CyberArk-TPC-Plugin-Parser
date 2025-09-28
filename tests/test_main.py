"""Tests for main.py"""
from src.main import main

class TestMain(object):
    """Tests for main.py"""
    def test_main(self, capsys):
        """Test the main function"""
        main()
        captured = capsys.readouterr()
        assert captured.out == "Package is running...\n"
