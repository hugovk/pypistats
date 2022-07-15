"""
Unit tests for pypistats cache
"""
import tempfile
from pathlib import Path

import respx
from freezegun import freeze_time

import pypistats


class TestPypiStatsCache:
    def setup_method(self) -> None:
        # Choose a new cache dir that doesn't exist
        self.original_cache_dir = pypistats.CACHE_DIR
        self.temp_dir = tempfile.TemporaryDirectory()
        pypistats.CACHE_DIR = Path(self.temp_dir.name) / "pypistats"

    def teardown_method(self) -> None:
        # Reset original
        pypistats.CACHE_DIR = self.original_cache_dir

    @freeze_time("2018-12-26")
    def test__cache_filename(self) -> None:
        # Arrange
        url = "https://pypistats.org/api/packages/pip/recent"

        # Act
        out = pypistats._cache_filename(url)

        # Assert
        assert str(out).endswith(
            "2018-12-26-https-pypistats-org-api-packages-pip-recent.json"
        )

    def test__load_cache_not_exist(self) -> None:
        # Arrange
        filename = Path("file-does-not-exist")

        # Act
        data = pypistats._load_cache(filename)

        # Assert
        assert data == {}

    def test__load_cache_bad_data(self) -> None:
        # Arrange
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"Invalid JSON!")

        # Act
        data = pypistats._load_cache(Path(f.name))

        # Assert
        assert data == {}

    def test_cache_round_trip(self) -> None:
        # Arrange
        filename = pypistats.CACHE_DIR / "test_cache_round_trip.json"
        data = "test data"

        # Act
        pypistats._save_cache(filename, data)
        new_data = pypistats._load_cache(filename)

        # Tidy up
        filename.unlink()

        # Assert
        assert new_data == data

    def test__clear_cache(self) -> None:
        # Arrange
        # Create old cache file
        cache_file = pypistats.CACHE_DIR / "2018-11-26-old-cache-file.json"
        pypistats._save_cache(cache_file, data={})
        assert cache_file.exists()

        # Act
        pypistats._clear_cache()

        # Assert
        assert not cache_file.exists()

    @respx.mock
    def test_subcommand_with_cache(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/overall"
        mocked_response = """{
          "data": [
            {"category": "without_mirrors", "date": "2018-11-01", "downloads": 2295765}
          ],
          "package": "pip",
          "type": "overall_downloads"
        }"""
        expected_output = """
| category        | downloads |
|:----------------|----------:|
| without_mirrors | 2,295,765 |

Date range: 2018-11-01 - 2018-11-01
"""

        # Act
        respx.get(mocked_url).respond(content=mocked_response)
        # First time to save to cache
        pypistats.overall(package)
        # Second time to read from cache
        output = pypistats.overall(package, format="md")

        # Assert
        assert output.strip() == expected_output.strip()
