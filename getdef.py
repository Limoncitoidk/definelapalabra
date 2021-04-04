import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re


roman_nums = ["I", "II", "III", "IV", "V"]

def getDef(palabra):
    
    #URL del sitio web (el método urllib.parse es para codificar los caracteres especiales a url) 
    url = "https://dle.rae.es/?w=" + urllib.parse.quote_plus(palabra)

    #Headers
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    #Obtener el código HTML del sitio web
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf8')
    soup = BeautifulSoup(html, features="html.parser")

    #Remueve la tabla de conjugaciones para los verbos
    #Esto es necesario ya que la tabla está dentro de un tag <article>
    for tabla_conj in soup.find_all("div", attrs={"id": "conjugacion"}):
        tabla_conj.extract()

    #Verifica que la palabra exista
    #Cada artículo corresponde a una entrada distinta (por lo general, cada palabra posee solo una entrada) 
    if len(soup.find_all("article")) > 0:

        finalstr = ""
        index = 0
            
        for entradas in soup.find_all("article"):

            if len(soup.find_all("article")) > 1:    
                finalstr = finalstr + "Entrada " + roman_nums[index] + "\n\n"
                index = index + 1

            #Cada definición corresponde a una acepción distinta de la palabra
            for defstr in entradas.select('p[class="j"], p[class="j1"], p[class="j2"], p[class="l2"]'):
            
                for extrastr in defstr.select('abbr[title*="usado"], abbr[title*="Usado"], span[class="h"], sup'):
                    if extrastr.text.strip() != "U.":
                        extrastr.extract()

                #Quita los caracteres especiales (‖)
                texto = defstr.text.strip().replace("‖ ","")

                #Reemplaza los espacios dobles y triples por uno solo ("Hola   mundo" -> "Hola mundo")
                texto = re.sub("\s\s+", " ", texto)
            
                finalstr = finalstr + texto + "\n"
            finalstr = finalstr + "\n"
            
        return finalstr
    
    else:
        
        return "No hemos encontrado una definición para la palabra que buscas. ¿Estás seguro de haberla escrito bien?"

#Solo para uso local (consola)

#print("Escribe la palabra que desees buscar:")

#while(True):       
#    palabra = input()
#    print("")
#    print(getDef(palabra))


