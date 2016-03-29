#!/usr/bin/python
# -*- coding: utf-8 -*-

# Jesús Galán Barba
# Ing. en Sistemas de Telecomunicaciones

import webapp
import sys
import urllib


hostname = "localhost"
port = 1234

dicc_cache = {}

class cache_anotada(webapp.webApp):

    def parse(self, request):
        try:
            recurso = request.split()[1][1:].split('/')[1]
            cabeceras = request.split("HTTP/1.1")[1][1:]
        except IndexError:
            return None

        parsedrequest = [recurso, cabeceras]
        return parsedrequest

    def process(self, parsedrequest):

        try:
            recurso, cabeceras = parsedrequest
        except IndexError:
            httpCode = "404 Not Found"
            htmlResp = "<html><body>Error en la solitud!</body></html>"
            return (httpCode, htmlResp)

        url_http = "http://" + recurso
        url_proxy = "http://" + hostname + ":" + str(port) + "/" + recurso
        url_cache = url_proxy + "/cache"
        url_cab1 = url_proxy + "/cabeceras1"
        url_cab2 = url_proxy + "/cabeceras2"
        url_cab3 = url_proxy + "/cabeceras3"
        url_cab4 = url_proxy + "/cabeceras4"

        enlaces = "<center><a href=" + url_http + ">Original webpage</a>" +\
                    "<p><a href=" + url_proxy + ">Reload</a></p>" +\
                    "<p><a href=" + url_cache + ">Cache</a></p>" +\
                    "<p><a href=" + url_cab1 + ">Cabeceras 1</a></p>" +\
                    "<p><a href=" + url_cab2 + ">Cabeceras 2</a></p>" +\
                    "<p><a href=" + url_cab3 + ">Cabeceras 3</a></p>" +\
                    "<p><a href=" + url_cab4 + ">Cabeceras 4</a></p></center>"

        if recurso == "cache/":
            httpCode = "200 OK"
            htmlResp = "<html><body>Esto es cache</body></html>"
        elif recurso == "cabeceras1/":
            httpCode = "200 OK"
            htmlResp = "<html><body>Esto es cabeceras1</body></html>"
        elif recurso == "cabeceras2/":
            httpCode = "200 OK"
            htmlResp = "<html><body>Esto es cabeceras2</body></html>"
        elif recurso == "cabeceras3/":
            httpCode = "200 OK"
            htmlResp = "<html><body>Esto es cabeceras3</body></html>"
        elif recurso == "cabeceras4/":
            httpCode = "200 OK"
            htmlResp = "<html><body>Esto es cabeceras4</body></html>"
        else:
            try:
                fp = urllib.urlopen(url_http)
            except IOError:
                httpCode = "400 Not Found"
                htmlResp = "<html><body><h3> Error. Pagina no encontrada.</h3></body></html>"
                return(httpCode, htmlResp)

            contenido = fp.read()
            dicc_cache[url_http] = contenido
            cadena_find = contenido.find('<body>')
            anotaciones = contenido.find(">", cadena_find)
            html_contenido = (contenido[:anotaciones+1] + enlaces + "\r\n\r\n" + \
                                contenido[(anotaciones+1):])

            httpCode = "200 OK"
            htmlResp = html_contenido

        return (httpCode, htmlResp)



if __name__ == "__main__":
    try:
        Test_cache = cache_anotada(hostname, port)
    except KeyboardInterrupt:
        print "\nAplicación cerrada por el usuario en el terminal!\n"
        sys.exit()
