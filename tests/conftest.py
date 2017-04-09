import pytest
import os, shutil, glob
from click.testing import CliRunner
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item

def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" %previousfailed.name)

@pytest.fixture
def structure_fix():
    with open(dir_path + '/reference/json/good_example/structure.json') as f:
        return json.load(f)

@pytest.fixture
def links_fix():
    with open(dir_path + '/reference/json/good_example/links.json') as f:
        return json.load(f)

@pytest.fixture
def formatting_fix():
    with open(dir_path + '/reference/json/good_example/formatting.json') as f:
        return json.load(f)

@pytest.fixture
def project_fix():
    with open(dir_path + '/reference/json/good_example/project.json') as f:
        return json.load(f)

@pytest.fixture
def headings_to_folders_fix():
    with open(dir_path + 
            '/reference/json/good_example/headings_to_folders.json') as f:
        return json.load(f)

@pytest.fixture
def title_to_index_fix():
    with open(dir_path + 
            '/reference/json/good_example/title_to_index.json') as f:
        return json.load(f)

@pytest.fixture
def structure_get_structure_headings():
    with open(dir_path + 
            '/reference/json/good_example/structure_get_structure_headings.json') as f:
        return json.load(f)

@pytest.fixture
def structure_check_urls():
    with open(dir_path + 
            '/reference/json/good_example/structure_check_urls.json') as f:
        return json.load(f)

@pytest.fixture
def links_check_urls():
    with open(dir_path + 
            '/reference/json/good_example/links_check_urls.json') as f:
        return json.load(f)

class JsonWrapper:
    def __init__(self, structure, links, formatting, project, 
            headings_to_folders,
            title_to_index,
            structure_get_structure_headings,
            structure_check_urls,
            links_check_urls):
        self.structure = structure
        self.links = links
        self.formatting = formatting
        self.project= project
        self.headings_to_folders = headings_to_folders
        self.title_to_index = title_to_index
        self.structure_get_structure_headings = structure_get_structure_headings
        self.structure_check_urls = structure_check_urls
        self.links_check_urls = links_check_urls

@pytest.fixture(scope="module")
def jsonwrapper():
    return JsonWrapper(structure_fix(), links_fix(), formatting_fix(), 
            project_fix(), headings_to_folders_fix(), title_to_index_fix(),
            structure_get_structure_headings(), structure_check_urls(),
            links_check_urls())


