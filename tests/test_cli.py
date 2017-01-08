import pytest
from click.testing import CliRunner
from links_list import cli
import os
import json

@pytest.fixture
def runner():
    return CliRunner()

def test_anchor():
    assert cli.anchor('title with spaces') == 'titlewithspaces'

@pytest.mark.incremental
@pytest.mark.usefixtures("runner")
class TestStartProject(object):

    def test_folder_creation(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli.main, ['start_project'])
            assert result.exit_code == 0
            assert not result.exception
            assert os.path.isdir('./json')

    def test_links_file(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli.main, ['start_project'])
            assert result.exit_code == 0
            assert not result.exception
            assert os.path.exists('./json/links.json')

    def test_structure_file(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(cli.main, ['start_project'])
            assert result.exit_code == 0
            assert not result.exception
            assert os.path.exists('./json/structure.json')

def start_project(jsonwrapper):
    print(os.getcwd())
    os.mkdir('./json')
    with open('./json/structure.json', 'w') as f:
        json.dump(jsonwrapper.structure, f)
    with open('./json/links.json', 'w') as f:
        json.dump(jsonwrapper.links, f)
    with open('./json/formatting.json', 'w') as f:
        json.dump(jsonwrapper.formatting, f)

@pytest.mark.usefixtures("runner", "jsonwrapper")
class TestGetJson(object):

    def test_structure(self, runner, jsonwrapper):
        with runner.isolated_filesystem():
            start_project(jsonwrapper)
            structure, _, _ = cli.get_json()
            assert structure == jsonwrapper.structure

    def test_links(self, runner, jsonwrapper):
        with runner.isolated_filesystem():
            start_project(jsonwrapper)
            _, links, _ = cli.get_json()
            assert links == jsonwrapper.links

    def test_formatting(self, runner, jsonwrapper):
        with runner.isolated_filesystem():
            start_project(jsonwrapper)
            print(os.getcwd())
            _, _, formatting = cli.get_json()
            assert formatting == jsonwrapper.formatting

def test_get_link_headings(jsonwrapper):
    link_headings = cli.get_link_headings(jsonwrapper.links)
    headings = set(['Dogs','Puppies','Cats','Kittens'])
    assert link_headings == headings
        
@pytest.mark.usefixtures("jsonwrapper")
class TestStructureHeadings(object):

    def test_structure_headings(self, jsonwrapper):
        headings = set(['Dogs','Puppies','Cats','Kittens'])
        structure_headings, _, _ = cli.get_structure_headings(
                jsonwrapper.structure)
        assert structure_headings == headings

    def test_headings_to_folders(self, jsonwrapper):
        htf = {'Dogs':'Dog Photos', 'Puppies':'Dog Photos', 
                'Cats':'Cat Photos', 'Kittens':'Cat Photos'}
        _, headings_to_folders, _ = cli.get_structure_headings(
                jsonwrapper.structure)
        assert headings_to_folders == htf

    def test_title_to_index(self, jsonwrapper):
        tti = {'Cat Photos':0, 'Dog Photos':1}
        _, _, title_to_index = cli.get_structure_headings(
                jsonwrapper.structure)
        assert title_to_index == tti
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
