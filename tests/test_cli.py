import pytest
from click.testing import CliRunner
from links_list import cli
import os

@pytest.fixture
def runner():
    return CliRunner()

def test_anchor():
    assert cli.anchor('title with spaces') == 'titlewithspaces'

@pytest.mark.incremental
class TestStartProject(object):

    def test_folder_creation(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            #cli.start_project()
            result = runner.invoke(cli.main, ['start_project'])
            assert result.exit_code == 0
            assert not result.exception
            assert os.path.isdir('./json')

    def test_links_file(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            #cli.start_project()
            result = runner.invoke(cli.main, ['start_project'])
            assert result.exit_code == 0
            assert not result.exception
            assert os.path.exists('./json/links.json')

    def test_structure_file(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            #cli.start_project()
            result = runner.invoke(cli.main, ['start_project'])
            assert result.exit_code == 0
            assert not result.exception
            assert os.path.exists('./json/structure.json')


@pytest.mark.usefixtures("runner", "start_project")
class TestGetJson(object):

    def test_structure(self, start_project):
        structure, _, _ = cli.get_json()
        assert structure == start_project.structure

    def test_links(self, start_project):
        _, links, _ = cli.get_json()
        assert links == start_project.links

    def test_formatting(self, start_project):
        print(os.getcwd())
        _, _, formatting = cli.get_json()
        assert formatting == start_project.formatting
"""

def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'Hello, world.'


def test_cli_with_option(runner):
    result = runner.invoke(cli.main, ['--as-cowboy'])
    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == 'Howdy, world.'


def test_cli_with_arg(runner):
    result = runner.invoke(cli.main, ['Dave'])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'Hello, Dave.'
"""
