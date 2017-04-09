import click
import os
import glob
import shutil
import json
from urllib.request import urlopen, Request
from collections import OrderedDict
import copy

dir_path = os.path.dirname(os.path.realpath(__file__))
output_dir = '.'

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
    structure = copy.deepcopy(structure)
    structure_headings = set([])
    headings_to_folders = {}
    title_to_index = {}
    for idx, folder in enumerate(structure):
        a = []
        for heading in folder['headings']:
            #print(folder)
            headings_to_folders[heading] = folder['title']
            structure_headings.add(heading)
            title_to_index[folder['title']] = idx
            a.append({heading:[]})
        folder['headings'] = a
    print(structure)
    return structure, structure_headings, headings_to_folders, title_to_index

def delete_old_output():
    shutil.rmtree('./output')
    os.remove('README.md')

def check_urls(links, structure, headings_to_folders, title_to_index):
    structure = copy.deepcopy(structure)
    links = copy.deepcopy(links)
    max_err = 5
    for link in links:
        url_err = True
        attempts = 0
        while url_err and attempts < max_err:
            if attempts > 1:
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
                list_of_headings = structure[title_to_index[headings_to_folders[
                    tag]]]['headings']
                for heading in list_of_headings:
                    if tag in heading.keys():
                        heading[tag].append(link)
    return links, structure


def generate_output(structure, formatting, project):
    with open(output_dir + "/README.md","a+") as toc:
        toc.write(formatting['main title'] + " " + project['title'] + " \n")
        toc.write(formatting['description'] + " \n")
        toc.write(formatting['headings'] + " Table of Contents  \n")
        for folder, item in structure.items():
            toc.write(formatting['toc headings'] + " [" + item['title'] + "](./" + folder + ")  \n")
            new_folder = output_dir + "/" + folder
            os.mkdir(new_folder)
            with open(new_folder + "/README.md","a+") as f:
                f.write(formatting['main title'] + " " + item['title'] + '  \n')
                f.write(formatting['toc headings'] + " Local Table of Contents  \n")
                f.write("[(Back to Master Table of Contents)](../)  \n")
                for heading in item['headings'].keys():
                    f.write("[" + heading + "](" + formatting['main title'] + " " + anchor(heading) + ")  \n")
                for heading, hlinks in item['headings'].items():
                    toc.write("[" + heading + "](" + folder + "#" + anchor(heading)
                            + ")  \n")
                    f.write(formatting['headings'] + " <a name=\"" + anchor(heading) + "\"></a>" + 
                            heading + "  \n\n")
                    for link in hlinks:
                        f.write("[" + link['title'] + "](" + link['url'] + ")")
                        if link['url_err']:
                            f.write(" (URL Failure)")
                        f.write("  \n")
                        if 'author' in link:
                            f.write("by " + link['author'] + "  \n")
                        f.write(link['description'] + "  \n")
                        if len(link['tags']) > 1:
                            f.write("Other tags: " )
                            tags = link['tags'][:]
                            tags.remove(heading)
                            for tag in tags[:-1]:
                               f.write("[" + tag + "](../" + headings_to_folders[tag] + "#" + anchor(tag) + "), ")
                            f.write("[" + tags[-1] + "](../" + headings_to_folders[tags[-1]] + "#" + anchor(tags[-1]) + ") ")
                            f.write("  \n")
                        f.write("  \n")


def print_results():
    pass

@main.command()
def generate():
    """Generate markdown list of links from json
    """
    structure, links, formatting, project = get_json()
    link_headings = get_link_headings(links)
    structure, structure_headings, headings_to_folders, title_to_index = \
            get_structure_headings(structure)
    delete_old_output()
    links, structure = check_urls(links, structure, headings_to_folders, title_to_index)
    generate_output(structure, formatting, project)
    print_results(links, link_headings, structure_headings)
