from typing import Dict, Generator, Iterable
import datetime
import collections
import functools
from lxml import etree as et
import httplib2

from . import helpers
from . import boe

def get_sections(tree) -> Generator:
    sections = ((section.get(boe.SummaryAttribute.section_number), section)
            for section
            in helpers.use_tree_for_search(tree)(boe.SummaryXpath.section))
    
    return sections

def get_departments_per_section(sections) -> Generator:
    departments = (
            (section_number, department.get(boe.SummaryAttribute.department_name), department)
            for (section_number, section)
            in sections
            for department
            in helpers.use_tree_for_search(section)(boe.SummaryXpath.department))
    
    return departments

def get_items_per_department(departments) -> Generator:
    items = ((section_number, department_name, item)
        for (section_number, department_name, department)
        in departments
        for item
        in helpers.use_tree_for_search(department)(boe.SummaryXpath.items))
    
    return items

def get_item_details(section_number:str, department_name:str, node) -> Dict:
    search_details = helpers.use_tree_for_search(node)
    title_node = search_details(boe.SummaryXpath.item_title)[0]
    pdf_url_node = search_details(boe.SummaryXpath.item_pdf_url)[0]
    xml_url_node = search_details(boe.SummaryXpath.item_xml_url)[0]
    htm_url_node = search_details(boe.SummaryXpath.item_htm_url)[0]
    
    parent = node.getparent()
    is_epigraph = parent.tag.lower() == 'epigrafe'
    epigraph = parent = parent.get(boe.SummaryAttribute.epigraph_name) if is_epigraph else ''
    
    details = {}
    details['id'] = node.get(boe.SummaryAttribute.item_id)
    details['epigraph'] = epigraph
    details['section'] = section_number
    details['department'] = department_name
    details['title'] = title_node.text
    details['pdf_url'] = pdf_url_node.text
    details['xml_url'] = xml_url_node.text
    details['htm_url'] = htm_url_node.text
    
    return details

def get_details_per_item(items) -> Generator:
    details = (get_item_details(*item) for item in items)
    
    return details

