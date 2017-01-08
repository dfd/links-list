import click
import os
import glob
import shutil
import json

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
    #formatting = []
    return structure, links, formatting

def get_link_headings(links):
    link_headings = set([])
    for link in links:
        for tag in link['headings']:
            link_headings.add(tag)
    return link_headings

def get_structure_headings(structure):
    pass

def delete_old_output():
    pass

def check_urls(links):
    pass

def generate_output(links, structure, formatting):
    pass

def print_results():
    pass

@main.command()
def generate():
    """Generate markdown list of links from json
    """
    structure, links, formatting = get_json()
    link_headings = get_link_headings(links)
    headings_to_folders, structure_headings = get_structure_headings(structure)
    delete_old_output()
    links = check_urls(links)
    generate_output(links, structure, formatting)
    print_results(links, link_headings, structure_headings)
