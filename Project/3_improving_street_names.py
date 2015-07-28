import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "barcelona_spain.osm"
street_type_re = re.compile(r'\b\S+\.?', re.IGNORECASE)


expected = ["Calle", "Carrer", u"Cam\xed", "Can", "Avinguda", "Avenida", "Plaza", u"Pla\xe7a", u"Pla\xe7eta", "Passeig", "Passatge", "Pasaje", "Carretera", "Autopista", "Rambla", "Barri", "Travessera", "Ronda", "Baixada", "Camp", "Rambleta", "Jardins", "Via", "Platja", "Tren", u"Tur\xf3", "Autovia", "Hospital", "Moll"]

ignored = ["BV-2002", "B-500", "LUGAR", "ACCESO", "BV", "BP-1417", "Paralel"]

typeMissing = ["Gran", "AGUSTI", "Collblanc,", "Serragalliners", u"Enten\xe7a", "Ribot", u"Moss\xe8n",  "Independencia", "Catalans", u"Val\xe8ncia", "Balboa", "Mallorca", "Santiago", "Pelai", "20", "PERE", "22", "la", u"Lan\xe7a", "Girona",  u"Jard\xed", "empuries", "Masia", u"Ram\xf3n", "Abat", "Cristobal", "Baldaya", "MOIANES", "Xucla", "Numancia", "Josep", "Felip", u"Sagu\xe9s", u"Alc\xfadia", u"V\xeda", "Nostra", "Pablo", "Elkano", "Maria", "Ramiro", "Consell", "Mare", "Rembla", "Pere", "Sagrera", "Carles", "Sena", "Taulat", "Eivissa", "girona", "Dr.", "Pi", u"Ruperto", "Immaculada", "Provenza", "Marcelino", "Pizarro", "Ferrer", "Pla", u"Alc\xe0ntara", "Ausias", u"Diputaci\xf3", "Clementina", "Sant", "Vidrieria", "Alacant", "Pau", "GRUNYI", "Pomar", "Padilla", u"Escales", "El", "Llacuna", u"Castell\xf3", "Colom", "31", u"Comer\xe7", "Ramoneda", "Ateneu", u"Vall\xe8s", "Albareda", "Joan", "Campus", "Victor",  "Doctor", "Escullera", "Magdalenes", "Lope", "Gomis", "BOTANICA", u"Cop\xe8rnic", "Rosa", "Comte", "Enric", "Diagonal", "l'Argenteria", "2", "Torras", "Luxemburgo", "Calvet", "Vallirana", "Ginebra", "Secretari", "Adria", "Eucaliptus",  "Roger", u"Cicer\xf3", "Requesens", "Torrent", "Frededic", "Olzinelles", u"Puigcerd\xe0", "Almirall", "Sardenya", u"Baltasar", "La", "Regent", u"Rossell\xf3", "MOSSEN", "Lateral", "Wellinton", "Valencia","Sort", "Blai", u"Estel\xed", u"Arag\xf3", "Viaducte", "Riera", u"Sep\xfalveda", "Ramon", "Frederic", "Reverendo", "Tibidabo", "Santa", u"Pened\xe8s", "Andrea", "Guardiola", "Paisos", "Selva", "Teodora", "Costa", u"Provid\xe8ncia", "CarRoc", "Verge", "Salvador",  "Antoni", "Carders", "santa",  "Parc", "Castillejos", "pau", "Torent",  "Rocafort",  "Aribau", "Prat",  u"Sic\xedlia", "Beat", "Lanzarote", "Muntaner", "JOSEP", u"Almog\xe0vers"]

mapping = { "C.": "Carrer",
            "C/": "Carrer",
            "c/": "Carrer",
            "C": "Carrer",
            "c.": "Carrer",
            "CL": "Carrer",
            "CR": "Carrer",
            "Ca": "Carrer",
            "Career": "Carrer",
            "carrer": "Carrer",
             "Carrar": "Carrer",
            "Caller": "Carrer",
            "Carre": "Carrer",
            "Carrerde": "Carrer de",
            "Carrrer": "Carrer",
            "CALLE": "Carrer",
            "calle": "Carrer",
            "C/Sant": "Carrer Sant",
            "C/TAULAT,": "Carrer Taulat",
            "C/TORRASSA,": "Carrer Torrassa",
            "CarrerAlt": "Carrer Alt",
            "Cami": u"Cam\xed",
            "CAN": "Can",
            u"cam\xed": u"Cam\xed", 
            "cami": u"Cam\xed", 
            "Av": "Avinguda",
            "Av.": "Avinguda",
            "Av": "Avinguda",
            "Avda.": "Avinguda",
            "avinguda": "Avinguda",
            "AVINGUDA": "Avinguda",
            "AVDA": "Avinguda",
            "AVDA.": "Avinguda",
            "AVENIDA": "Avinguda",
            "Avenidas": "Avinguda",
            "Avinguida": "Avinguda",
            "Avnd.de": "Avinguda",
            "Pl.": u"Pla\xe7a",
            "Pl": u"Pla\xe7a",
            "Pl,": u"Pla\xe7a",
            "pl.": u"Pla\xe7a",
            "Placa": u"Pla\xe7a",
            u"P\xba": u"Pla\xe7a",
            "PLAZA": u"Pla\xe7a",
            u"pla\xe7a": u"Pla\xe7a",
            "Placeta":  u"Pla\xe7eta",
            "Pg.": "Passeig",
            "Pg": "Passeig",
            "passeig": "Passeig",
            "Pasatge": "Passatge",
            "passatge": "Passatge",
            "PASEO": "Passeig",
            "Paseo": "Passeig",
            "PS": "Passeig",
            "Rb": "Rambla",
            "CTRA": "Carretera",
            "CTRA.": "Carretera",
            "CRTA.": "Carretera",
            "Ctra.": "Carretera",
            "carretera": "Carretera",
            "CARRETERA": "Carretera",
            "CRA.": "Carretera",
            "ronda": "Ronda",
            "Pol.": "Poligon",
            u"Pol\xedgono": "Poligon",
            "POLIGONO": "Poligon",
            "St.": "Sant",
            "TRAVESSIA": "Travessera",
            "TRAVESIA": "Travessera",
            "Travessia": "Travessera",
            "Travesera": "Travessera",
            "Ptja": "Platja",
            "AUTOVIA": "Autovia",
            "AUTOPISTA": "Autopista",
            "Rbla.": "Rambla",
            "rbla.": "Rambla",
            "rambla": "Rambla",
            "RAMBLA": "Rambla",
            "jardins": "Jardi",
            "Ramble": "Rambla",
            "RONDA": "Ronda",
            "AV.ELECTRICIDAD,ESQ.CHAPLIN": "Avinguda Electricitat - Carrer Chaplin",
            "POL.IND.LAS": "Poligon Ind. las",
            "Pso.Maritimo": "Passeig Maritim",
            }


def audit_street_type(street_types, street_name):
    m = re.search(street_type_re, street_name)
    if m:
        street_type = m.group()
        if street_type not in expected and street_type not in ignored:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib["k"] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib["v"])

    return street_types


def update_name(name, mapping):
    if street_type_re.findall(name)[0] in typeMissing:
        name = "Carrer " + name
    else:
        name = street_type_re.sub(mapping[street_type_re.findall(name)[0]], name, 1 )

    return name


def run():
    st_types = audit(OSMFILE)
    #pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name.encode("utf-8"), "=>", better_name.encode("utf-8")
            
if __name__ == "__main__":
    run()

