import pytest
import os, shutil, glob
from click.testing import CliRunner
import json

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
    structure = [
            {
                "headings": [
                    "Kittens",
                    "Cats"
                ],
                "title": "Cat Photos"
            },
            {
                "headings": [
                    "Puppies",
                    "Dogs"
                ],
                "title": "Dog Photos"
            }
        ]
    return structure

@pytest.fixture
def links_fix():
    links = [
            {
                "author": "Amanda",
                "description": "\"Your Recommended Daily Allowance of Puppies\"",
                "headings": [
                    "Puppy"
                ],
                "title": "The Daily Puppy",
                "url": "http://www.dailypuppy.com/"
            },
            {
                "author": "Pexels",
                "description": "\"Browse a wide range of dog images and find high quality and professional pictures you can use for free. You can find photos of bulldogs, retrievers, beagles and of course puppies. Also have a look at our pictures of pets and cats.\"",
                "headings": [
                    "Dogs"
                ],
                "title": "Dog Images",
                "url": "https://www.pexels.com/search/dog/"
            },
            {
                "author": "Chelsea Marshall",
                "description": "\"The whole internet has led up to this crucial moment.\"",
                "headings": [
                    "Kittens"
                ],
                "title": "The 100 Most Important Kitten Photos Of All Time",
                "url": "https://www.buzzfeed.com/chelseamarshall/best-kitten-pictures?utm_term=.kieR4bQpwG#.xyA4JZEVx3"
            },
            {
                "author": "Reddit",
                "description": "\"This is subreddit is only for cat pictures, so yeah... Keep your paws off it if you want to post something else.\"",
                "headings": [
                    "Cats"
                ],
                "title": "r/CatPictures",
                "url": "https://www.reddit.com/r/catpictures/"
            },
            {
                "author": "Awkward Family Photos",
                "description": "Awkward family photos featuring pets.",
                "headings": [
                    "Dogs",
                    "Cats"
                ],
                "title": "Awkward Family Pet Photos",
                "url": "http://awkwardfamilyphotos.com/category/photos/pets-2/"
            }
        ]
    return links

@pytest.fixture
def formatting_fix():
    formatting = {
            "main title": "#",
            "headings": "##",
            "toc headings": "###",
            "link title": "",
            "author": "",
            "description": "",
            "tags": ""
        }
    return formatting


class JsonWrapper:
    def __init__(self, structure, links, formatting):
        self.structure = structure
        self.links = links
        self.formatting = formatting

#@pytest.fixture(scope="module")
#def jsonwrapper():
#    return JsonWrapper(structure_fix, links_fix)
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

@pytest.fixture(scope="function")
def start_project(structure_fix, links_fix, formatting_fix):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir('./json')
        with open('./json/structure.json', 'w') as f:
            json.dump(structure_fix, f)
        with open('./json/links.json', 'w') as f:
            json.dump(links_fix, f)
        with open('./json/formatting.json', 'w') as f:
            json.dump(formatting_fix, f)
        #json.dump({}, f)
    return JsonWrapper(structure_fix, links_fix, formatting_fix)
