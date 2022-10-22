from tabulate import tabulate

import cloudscraper

from bs4 import BeautifulSoup

from requests_html import HTMLSession

####### Componentes deseados #######
pc = {
    # Procesador
    "Procesador" : {
        "Nombre": "Intel Core i7-13700K",
        "Cantidad": 1,
        "Urls": {
            "PcComponentes": "https://www.pccomponentes.com/intel-core-i7-13700k-34-ghz-box",
            "Amazon": "https://www.amazon.es/Intel%C2%AE-Procesador-Escritorio-i7-13700K-n%C3%BAcleos/dp/B0BG6843GX/ref=sr_1_1?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=17YONP6JL80QI&keywords=Intel+Core+i7-13700K&qid=1666383541&sprefix=intel+core+i7-13700k%2Caps%2C68&sr=8-1",
            "PcBox": "https://www.pcbox.com/bx8071513700k-cpu-core-i7-13700k-5-4-ghz-lga1700-box/p",
            "Coolmod": "https://www.coolmod.com/intel-core-i7-13700k-5-4ghz-socket-1700-boxed/"
        }
    },
    # Placa Base
    # Memora RAM
    # Caja
    # Refrigeración
    # Almacenamiento
    # Fuente de Alimentación
    # Tarjeta Gráfica
}

selectores = {
    "PcComponentes": "baseprice",
    "Amazon": ".a-offscreen",
    "PcBox": ".vtex-product-price-1-x-currencyInteger",
    "Coolmod": "#normalpricenumber"
}

tabla = [["Componente", "Nombre", "Sitio Web", "Cantidad", "Precio Unit", "Precio Total", "URL"]]


precios = []

for key, value in pc.items():
    fila = [key, value["Nombre"]]
    for nombre, url in value["Urls"].items():
        if (nombre == "PcComponentes"):
            session = cloudscraper.create_scraper(delay=10, browser='chrome')
            with session.get(url) as response:
                print(nombre)
                print(response)
                soup = BeautifulSoup(response.text, "html.parser")
                try:
                    print(soup.find("span", class_=selectores[nombre]).text)
                except:
                    print('Ha cascao')
                    #print(response.text)
        else:
            session = HTMLSession()
            with session.get(url) as response:
                print(nombre)
                print(response)
                response.html.render()
                try:
                    print(response.html.find(selectores[nombre], first=True).text)
                except:
                    print('Ha cascao')
                    print(response.html)

                print('---------')
                #soup = BeautifulSoup(response.content, "html.parser")
                #precios.append(soup.find("span", class_=selectores[nombre]).text)

print("Comparador de PCs 2022")
print(tabulate(tabla, headers="firstrow", tablefmt="fancy_grid"))