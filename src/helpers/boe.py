"""BOE XML-related utilities."""

import datetime
import re
from enum import Enum


def is_valid_diary_entry_id(entry_id: str) -> bool:
    """Check whether a string is a valid diary entry identifier.

    Valid ones are expectde to have a similar format to "BOE-A-2020-4859".
    """
    if not isinstance(entry_id, str):
        return False

    valid_id = re.compile(r'BOE-[A-Z]-\d{4}-\d+')
    if valid_id.fullmatch(entry_id):
        return True

    return False


def summary_url_for_date(date: datetime.datetime) -> str:
    """Create an URL for fetching the correspondant BOE summary.

    Refer to https://www.boe.es/datosabiertos/documentos/SumariosBOE_v_1_0.pdf
    """
    if not date:
        return None
    if not isinstance(date, datetime.datetime):
        return None

    # variable naming according to the BOE docs
    pub = 'BOE'
    i = 'S'
    date_string = date.strftime('%Y%m%d')

    return f'https://boe.es/diario_boe/xml.php?id={pub}-{i}-{date_string}'


def file_url_for_resource(resource: str) -> str:
    """Create an URL for summary entry resource such as PDF files."""
    if not resource:
        return None
    if resource.find(' ') != -1:
        return None

    url = ''.join([
        'https://www.boe.es',
        resource if resource.startswith('/') else f'/{resource}'
        ])
    return url


class SummaryXpath:
    """Xpath strings for nodes in a BOE diary summary."""

    # Accessible from the diary's root
    publication_type = '/sumario/meta/pub'
    publication_date = '/sumario/meta/fecha'
    prev_publication_date = '/sumario/meta/fechaAnt'
    next_publication_date = '/sumario/meta/fechaSig'

    sumary = '/sumario/diario/sumario_nbo'
    section = '/sumario/diario/seccion'

    # Accessible for a section
    department = './departamento'

    # Accessible for a department
    epigraf = './epigrafe'
    items = './/item'

    # Accessible for an itemType node
    item_title = './titulo'
    item_pdf_url = './urlPdf'
    item_htm_url = './urlHtm'
    item_xml_url = './urlXml'


class SummaryAttribute:
    """Available properties in BOE diary lxml elements."""

    diary_nbo = 'nbo'
    summary_nbo_id = 'id'
    section_number = 'num'
    section_name = 'nombre'
    department_name = 'nombre'
    epigraph_name = 'nombre'
    item_id = 'id'
    pdf_url_sz_bytes = 'szBytes'
    pdf_url_sz_kbytes = 'szKBytes'
    item_control = 'control'


class EntryXpath:
    """Xpath strings for nodes in a BOE entry."""

    enty_id = '/documento/metadatos/identificador'
    title = '/documento/metadatos/titulo'
    diary_number = '/documento/metadatos/diario_numero'
    section = '/documento/metadatos/seccion'
    department = '/documento/metadatos/departamento'
    entry_range = '/documento/metadatos/rango'
    initial_page = '/documento/metadatos/pagina_inicial'
    last_page = '/documento/metadatos/pagina_final'
    notes = '/documento/analisis/notas'
    topics = '/documento/analisis/materias/materia'
    alerts = '/documento/analisis/alertas/alerta'
    previous = '/documento/analisis/referencias/anteriores/anterior'
    posterior = '/documento/analisis/referencias/posteriores/posterior'
    reference_type = './palabra'
    reference_text = './texto'
    contents = '/documento/texto'
    paragraphs = '/documento/texto/p'


class EntryAttribute:
    """Available properties in BOE entry lxml elements."""

    department_code = 'codigo'
    range_code = 'codigo'
    topic_code = 'codigo'
    label_order = 'orden'
    alert_code = 'codigo'
    paragraph_class = 'parrafo'
    reference_entry_id = 'referencia'
    reference_type_code = 'codigo'


class EntryParagraphType(Enum):
    """Types of paragraphs findable on a BOE entry."""

    paragraph = 'parrafo'
    article = 'articulo'
