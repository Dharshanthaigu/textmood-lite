import subprocess
import sys


def test_cli_outputs_mood():
    result = subprocess.run(
        [sys.executable, "-m", "textmood_lite.cli", "I am happy and excited"],
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "happy"


# def test_cli_no_args_shows_usage():
#     result = subprocess.run(
#         [sys.executable, "-m", "textmood_lite.cli"], capture_output=True, rext=True
#     )
#     assert result.stdout.strip() == "happy"


def test_cli_detailed_flag():
    result = subprocess.run(
        [sys.executable, "-m", "textmood_lite.cli", "I am happy", "--detailed"],
        capture_output=True,
        text=True,
    )
    assert "happy" in result.stdout
    assert "sad" in result.stdout


def test_cli_no_args_exists_with_error():
    result = subprocess.run(
        [sys.executable, "-m", "textmoode_lite.cli"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


# def test_cli_no_args_shows_usage():
#     result = subprocess.run(
#         [sys.executable, "-m", "textmood_lite.cli"],
#         capture_output=True,
#         text=True,
#     )
#     assert result.returncode == 1
#     assert "Usage" in result.stdout
