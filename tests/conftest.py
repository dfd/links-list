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
def headings_to_folders_fix():
    with open(dir_path + 
            '/reference/json/good_example/headings_to_folders.json') as f:
        return json.load(f)

@pytest.fixture
def title_to_index_fix():
    with open(dir_path + 
            '/reference/json/good_example/title_to_index.json') as f:
        return json.load(f)

class JsonWrapper:
    def __init__(self, structure, links, formatting, headings_to_folders,
            title_to_index):
        self.structure = structure
        self.links = links
        self.formatting = formatting
        self.headings_to_folders = headings_to_folders
        self.title_to_index = title_to_index

@pytest.fixture(scope="module")
def jsonwrapper():
    return JsonWrapper(structure_fix(), links_fix(), formatting_fix(),
            headings_to_folders_fix(), title_to_index_fix())


