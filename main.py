from tabulate import tabulate
import cloudscraper
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from components import pc
import pyshorteners

srtUrl = pyshorteners.Shortener()
selectores = {
    "PcComponentes": "precio-main",
    "Amazon": ".a-offscreen",
    "PcBox": [".vtex-product-price-1-x-currencyInteger", ".vtex-product-price-1-x-currencyFraction"],
    "Coolmod": "#normalpricenumber",
    "Corsair": ".product-price",
    "Casemod": ".product-price",
    "Nvidia": ".startingprice",
}

tabla = [["Componente", "Nombre", "Sitio Web", "Cantidad", "Precio Unit", "Precio Total", "URL"]]
precioFinal = 0.0


for key, value in pc.items():
    fila = [key, value["Nombre"]]
    precios = {}

    for nombre, url in value["Urls"].items():
        print("ESTADO: Buscando " + value["Nombre"] + " en " + nombre, end="\r")
        if (nombre == "PcComponentes"):
            session = cloudscraper.create_scraper(delay=10, browser='chrome')
            with session.get(url) as response:
                #print(nombre)
                #print(response)
                soup = BeautifulSoup(response.text, "html.parser")
                try:
                    precio = soup.find("div", id=selectores[nombre]).attrs['data-price'].replace('.', ',')
                    if(not ',' in precio):
                        precio += ",00"
                    #print(precio)
                    precios[nombre] = precio
                except:
                    print('Ha cascao')
                    #print(response.text)
        else:
            session = HTMLSession()
            with session.get(url) as response:
                #print(nombre)
                #print(response.text)
                response.html.render()
                try:
                    if (nombre == "PcBox"):
                        precio = response.html.find(selectores[nombre][0], first=True).text
                        precio += ','
                        precio += response.html.find(selectores[nombre][1], first=True).text
                        precios[nombre] = precio
                    elif (nombre == "Nvidia"):
                        precio = response.html.find(selectores[nombre], first=True).text.replace('RTX 4080 (16GB) a partir de', '').replace('€', '').replace(' ', '').replace('.', '')
                        precios[nombre] = precio
                    else:
                        precio = response.html.find(selectores[nombre], first=True).text.replace('€', '').replace(' ', '')
                        #print(precio)
                        precios[nombre] = precio
                except:
                    print('Ha cascao')
                    #print(response.html)
        print("                                                                              ", end="\r")
        
    lugar = list(value["Urls"].keys())[0]
    dineros = 100000000.00
    for sitio, coste in precios.items():
        if(float(coste.replace(',', '.')) < dineros):
            lugar = sitio
            dineros = float(coste.replace(',', '.'))
    precioUnit = str(dineros).replace('.', ',') + "€"
    precioTot = str(dineros * value["Cantidad"]).replace('.', ',') + "€"
    fila.append(lugar)
    fila.append(value["Cantidad"])
    fila.append(precioUnit)
    fila.append(precioTot)
    fila.append(srtUrl.tinyurl.short(value["Urls"][lugar]))
    tabla.append(fila)
    precioFinal += dineros * value["Cantidad"]


precioEnTabla = str(round(precioFinal, 2)).replace('.', ',')
if(not ',' in precioEnTabla):
    precioEnTabla += ",00"
precioEnTabla += "€"
tabla2 = [["Precio Total", precioEnTabla]]

print("Comparador de PCs 2022")
print(tabulate(tabla, headers="firstrow", tablefmt="fancy_grid"))
print(tabulate(tabla2, tablefmt="fancy_grid"))