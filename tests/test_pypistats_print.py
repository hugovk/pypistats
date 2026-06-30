from __future__ import annotations

import pypistats


# pytest's capsys cannot be used in a unittest class
def test__print_verbose_print(capsys, monkeypatch) -> None:
    # Arrange
    monkeypatch.setattr(pypistats, "_verbose", True)

    # Act
    pypistats._print_verbose("test output")

    # Assert
    captured = capsys.readouterr()
    assert captured.err == "test output\n"
