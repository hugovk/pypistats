"""
Unit tests for cache
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import mock

from freezegun import freeze_time

import pypistats
from pypistats import _cache

from .test_pypistats import mock_urllib3_response


class TestCache:
    def setup_method(self) -> None:
        # Choose a new cache dir that doesn't exist
        self.original_cache_dir = _cache.CACHE_DIR
        self.temp_dir = tempfile.TemporaryDirectory()
        _cache.CACHE_DIR = Path(self.temp_dir.name) / "pypistats"

    def teardown_method(self) -> None:
        # Reset original
        _cache.CACHE_DIR = self.original_cache_dir

    @freeze_time("2018-12-26")
    def test__cache_filename(self) -> None:
        # Arrange
        url = "https://pypistats.org/api/packages/pip/recent"

        # Act
        out = _cache.filename(url)

        # Assert
        assert str(out).endswith(
            "2018-12-26-https-pypistats-org-api-packages-pip-recent.json"
        )

    def test_load_cache_not_exist(self) -> None:
        # Arrange
        filename = Path("file-does-not-exist")

        # Act
        data = _cache.load(filename)

        # Assert
        assert data == {}

    def test_load_cache_bad_data(self) -> None:
        # Arrange
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"Invalid JSON!")

        # Act
        data = _cache.load(Path(f.name))

        # Assert
        assert data == {}

    def test_cache_round_trip(self) -> None:
        # Arrange
        filename = _cache.CACHE_DIR / "test_cache_round_trip.json"
        data = {"test": "data"}

        # Act
        _cache.save(filename, data)
        new_data = _cache.load(filename)

        # Tidy up
        filename.unlink()

        # Assert
        assert new_data == data

    def test_cache_clear(self) -> None:
        # Arrange
        # Create old cache file
        cache_file = _cache.CACHE_DIR / "2018-11-26-old-cache-file.json"
        _cache.save(cache_file, data={})
        assert cache_file.exists()

        # Act
        _cache.clear()

        # Assert
        assert not cache_file.exists()

    @mock.patch("urllib3.request")
    def test_subcommand_with_cache(self, mock_request) -> None:
        # Arrange
        package = "pip"
        mocked_response = """{
          "data": [
            {"category": "without_mirrors", "date": "2018-11-01", "downloads": 2295765}
          ],
          "package": "pip",
          "type": "overall_downloads"
        }"""
        expected_output = """
| category        | downloads |
| :---------------|---------: |
| without_mirrors | 2,295,765 |

Date range: 2018-11-01 - 2018-11-01
"""

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        # First time to save to cache
        pypistats.overall(package)
        # Second time to read from cache
        output = pypistats.overall(package, format="md")

        # Assert
        assert output.strip() == expected_output.strip()
