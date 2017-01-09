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


class JsonWrapper:
    def __init__(self, structure, links, formatting):
        self.structure = structure
        self.links = links
        self.formatting = formatting

@pytest.fixture(scope="module")
def jsonwrapper():
    return JsonWrapper(structure_fix(), links_fix(), formatting_fix())

"""
@pytest.fixture(scope="function")
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        return runner
        #yield runner
        
        for the_file in os.listdir('./'):
            file_path = os.path.join('./', the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        """
"""
@pytest.fixture(scope="function")
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        for the_file in os.listdir('./'):
            file_path = os.path.join('./', the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        return runner
   """     

@pytest.fixture(scope="function")
def start_project(structure_fix, links_fix, formatting_fix):
    #runner = CliRunner()
    #with runner.isolated_filesystem():
    print(os.getcwd())
    os.mkdir('./json')
    with open('./json/structure.json', 'w') as f:
        json.dump(structure_fix, f)
    with open('./json/links.json', 'w') as f:
        json.dump(links_fix, f)
    with open('./json/formatting.json', 'w') as f:
        json.dump(formatting_fix, f)
        #json.dump({}, f)
    return JsonWrapper(structure_fix, links_fix, formatting_fix)
