from bs4 import BeautifulSoup
from time import sleep as wait
import re
import requests
from html.parser import HTMLParser
import xml.etree.cElementTree as etree
import pickle
TREE_LABEL_CLASS = ['CategoryTreeLabel', 'CategoryTreeLabelNs14', 'CategoryTreeLabelCategory']
VALUE_CONTENT_CLASS = "mw-category-group"
ROOT = "חברות"
HOME = "https://he.wikipedia.org"
CATEGORY_URL = "https://he.wikipedia.org/wiki" \
               "/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%94:%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA"
PERSON_URL = "https://he.wikipedia.org/wiki/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%94:%D7%90%D7%99%D7%A9%D7%99%D7%9D"
COMPANY_URL = "https://he.wikipedia.org/wiki" \
              "/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%94:%D7%97%D7%91%D7%A8%D7%95%D7%AA_%D7%9C%D7%A4%D7%99_%D7%A1%D7%95%D7%92"
CONSTRUCTIONS_URL = "https://he.wikipedia.org/wiki" \
                    "/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%94:%D7%9E%D7%91%D7%A0%D7%99%D7%9D_%D7%9C%D7%A4%D7%99_%D7%A1%D7%95%D7%92"
VALUES_ADDED = 0
ADDED_VALUES = []


# Class tree taken from stack overflow
class WikiTree:
    def __init__(self, name, link="-1"):
        self.name = name
        self.link = link
        self.children = []

    def __repr__(self):
        return self.name

    def add_child(self, node_name, node_link="-1"):
        node = WikiTree(node_name, node_link)
        self.children.append(node)


def recursive_tree_generation(tree_node):
    global VALUES_ADDED
    global ADDED_VALUES
    if tree_node.link != "-1":
        soup = BeautifulSoup(requests.get(tree_node.link).text, "lxml")
    else:
        return
    links = soup('a')
    for link in links:
        if link.get('class') == TREE_LABEL_CLASS:
            name = link.text
            if name not in ADDED_VALUES:
                ADDED_VALUES.append(name)
                link_to_child = link.get('href')
                if HOME not in link_to_child:
                    link_to_child = HOME + link_to_child
                tree_node.add_child(name, link_to_child)
            else:
                return
    divs = soup('div')
    for div in divs:
        if div.get('class'):
            if div.get('class')[0] == VALUE_CONTENT_CLASS:
                # div_string = div.tostring()
                div_links = div('a')
                if div_links:
                    for link in div_links:
                        value_name = link.text
                        if value_name not in ADDED_VALUES:
                            tree_node.add_child(value_name)
                            ADDED_VALUES.append(value_name)
                            VALUES_ADDED += 1
                            if not VALUES_ADDED % 10:
                                print("Added: " + str(VALUES_ADDED)+ " values")
                                print("Last value: " + value_name)
    for generation in tree_node.children:
        recursive_tree_generation(generation)


# recursive method for writing the tree
def write_node(node, file, depth):
    tabs = depth * "\t"
    file.write(tabs + node.name)
    file.write("\n")
    for child in node.children:
        write_node(child, file, depth + 1)


# writes the whole tree to a file
def write_tree(tree):
    with open("wikiTreeConstructions.txt", "w", encoding="utf8") as tree_file:
        write_node(tree, tree_file, 0)


def generate_tree(start_page_url, root):
    # init the tree
    category_tree = WikiTree(root,start_page_url)
    # recursive function
    recursive_tree_generation(category_tree)
    write_tree(category_tree)

generate_tree(CONSTRUCTIONS_URL, ROOT)
