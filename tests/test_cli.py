import pytest
from click.testing import CliRunner
from links_list import cli
import os, shutil, glob
import json
from collections import OrderedDict

dir_path = os.path.dirname(os.path.realpath(__file__))

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
    with open('./json/project.json', 'w') as f:
        json.dump(jsonwrapper.project, f)

@pytest.mark.usefixtures("runner", "jsonwrapper")
class TestGetJson(object):

    def test_structure(self, runner, jsonwrapper):
        with runner.isolated_filesystem():
            start_project(jsonwrapper)
            structure, _, _, _ = cli.get_json()
            assert structure == jsonwrapper.structure

    def test_links(self, runner, jsonwrapper):
        with runner.isolated_filesystem():
            start_project(jsonwrapper)
            _, links, _, _ = cli.get_json()
            assert links == jsonwrapper.links

    def test_formatting(self, runner, jsonwrapper):
        with runner.isolated_filesystem():
            start_project(jsonwrapper)
            print(os.getcwd())
            _, _, formatting, _ = cli.get_json()
            assert formatting == jsonwrapper.formatting

    def test_project(self, runner, jsonwrapper):
        with runner.isolated_filesystem():
            start_project(jsonwrapper)
            print(os.getcwd())
            _, _, _, project = cli.get_json()
            assert project == jsonwrapper.project

def test_get_link_headings(jsonwrapper):
    link_headings = cli.get_link_headings(jsonwrapper.links)
    headings = set(['Dogs','Puppies','Cats','Kittens'])
    assert link_headings == headings
        
@pytest.mark.usefixtures("jsonwrapper")
class TestStructureHeadings(object):

    def test_structure(self, jsonwrapper):
        sgsh = jsonwrapper.structure_get_structure_headings
        structure_get_structure_headings, _, _, _ = cli.get_structure_headings(
                jsonwrapper.structure)
        assert structure_get_structure_headings == sgsh

    def test_structure_headings(self, jsonwrapper):
        headings = set(['Dogs','Puppies','Cats','Kittens'])
        _, structure_headings, _, _ = cli.get_structure_headings(
                jsonwrapper.structure)
        assert structure_headings == headings

    def test_headings_to_folders(self, jsonwrapper):
        htf = jsonwrapper.headings_to_folders
        _, _, headings_to_folders, _ = cli.get_structure_headings(
                jsonwrapper.structure)
        assert headings_to_folders == htf

    def test_title_to_index(self, jsonwrapper):
        tti = jsonwrapper.title_to_index
        _, _, _, title_to_index = cli.get_structure_headings(
                jsonwrapper.structure)
        assert title_to_index == tti

def setup_output():
    for f in glob.glob(dir_path + '/reference/example_output/*'):
        if os.path.isfile(f):
            shutil.copy(f, './')
        else:
            shutil.copytree(f, os.path.basename(f))


def test_delete_old_output(runner):
    with runner.isolated_filesystem():
        setup_output()
        cli.delete_old_output()
        assert not os.path.exists('README.md')
        assert not os.path.exists('./output')
        
@pytest.mark.usefixtures("jsonwrapper")
class TestCheckUrls(object):

    def test_structure(self, jsonwrapper):
        links = jsonwrapper.links
        structure = jsonwrapper.structure_get_structure_headings
        links, structure = cli.check_urls(links, structure,
                jsonwrapper.headings_to_folders, jsonwrapper.title_to_index)
        assert structure == jsonwrapper.structure_check_urls

    def test_links(self, jsonwrapper):
        links = jsonwrapper.links
        structure = jsonwrapper.structure_get_structure_headings
        links, structure = cli.check_urls(links, structure,
                jsonwrapper.headings_to_folders, jsonwrapper.title_to_index)
        assert links == jsonwrapper.links_check_urls

"""
@pytest.mark.usefixtures("jsonwrapper")
class TestGenerateOutput(object):
    
    def test_main_toc(self, jsonwrapper):
        structure = 
"""


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
