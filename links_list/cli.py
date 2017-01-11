import click
import os
import glob
import shutil
import json
from urllib.request import urlopen, Request
from collections import OrderedDict

dir_path = os.path.dirname(os.path.realpath(__file__))

def anchor(heading):
    """Removes spaces from string

    :param heading: string to remove spaces from

    :return: string with spaces removed
    """
    return heading.replace(" ", "")


#@click.option('--verbose', '-v', is_flag=True, help='Provide verbose output')
@click.group()
def main():
    """Main command for links-list"""
    pass

@main.command()
def start_project():
    """Create project folder
    """
    os.mkdir('./json')
    click.echo('Created json directory.')
    for f in glob.glob(dir_path + '/reference/*'):
        shutil.copy(f, './json')
        click.echo('Copied ' + f)

def read_json(location):
    print(os.getcwd())
    with open(location) as data_file:
        return json.load(data_file)

def get_json():
    json_dir = './json/'
    structure = read_json(json_dir + 'structure.json')
    links = read_json(json_dir + 'links.json')
    formatting = read_json('./json/formatting.json')
    project = read_json('./json/project.json')
    return structure, links, formatting, project

def get_link_headings(links):
    link_headings = set([])
    for link in links:
        for tag in link['headings']:
            link_headings.add(tag)
    return link_headings

def get_structure_headings(structure):
    structure_headings = set([])
    headings_to_folders = {}
    title_to_index = {}
    for idx, folder in enumerate(structure):
        a = OrderedDict()
        for heading in folder['headings']:
            headings_to_folders[heading] = folder['title']
            structure_headings.add(heading)
            title_to_index[folder['title']] = idx
            a[heading] = []
        folder['headings'] = a
    return structure_headings, headings_to_folders, title_to_index

def delete_old_output():
    shutil.rmtree('./output')
    os.remove('README.md')

def check_urls(links, structure, headings_to_folders, title_to_index):
    max_err = 5
    for link in links:
        url_err = True
        attempts = 0
        while url_err and attempts < 5:
            if attempts > 1:
                print("attempt:", attempts, link['url'])
            attempts += attempts
            try:
                req = Request(link['url'], 
                        headers={'User-Agent' : "Magic Browser"})
                res = urlopen(req)
                if res.status != 200:
                    url_err = True
                else:
                    url_err = False
            except HTTPException:
                url_err = True
                click.echo("HTTPException for " + link['url'])
            except URLError:
                url_err = True
                click.echo("URLError for " + link['url'])
            link['url_err'] = url_err
            for tag in link['headings']:
                structure[title_to_index[headings_to_folders[tag]]
                        ]['headings'][tag].append(link)



def generate_output(links, structure, formatting, project):
    pass

def print_results():
    pass

@main.command()
def generate():
    """Generate markdown list of links from json
    """
    structure, links, formatting, project = get_json()
    link_headings = get_link_headings(links)
    structure_headings, headings_to_folders, title_to_index = \
            get_structure_headings(structure)
    delete_old_output()
    check_urls(links)
    generate_output(links, structure, formatting, project)
    print_results(links, link_headings, structure_headings)
