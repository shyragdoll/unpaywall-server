import re
import httpx
import difflib

unpaywallMap = {
    'Wiley': 'wiley',
    'Institution of Engineering and Technology (IET)': 'iet',
    'Oxford University Press (OUP)': 'oxford',
    'American Medical Association (AMA)': 'jamanetwork',
    'BMJ': 'bmj',
    'Optica Publishing Group': 'osa',
    'SPIE': 'spie',
    'Institute of Electrical and Electronics Engineers (IEEE)': 'ieee',
    'American Society of Hematology': 'ash',
    'American Physiological Society': 'physiology',
    'Cambridge University Press': 'cambridge',
    'Royal Society of Chemistry (RSC)': 'rsc',
    'American Association for the Advancement of Science (AAAS)': 'aaas',
    'BENTHAM SCIENCE PUBLISHERS': 'bentham',
    'American Society for Microbiology': 'asm',
    'American Society of Clinical Oncology (ASCO)': 'asco',
    'Association for Computing Machinery (ACM)': 'acm',
    'American Association for Cancer Research (AACR)': 'aacr',
    'Emerald Publishing Limited': 'emerald',
    'CSIRO Publishing': 'csiro',
    'European Respiratory Society': 'ers',
    'Rockefeller University Press': 'rupress',
    'American Psychological Association (APA)': 'apa',
    'PUBLISHED BY IMPERIAL COLLEGE PRESS AND DISTRIBUTED BY WORLD SCIENTIFIC PUBLISHING CO.': 'worldscientific',
    'Bioscientifica': 'bioscientifica',
    'Cold Spring Harbor Laboratory': 'csh',
    'Baishideng Publishing Group Inc.': 'baishideng',
    'American Physical Society (APS)': 'aps',
    'China Science Publishing & Media Ltd.': 'sciengine',
    'Physicians Postgraduate Press, Inc': 'ppp',
    'Edizioni Minerva Medica': 'minervamedica',
    'Academy of Management': 'aom',
    'American Economic Association': 'aea',
    'American Chemical Society': 'acs',
    'Association for Research in Vision and Ophthalmology (ARVO)': 'arvo',
    'American Institute of Aeronautics and Astronautics, Inc.': 'arc',
    'Bio-Protocol, LLC': 'bioprotocol',
    'American Roentgen Ray Society': 'ajr',
    'The Company of Biologists': 'biologists',
    'The American Association of Immunologists': 'aai',
    'Society of Exploration Geophysicists': 'seg',
    'Proceedings of the National Academy of Sciences': 'pnas',
    'Society for Neuroscience': 'jneurosci',
    'Frontiers Media SA': 'frontiersin',
    'British Editorial Society of Bone & Joint Surgery': 'boneandjoint',
    'Begell House': 'begell',
    'American Thoracic Society': 'ats',
    'American Mathematical Society': 'amas',
    'Research Square Platform LLC': 'researchsquare',
    'Society for Industrial and Applied Mathematics': 'siam',
    'SciELO Agencia Nacional de Investigacion y Desarrollo (ANID)': 'scielo',
    'Portland Press Ltd.': 'portlandpres',
    'MDPI AG': 'mdpi',
    'The Society of Synthetic Organic Chemistry, Japan': 'jstage',
    'International Union of Crystallography (IUCr)': 'iucr',
    'Inderscience Publishers': 'inderscience',
    'Future Medicine Ltd': 'futuremedicine',
    'Faculty Opinions Ltd': 'facultyopinions',
    'Copernicus GmbH': 'copernicus',
    'American Psychiatric Association Publishing': 'apap',
    'Equinox Publishing': 'equinox',
    'MIT Press': 'mit',
    'American Speech Language Hearing Association': 'asha',
    'Springer Publishing Company': 'springerpub',
    'Georg Thieme Verlag KG': 'thieme',
    'John Benjamins Publishing Company': 'jbe',
    'IOS Press': 'iospress',
    'Institute for Operations Research and the Management Sciences (INFORMS)': 'informs',
    'IGI Global': 'igi',
    'Global Science Press': 'globalsci',
    'eLife Sciences Publications, Ltd': 'elifesciences',
    'Clinical Laboratory Publications': 'clinlab',
    'American Institute of Mathematical Sciences (AIMS)': 'aims',
    'The Electrochemical Society': 'iop',
    'IOP Publishing': 'iop',
    'American Society for Clinical Investigation': 'jci',
    'Trans Tech Publications, Ltd.': 'scientific',
    'SPE': 'onepetro',
    'Society for Makers, Artist, Researchers and Technologists': 'ingenta',
    'SLACK, Inc.': 'healio',
    'Massachusetts Medical Society': 'nejm',
    'DEStech Publications': 'dpiproceedings',
    'Magnolia Press': 'biotaxa',
    'Scientific Societies': 'apsnet',
    'Association for Materials Protection and Performance (AMPP)': 'allenpress',
    'Institute of Organic Chemistry & Biochemistry': 'cccc',
    'Anticancer Research USA Inc.': 'iiar',
    'Institute of Mathematical Statistics': 'projecteuclid',
    'Ornithological Society of Japan': 'bioone',
    'SAE International': 'sae',
    'Hogrefe Publishing Group':'hogrefe',
    'ASME International': 'asme',
    'ASTM International': 'astm',
    'Akademiai Kiado Zrt.': 'akjournals',
    'American Scientific Publishers': 'ingenta',
    'Annual Reviews': 'annualreviews',
    'Atlantis Press': 'atlantis',
    'Bentham Science Publishers Ltd.': 'bentham',
    'Emerald': 'emerald',
    'JSTOR': 'jstor',
    'Microbiology Society': 'microbiologysociety',
    'Princeton University Press': 'degruyter',
    'American Concrete Institute': 'aci',
    "ARMA":"onepetro",
    "Society for Sedimentary Geology":"geoscienceworld",
    "MIS Quarterly":"misq",
    "American Society of Consultant Pharmacists":"ingenta",
    "Japan Petroleum Institute":"jstage",
    "Trans Tech Publications Ltd":"scientific",
    "American Society of Mechanical Engineers":"asme",
    "Mark Allen Group":"magonline",
    "MyJove Corporation":"jove",
    "Water Environment Federation":"ingenta",
    "Institution of Engineering and Technology":"iet",
    "Society of Rheology":"aip",
    "National Institute of Industrial Health":"jstage",
    "American Institute of Aeronautics and Astronautics":"arc",
    "ACM":"acm",
    "Hindawi Limited":"hindawi",
    "GeoScienceWorld":"geoscienceworld",
    "Japan Society for Analytical Chemistry":"ingenta",
    "International Society for Horticultural Science (ISHS)":"ishs",
}

