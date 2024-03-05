import re
import httpx

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
    'American Concrete Institute': 'aci'
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
    "sage": "(sage)"
}

pattern = {k:re.compile(v, re.I) for k, v in pattern.items()}

def FormatPublish(x):
    publisher = unpaywallMap.get(x)

    if publisher:
        return publisher
    else:
        for k,v in pattern.items():
            matchd = v.search(x)
            if matchd:
                return k

    return "doi" if '10.' in x else "other"
    
def doiInfo(doi):
    for _ in range(2):
        try:
            resp = httpx.get(f'https://api.unpaywall.org/v2/{doi}?email=info@booksci.cn', verify=False, follow_redirects=False, timeout=10)
            data = resp.json()
            break
        except:
            pass

    journal = data.get("journal_name", "") or ""
    source_publisher = data.get("publisher", "") or ""
    publisher = "nature" if "nature" in journal.lower() else FormatPublish(source_publisher)
    
    best_oa = data.get("best_oa_location")

    pdf = None
    if isinstance(best_oa, dict):
        pdf = best_oa.get("url_for_pdf") or best_oa.get("url")

    return {
        "doi": data.get("doi"),
        "title": data.get("title"),
        "journal_name": journal,
        "source_publisher": source_publisher,
        "publisher": publisher,
        "is_oa": data.get("is_oa"),
        "pdf": pdf
    }
