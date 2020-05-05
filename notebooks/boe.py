import datetime
from enum import Enum

def summary_url_for_date(date: datetime.datetime) -> str:
    '''Create an URL for fetching the correspondant BOE summary.
    Refer to https://www.boe.es/datosabiertos/documentos/SumariosBOE_v_1_0.pdf
    '''
    
    pub = 'BOE'
    I = 'S'
    date_string = date.strftime('%Y%m%d')
    
    return f'https://boe.es/diario_boe/xml.php?id={pub}-{I}-{date_string}'

def file_url_for_resource(resource: str) -> str:
    '''Create an URL for summary entry resource such as PDF files.'''
    
    return f'https://www.boe.es{resource}'

class SummaryXpath:
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
    previous = '/documento/analisis/referencia/anteriores/anterior'
    contents = '/documento/texto'
    paragraphs = '/documento/texto/p'

class EntryAttribute:
    department_code = 'codigo'
    range_code = 'codigo'
    topic_code = 'codigo'
    label_order = 'orden'
    alert_code = 'codigo'
    previous_reference = 'referencia'
    paragraph_class = 'parrafo'
    
class EntryParagraphType(Enum):
    paragraph = 'parrafo'
    article = 'articulo'
    