pattern = {
    "elsevier": "(Elsevier BV|Elsevie)",
    "springer": "(Springer|Pleiades Publishing Ltd)",
    "ovid": "(Ovid Technologies|Medknow)",
    "oxford": "(Oxford|The Endocrine Society)",
    "spie": "(SPIE)",
    "wiley": "(Wiley)",
    "ash": "(American Society of Hematology)",
    "taylorfrancis": "(Informa UK Limited|CRC Press|Jenny Stanford Publishing)",
    "nature": "(nature)",
    "acs": "(American Chemical Society)",
    "ieee": "(IEEE|Institute of Electrical and Electronics Engineers)",
    "rsc": "(RSC|Royal Society of Chemistry)",
    "bmj": "(bmj)",
    "iospress": "(IOS Press)",
    "jamanetwork": "(American Medical Association)",
    "ppp": "(Physicians Postgraduate Press)",
    "degruyter": "(Gruyter)",
    "physiology": "(Physiolog)",
    "ams": "(American Meteorological Society)",
    "asce": "(American Society of Civil Engineers)",
    "iet": "(Institution of Engineering and Technology)",
    "osa": "(Optica Publishing Group)",
    "liebert": "(Liebert)",
    "jstage": "(IEE Japan)",
    'aip': "(AIP Publishing|American Vacuum Society|Author\(s\)|AIP)",
    'worldscientific': "(WORLD SCIENTIFIC)",
    "sage": "(sage)",
    'cambridge': '(Cambridge)',
    'karger': '(Karger)',
}

pattern = {k:re.compile(v, re.I) for k, v in pattern.items()}

def _fetch(url):
    for _ in range(2):
        try:
            resp = httpx.get(url, headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            }, verify=False, timeout=15)
            return resp.json()
        except:
            pass

    return None

def FormatPublish(doi, journal, source_publisher):
    # doi 特殊处理
    if '.cnki.' in doi:
        return 'cnki'
    
    if '10.5004/dwt.' in doi:
        return 'deswater'

    # journal 特殊处理
    if "nature" in journal.lower():
        return 'nature'

    publisher = unpaywallMap.get(source_publisher)

    if publisher:
        return publisher
    else:
        for k,v in pattern.items():
            matchd = v.search(source_publisher)
            if matchd:
                return k
            
    return 'default'

def search_by_unpaywall(doi):
    """
    使用 unpaywall 查询文献
    """
    data = _fetch(f'https://api.unpaywall.org/v2/{doi}?email=info@booksci.cn')

    pdf = None
    journal = data.get("journal_name", "") or ""
    source_publisher = data.get("publisher", "") or ""

    best_oa = data.get("best_oa_location")
    if isinstance(best_oa, dict):
        pdf = best_oa.get("url_for_pdf") or best_oa.get("url")
    
    publisher = FormatPublish(doi, journal, source_publisher)
    
    return {
        "doi": data.get("doi"),
        "title": data.get("title"),
        "journal_name": journal,
        "source_publisher": source_publisher,
        "publisher": publisher,
        "is_oa": data.get("is_oa"),
        "pdf": pdf
    }


def search_by_cnki(keyword):
    """
    使用 cnki 查询文献
    """
    publisher = "other"

    url = f'https://bjpaper-cnki-paperserver-yixffbglrj.cn-beijing.fcapp.run/cnki/search?keyWord={keyword}&publishTimeType=1'
    data = _fetch(url)

    if data and len(data["results"]) >= 1:
        title = data["results"][0]["title"]
        # 相似度 > 0.8
        if difflib.SequenceMatcher(None, keyword, title).quick_ratio() > 0.8:
            publisher = 'cnki' 
     
    return {
        "doi": "",
        "title": keyword,
        "journal_name": "",
        "source_publisher": "",
        "publisher": publisher,
        "is_oa": False,
        "pdf": None
    }
    
def doiInfo(doi):
    if re.search(r'[\u4e00-\u9fa5]', doi):
        return search_by_cnki(doi)
    else:
        return search_by_unpaywall(doi)

