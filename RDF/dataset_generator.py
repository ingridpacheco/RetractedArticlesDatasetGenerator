import json
import semanticscholar as sch
import requests
from xml.sax.saxutils import escape
from xml.sax.saxutils import quoteattr
from datetime import date
from datetime import datetime 
import time


#from pprint import pprint
today = date.today() 
doi_api = "https://doi.org/api/handles/"


# Opening JSON retracted file 
with open('./retracted.json') as json_file:
    data = json.load(json_file)

    retratados = data['retratados']
    nomeArquivo = 'retracted-' + str(today) + '.ttl'
    with open(nomeArquivo,'w') as testwritefile:
        #escrevendo cabecalho do arquivo
        testwritefile.write("@base <http://example.org/> .\n")
        testwritefile.write("@prefix dc: <http://purl.org/dc/terms/>  .\n")
        testwritefile.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . \n")
        testwritefile.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . \n")
        testwritefile.write("@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n")
        testwritefile.write("@prefix rel: <http://www.perceive.net/schemas/relationship/> .\n")
        testwritefile.write("@prefix fabio: <http://purl.org/spar/fabio/> .\n")
        testwritefile.write("@prefix cito: <http://purl.org/spar/cito> . \n")
        testwritefile.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
        testwritefile.write("@prefix doi: <http://prismstandard.org/namespaces/basic/2.0/doi#> .\n")
        testwritefile.write("@prefix prism: <http://prismstandard.org/namespaces/basic/2.0/> .  \n")
        
                    
        
        j=0 #contador de Artigos nao encontrados no SEMANTIC SCHOLAR
        i=1
        #pprint(data)
        for artigos in retratados:

            artigo = retratados[artigos]
            #print('doi: ' + str(artigo['doi']))

            if i == 99:
                time.sleep(300)

            paper = sch.paper(artigo['doi'] + "", timeout=8)

            #caso nao encontre o artigo na base, pula pra proxima iteracao
            if not paper:
                j = j + 1
                print("Artigo DOI: " + artigo['doi'] + " nao encontrado no Semantic Scholar")
                continue

            article_url = doi_api + str(artigo['doi']) #obtendo data de publicacao
            r = requests.get(url = article_url)
            response = r.json()
            publication_date = response["values"][0]["timestamp"].split('T')[0]#data de publicacao

            #gravando arquivo
            testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Article ; \n")
            testwritefile.write("\t doi:doi  \""+str(artigo['doi'])+"\" ; \n") 
            testwritefile.write("\t fabio:hasRetractionDate   \""+str(artigo['retractionDate'])+"\"^^xsd:date  ; \n") 
            testwritefile.write("\t prism:publicationDate    \""+str(publication_date)+"\"^^xsd:date  ; \n") 
            testwritefile.write("\t fabio:Abstract   \""+escape(str(paper['abstract'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")  
            testwritefile.write("\t dc:title   \""+escape(str(paper['title'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")  
            testwritefile.write("\t fabio:Report   \""+escape(str(artigo['kind'])) +"\"@en-us  ; \n")  
            testwritefile.write("\t dc:publisher   \""+escape(str(paper['venue'])) +"\"@en-us  ; \n")  
            

            
            for autor in paper['authors'] :
                if autor['authorId'] != None :
                    testwritefile.write("\t dc:creator   <#"+str(autor['authorId']) +">  ; \n")  


            for keyword in paper['topics']:
                testwritefile.write("\t prism:keywords   \""+escape(str(keyword['topic'])).replace('"', '')+"\"@en-us  ; \n")  
            
            if (not paper['fieldsOfStudy'] is None) :
                for field in paper['fieldsOfStudy']:
                    testwritefile.write("\t fabio:SubjectDiscipline   <#"+str((field))+">  ; \n")  
            
            for reason in artigo['reasons']:
                testwritefile.write("\t fabio:retraction   \""+escape(str(reason)).replace('"', '')+"\"@en-us  ; \n")  

            for citacao in paper['citations'] :
                testwritefile.write("\t cito:isCitedBy   <#"+str(citacao['paperId']) +">  ; \n")  

            
            cont = 1
            pontuacao = " ; "
            #if len (paper['references'] ) > 0 :
            #  pontuacao = " ; "

            for location in artigo['Countries']:            
                cont = cont + 1
                testwritefile.write("\t dc:Location   \""+escape(str(location)).replace('"', '')+"\"@en-us  "+pontuacao+" \n")  

            for referencia in paper['references'] :
                doiref = referencia['paperId']

                if referencia['isInfluential'] :
                    testwritefile.write("\t cito:extends   <#"+str(doiref) +">  ; \n")  
                    #explicação de como verifica-se a influencia
                    #https://www.semanticscholar.org/paper/Identifying-Meaningful-Citations-Valenzuela-Ha/1c7be3fc28296a97607d426f9168ad4836407e4b

                for intencao in referencia['intent'] :
                    if intencao.upper() == "background".upper() :
                        testwritefile.write("\t cito:obtainsBackgroundFrom   <#"+str(doiref) +">  ; \n")  

                    if intencao.upper() == "results".upper():
                        testwritefile.write("\t cito:usesDataFrom   <#"+str(doiref) +">  ; \n")  
                        #    ou usesConclusionsFrom ?????????
                    if intencao.upper() == "methods".upper() :
                        testwritefile.write("\t cito:usesMethodIn   <#"+str(doiref) +">  ; \n")  

            publicationYear = 0000
            if paper['year']  != None:
                publicationYear = paper['year']
            testwritefile.write("\t fabio:hasPublicationYear    "+str(publicationYear)+"  . \n")  

            ##montando listagem de referencias
            for referencia in paper['references'] :
                testwritefile.write("<#"+str(referencia['paperId'])+"> a fabio:Article ; \n")
                if referencia['doi'] != None:
                    testwritefile.write("\t doi:doi  \""+str(referencia['doi'])+"\" ; \n")               
                    article_url = doi_api + str(referencia['doi']) #obtendo data de publicacao
                    r = requests.get(url = article_url)
                    response = r.json()
                    if "values" in response:
                        publication_date_reference = response["values"][0]["timestamp"].split('T')[0]#data de publicacao
                        testwritefile.write("\t prism:publicationDate    \""+str(publication_date_reference)+"\"^^xsd:date  ; \n") 

                        
                testwritefile.write("\t cito:isCitedBy   <#"+str(paper['paperId']) +">  ; \n")  
                testwritefile.write("\t dc:title   \""+escape(str(referencia['title'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")
                testwritefile.write("\t dc:publisher   \""+escape(str(referencia['venue'])) +"\"@en-us  ; \n")                       

                for autorReferencia in referencia['authors'] : #carergando autores da referencia
                    if autorReferencia['authorId'] != None :
                        testwritefile.write("\t dc:creator   <#"+str(autorReferencia['authorId']) +">  ; \n")  
                
                publicationYear = 0000
                if referencia['year']  != None:
                    publicationYear = referencia['year']
                testwritefile.write("\t fabio:hasPublicationYear    "+str(publicationYear)+"  . \n")
            

            #criando listagem de autores das referencias  
            for referencia in paper['references'] :     
                for autorReferencia in referencia['authors'] :      
                    testwritefile.write("<#"+str((autorReferencia['authorId']))+"> a foaf:Person ; \n")
                    testwritefile.write("\t foaf:name   \""+escape(str(autorReferencia['name'])) +"\"  . \n") 
            ##fim inclusao de referencias

            #criando listagem de autores dos artigos retratados
            for autor in paper['authors'] :
                testwritefile.write("<#"+str((autor['authorId']))+"> a foaf:Person ; \n")
                testwritefile.write("\t foaf:name   \""+escape(str(autor['name'])) +"\"  . \n")   

            #criando um dictionary de disciplinas 
            if (not paper['fieldsOfStudy'] is None) :
                for field in paper['fieldsOfStudy']:
                    testwritefile.write("<#"+str((field))+"> a fabio:DisciplineDictionary ; \n")
                    testwritefile.write("\t rdfs:label   \""+escape(str(field)) +"\"@en-us  . \n")   

            for citacao in paper['citations'] :
                testwritefile.write("<#"+str(citacao['paperId'])+"> a fabio:Article ; \n")
                if citacao['doi'] != None:
                    time.sleep(0.05)
                    testwritefile.write("\t doi:doi  \""+str(citacao['doi'])+"\" ; \n")               
                    article_url = doi_api + str(citacao['doi']) #obtendo data de publicacao
                    r = requests.get(url = article_url)
                    if r != None :
                        response = r.json()
                        if "values" in response:
                            publication_date_citation = response["values"][0]["timestamp"].split('T')[0]#data de publicacao
                            testwritefile.write("\t prism:publicationDate    \""+str(publication_date_citation)+"\"^^xsd:date  ; \n") 

                
                testwritefile.write("\t cito:cites   <#"+str(paper['paperId']) +">  ; \n")  
                testwritefile.write("\t dc:title   \""+escape(str(citacao['title'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")
                testwritefile.write("\t dc:publisher   \""+escape(str(citacao['venue'])) +"\"@en-us  ; \n")  
                
                if citacao['isInfluential'] :
                    testwritefile.write("\t cito:extends   <#"+str(paper['paperId']) +">  ; \n")  
                    #explicação de como verifica-se a influencia
                    #https://www.semanticscholar.org/paper/Identifying-Meaningful-Citations-Valenzuela-Ha/1c7be3fc28296a97607d426f9168ad4836407e4b

                for intencao in citacao['intent'] :
                    if intencao.upper() == "background".upper() :
                        testwritefile.write("\t cito:obtainsBackgroundFrom   <#"+str(paper['paperId']) +">  ; \n")  

                    if intencao.upper() == "results".upper():
                        testwritefile.write("\t cito:usesDataFrom   <#"+str(paper['paperId']) +">  ; \n")  
                        #    ou usesConclusionsFrom ?????????
                    if intencao.upper() == "methods".upper() :
                        testwritefile.write("\t cito:usesMethodIn   <#"+str(paper['paperId']) +">  ; \n")                    

                for autorCitacao in citacao['authors'] :
                    if autorCitacao['authorId'] != None :
                        testwritefile.write("\t dc:creator   <#"+str(autorCitacao['authorId']) +">  ; \n")  
                
                publicationYear = 0000
                if citacao['year']  != None:
                    publicationYear = citacao['year']
                testwritefile.write("\t fabio:hasPublicationYear    "+str(publicationYear)+"  . \n")  

                    #criando listagem de autores das citacoes       
                for autorCitacao in citacao['authors'] :      
                    testwritefile.write("<#"+str((autorCitacao['authorId']))+"> a foaf:Person ; \n")
                    testwritefile.write("\t foaf:name   \""+escape(str(autorCitacao['name'])) +"\"  . \n") 

            i = i + 1