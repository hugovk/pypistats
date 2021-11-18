import pypistats


# pytest's capsys cannot be used in a unittest class
def test__print_verbose_print(capsys) -> None:
    # Arrange
    verbose = True

    # Act
    pypistats._print_verbose(verbose, "test output")

    # Assert
    captured = capsys.readouterr()
    assert captured.err == "test output\n"
