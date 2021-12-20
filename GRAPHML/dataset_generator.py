import semanticscholar as sch
import requests
from xml.sax.saxutils import escape
from xml.sax.saxutils import quoteattr
from datetime import date 
from datetime import datetime 

#DECLARANDO ARRAY COM OS 77 ARTIGOS RETRATADOS
retratados = [{'doi':'10.7759/cureus.8992','retractionDate':'2021-03-05'},
{'doi':'10.3389/fphar.2021.643369','retractionDate':'2021-03-01'},
{'doi':'10.0139/ssrn.3771318','retractionDate':'2021-02-19'},
{'doi':'10.1016/j.orcp.2020.07.002','retractionDate':'2021-02-06'},
{'doi':'10.1016/j.jinf.2020.02.028','retractionDate':'2021-01-31'},
{'doi':'10.1093/geront/gnaa143','retractionDate':'2021-01-22'},
{'doi':'10.1016/j.jinf.2020.02.022','retractionDate':'2021-01-21'},
{'doi':'10.1128/MRA.00169-20','retractionDate':'2021-01-21'},
{'doi':'10.7759/cureus.9995','retractionDate':'2021-01-13'},
{'doi':'10.7759/cureus.10369','retractionDate':'2021-01-13'},
{'doi':'10.4103/lungindia.lungindia_350_20','retractionDate':'2020-12-31'},
{'doi':'10.1371/journal.pone.0238679','retractionDate':'2020-12-31'},
{'doi':'10.1016/j.jaip.2020.12.047','retractionDate':'2020-12-31'},
{'doi':'10.1002/ptr.6786','retractionDate':'2020-12-30'},
{'doi':'10.1016/j.vaccine.2020.10.014','retractionDate':'2020-12-28'},
{'doi':'10.1016/j.sleepx.2020.100026','retractionDate':'2020-12-05'},
{'doi':'10.1002/opfl.1412','retractionDate':'2020-12-04'},
{'doi':'10.2217/fon-2020-0300','retractionDate':'2020-12-02'},
{'doi':'10.1016/j.ijmmb.2020.10.016','retractionDate':'2020-11-16'},
{'doi':'10.1016/j.ajp.2020.102462','retractionDate':'2020-11-10'},
{'doi':'10.1016/j.scitotenv.2020.142830','retractionDate':'2020-11-05'},
{'doi':'10.1101/2020.10.21.20208728', 'retractionDate':'2020-11-04'}, 
{'doi':'10.1016/j.ajp.2020.102052', 'retractionDate':'2020-11-03'}, 
{'doi':'10.1080/13548506.2020.1754438','retractionDate':'2020-10-23'},
{'doi':'10.1016/j.jhin.2020.10.010','retractionDate':'2020-10-22'},
{'doi':'10.1016/j.neurol.2020.08.001','retractionDate':'2020-10-08'},
{'doi':'10.1164/rccm.202009-3684CP','retractionDate':'2020-10-07'},
{'doi':'10.4097/kja.20227','retractionDate':'2020-09-14'},
{'doi':'10.1016/j.dsx.2020.06.018','retractionDate':'2020-09-11'},
{'doi':'10.1111/liv.14481','retractionDate':'2020-09-01'},
{'doi':'10.1016/j.hlc.2020.08.003','retractionDate':'2020-08-24'},
{'doi':'10.1007/s00415-020-10145-6','retractionDate':'2020-08-09'},
{'doi':'10.1016/j.ijid.2020.08.014','retractionDate':'2020-08-08'},
{'doi':'10.1007/s10389-020-01305-z','retractionDate':'2020-08-03'},
{'doi':'10.4103/jomfp.JOMFP_137_20','retractionDate':'2020-08-01'},
{'doi':'10.1089/dia.2020.0184','retractionDate':'2020-07-27'},
{'doi':'10.1016/j.freeradbiomed.2020.07.014','retractionDate':'2020-07-15'},
{'doi':'10.1038/s41423-020-0424-9','retractionDate':'2020-07-10'},
{'doi':'10.1016/S0140-6736(20)31174-0','retractionDate':'2020-07-09'},
{'doi':'10.1016/j.ajpath.2020.06.012','retractionDate':'2020-07-07'},
{'doi':'10.1016/j.ajog.2020.06.021','retractionDate':'2020-06-25'},
{'doi':'10.1016/j.anndiagpath.2020.151529','retractionDate':'2020-06-22'},
{'doi':'10.1101/2020.05.23.20099671','retractionDate':'2020-06-21'},
{'doi':'10.1101/2020.05.01.20087114','retractionDate':'2020-06-20'},
{'doi':'10.1016/j.amsu.2020.06.008','retractionDate':'2020-06-14'},
{'doi':'10.1101/2020.05.13.20094193','retractionDate':'2020-06-14'},
{'doi':'10.1101/2020.05.05.20092015','retractionDate':'2020-06-13'},
{'doi':'10.1016/j.psym.2020.06.004','retractionDate':'2020-06-12'},
{'doi':'10.1053/j.jvca.2020.06.010','retractionDate':'2020-09-06'},
{'doi':'10.1056/NEJMoa2007621','retractionDate':'2020-06-04'},
{'doi':'10.1016/S0140-6736(20)31180-6','retractionDate':'2020-06-04'},
{'doi':'10.7326/M20-1342','retractionDate':'2020-06-02'},
{'doi':'10.1016/j.tmaid.2020.101665','retractionDate':'2020-06-01'},
{'doi':'10.1016/j.jaccas.2020.05.029','retractionDate':'2020-05-27'},
{'doi':'10.1016/j.jaccas.2020.05.030','retractionDate':'2020-05-27'},
{'doi':'10.1101/2020.05.05.20088757','retractionDate':'2020-05-19'},
{'doi':'10.1016/j.ijnurstu.2020.103635','retractionDate':'2020-05-16'},
{'doi':'10.1016/j.clinimag.2020.05.001','retractionDate':'2020-05-15'},
{'doi':'10.1016/j.jaad.2020.04.140','retractionDate':'2020-05-01'},
{'doi':'10.1016/j.jflm.2020.101964','retractionDate':'2020-04-23'},
{'doi':'10.1016/j.transci.2020.102792','retractionDate':'2020-04-22'},
{'doi':'10.1007/s10489-020-01714-3','retractionDate':'2020-04-22'},
{'doi':'10.1101/2020.04.10.036020','retractionDate':'2020-04-21'},
{'doi':'10.25796/bdd.v3i1.54503','retractionDate':'2020-04-20'},
{'doi':'10.1016/j.sapharm.2020.04.017','retractionDate':'2020-04-19'},
{'doi':'10.1101/2020.04.04.025080','retractionDate':'2020-04-15'},
{'doi':'10.1101/2020.04.08.20058578v2','retractionDate':'2020-04-15'},
{'doi':'10.1016/j.ijantimicag.2020.105949','retractionDate':'2020-04-11'},
{'doi':'10.1016/j.japh.2020.04.007','retractionDate':'2020-04-09'},
{'doi':'10.1016/j.eng.2020.03.007','retractionDate':'2020-04-01'},
{'doi':'10.1016/j.jrid.2020.03.006','retractionDate':'2020-03-31'},
{'doi':'10.3760/cma.j.cn112338-20200221-00144','retractionDate':'2020-03-09'},
{'doi':'10.1101/2020.02.23.20026872','retractionDate':'2020-03-07'},
{'doi':'10.1093/nsr/nwaa036','retractionDate':'2020-03-05'},
{'doi':'10.1016/S2214-109X(20)30065-6','retractionDate':'2020-02-26'},
{'doi':'10.1101/2020.01.30.927871','retractionDate':'2020-02-02'},
{'doi':'10.1101/2020.01.24.919241','retractionDate':'2020-01-28'}
]

retratados_doi = [
    '10.7759/cureus.8992',
    '10.3389/fphar.2021.643369',
    '10.0139/ssrn.3771318',
    '10.1016/j.orcp.2020.07.002',
    '10.1016/j.jinf.2020.02.028',
    '10.1093/geront/gnaa143',
    '10.1016/j.jinf.2020.02.022',
    '10.1128/MRA.00169-20',
    '10.7759/cureus.9995',
    '10.7759/cureus.10369',
    '10.4103/lungindia.lungindia_350_20',
    '10.1371/journal.pone.0238679',
    '10.1016/j.jaip.2020.12.047',
    '10.1002/ptr.6786',
    '10.1016/j.vaccine.2020.10.014',
    '10.1016/j.sleepx.2020.100026',
    '10.1002/opfl.1412',
    '10.2217/fon-2020-0300',
    '10.1016/j.ijmmb.2020.10.016',
    '10.1016/j.ajp.2020.102462',
    '10.1016/j.scitotenv.2020.142830',
    '10.1101/2020.10.21.20208728', 
    '10.1016/j.ajp.2020.102052',
    '10.1080/13548506.2020.1754438',
    '10.1016/j.jhin.2020.10.010',
    '10.1016/j.neurol.2020.08.001',
    '10.1164/rccm.202009-3684CP',
    '10.4097/kja.20227',
    '10.1016/j.dsx.2020.06.018',
    '10.1111/liv.14481',
    '10.1016/j.hlc.2020.08.003',
    '10.1007/s00415-020-10145-6',
    '10.1016/j.ijid.2020.08.014',
    '10.1007/s10389-020-01305-z',
    '10.4103/jomfp.JOMFP_137_20',
    '10.1089/dia.2020.0184',
    '10.1016/j.freeradbiomed.2020.07.014',
    '10.1038/s41423-020-0424-9',
    '10.1016/S0140-6736(20)31174-0',
    '10.1016/j.ajpath.2020.06.012',
    '10.1016/j.ajog.2020.06.021',
    '10.1016/j.anndiagpath.2020.151529',
    '10.1101/2020.05.23.20099671',
    '10.1101/2020.05.01.20087114',
    '10.1016/j.amsu.2020.06.008',
    '10.1101/2020.05.13.20094193',
    '10.1101/2020.05.05.20092015',
    '10.1016/j.psym.2020.06.004',
    '10.1053/j.jvca.2020.06.010',
    '10.1056/NEJMoa2007621',
    '10.1016/S0140-6736(20)31180-6',
    '10.7326/M20-1342',
    '10.1016/j.tmaid.2020.101665',
    '10.1016/j.jaccas.2020.05.029',
    '10.1016/j.jaccas.2020.05.030',
    '10.1101/2020.05.05.20088757',
    '10.1016/j.ijnurstu.2020.103635',
    '10.1016/j.clinimag.2020.05.001',
    '10.1016/j.jaad.2020.04.140',
    '10.1016/j.jflm.2020.101964',
    '10.1016/j.transci.2020.102792',
    '10.1007/s10489-020-01714-3',
    '10.1101/2020.04.10.036020',
    '10.25796/bdd.v3i1.54503',
    '10.1016/j.sapharm.2020.04.017',
    '10.1101/2020.04.04.025080',
    '10.1101/2020.04.08.20058578v2',
    '10.1016/j.ijantimicag.2020.105949',
    '10.1016/j.japh.2020.04.007',
    '10.1016/j.eng.2020.03.007',
    '10.1016/j.jrid.2020.03.006',
    '10.3760/cma.j.cn112338-20200221-00144',
    '10.1101/2020.02.23.20026872',
    '10.1093/nsr/nwaa036',
    '10.1016/S2214-109X(20)30065-6',
    '10.1101/2020.01.30.927871',
    '10.1101/2020.01.24.919241'
]

today = date.today()
doi_api = "https://doi.org/api/handles/"

j=0 #contador de Artigos nao encontrados no SEMANTIC SCHOLAR
citation_article_index = 0

#gravando arquivo
nomeArquivo = 'teste' + str(today) + '.graphml'
with open(nomeArquivo,'w') as testwritefile:

#   #escrevendo cabecalho do arquivo
    testwritefile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    testwritefile.write("<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\" \n")
    testwritefile.write("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n")
    testwritefile.write("xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns\n")
    testwritefile.write("http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">\n")
    testwritefile.write("<graph id=\"\" edgedefault=\"directed\">\n")
    testwritefile.write("<key id=\"d0\" for=\"node\" attr.name=\"color\" attr.type=\"string\"> <default>red</default> </key>\n")
    testwritefile.write("<key id=\"d1\" for=\"node\" attr.name=\"retractionDate\" attr.type=\"string\"> <default></default> </key>\n")
    testwritefile.write("<key id=\"d2\" for=\"node\" attr.name=\"publicationDate\" attr.type=\"string\"> <default></default> </key>\n")
    testwritefile.write("<key id=\"d3\" for=\"edge\" attr.name=\"weight\" attr.type=\"double\"> <default>1</default> </key>\n")
    testwritefile.write("<key id=\"d4\" for=\"edge\" attr.name=\"color\" attr.type=\"string\"> <default></default> </key>\n")
    testwritefile.write("<key id=\"d5\" for=\"node\" attr.name=\"retracted\" attr.type=\"boolean\"> <default></default>False</key>\n")
    testwritefile.write("<key id=\"d6\" for=\"node\" attr.name=\"name\" attr.type=\"string\"> <default></default> </key>\n")
    testwritefile.write("<key id=\"d7\" for=\"node\" attr.name=\"isInfluential\" attr.type=\"boolean\"> <default>False</default> </key>\n")
    testwritefile.write("<key id=\"d8\" for=\"node\" attr.name=\"referencedArticle\" attr.type=\"string\"> <default></default> </key>\n")
    testwritefile.write("<key id=\"d9\" for=\"edge\" attr.name=\"aposRetratacao\" attr.type=\"boolean\"> <default>False</default> </key>\n")
    testwritefile.write("<key id=\"d10\" for=\"edge\" attr.name=\"influential\" attr.type=\"boolean\"> <default>False</default> </key>\n")

    
    #para cada artigoretratado
    for artigo in retratados:
        #consumindo servico do semantic scholar
        paper = sch.paper(artigo['doi'] + "?include_unknown_references=true", timeout=8)

        #caso nao encontre o artigo na base, pula pra proxima iteracao
        if not paper:
            j = j + 1
            continue

        paper.keys()
        article_url = doi_api + artigo['doi']
        r = requests.get(url = article_url)
        response = r.json()
        publication_date = response["values"][0]["timestamp"].split('T')[0]
        title = escape(paper['title']).replace('"', '') #titulo do artigo retratado ja com escape
        testwritefile.write("<node id=\"" +
                            artigo['doi'] + "\"><data key=\"d0\">red</data>  <data key=\"d1\">"+
                            artigo['retractionDate'] +"</data> <data key=\"d2\">"+
                            publication_date +"</data> <data key=\"d5\">True</data> <data key=\"d6\">"+
                            title +"</data> <data key=\"d7\">False</data> </node>\n"
                            ) #escrevo o no do artigo retratado no arquivo

        i=0 #contador de citacoes, pensei em usar de alguma forma pra dizer o peso da aresta, usar o page rank ou algo do tipo
        citacoes_cadastradas= []
        edges_cadastrados= []
        citado_apos_retratacao = 0 # contador de citações após retratação
        
        for citacao in paper['citations']:
            citacao_apos_retratacao_boolean = False
            tituloCitacao = escape(citacao['title']).replace('"', '')  #titulo do artigo que cita o retratado, ja com escape
            citation_id = ''
            if citacao['doi'] != None:
                citation_id = citacao['doi'].upper()
            else:
                citation_id = str(citation_article_index)
                citation_article_index += 1
                
            if not citation_id in citacoes_cadastradas and not citation_id in retratados_doi: #verificao para evitar duplicacao de nos
                citation_publication_date = "undefined"
                weight = 2 if citacao['isInfluential'] == True else 1
                colorEdge = "green" if citacao['isInfluential'] == True else ""
                if citacao['doi'] != None:
                    citation_url = doi_api + citacao['doi']
                    r = requests.get(url = citation_url)
                    response = r.json()
                    if "values" in response:
                        citation_publication_date = response["values"][0]["timestamp"].split('T')[0]

                # Convertendo datas para verificar citação após retratação

                if citation_publication_date != "undefined":
                    data_retratado = datetime.strptime(artigo['retractionDate'], '%Y-%m-%d').date()
                    data_citado = datetime.strptime(citation_publication_date, '%Y-%m-%d').date()

                    if data_retratado < data_citado:
                      citado_apos_retratacao +=1
                      citacao_apos_retratacao_boolean = True
                 # FIM Convertendo datas para verificar citação após retratação

                testwritefile.write("<node id=\"" + 
                                    citation_id + "\"><data key=\"d2\">" +
                                    citation_publication_date + "</data><data key=\"d5\">False</data> <data key=\"d6\">" +
                                    tituloCitacao + "</data> <data key=\"d7\">" +
                                    str(citacao['isInfluential']) + "</data> <data key=\"d8\">" +
                                    artigo['doi'] + "</data></node>\n") #escrevo o no do artigo que cita o retratado
                citacoes_cadastradas.append(citation_id)
            edge = "<edge source=\""+ citation_id +"\" target=\"" + artigo['doi'] + "\"><data key=\"d3\">"                     + str(weight) + "</data><data key=\"d4\">"                     + colorEdge + "</data><data key=\"d9\">"                     + str(citacao_apos_retratacao_boolean) + "</data><data key=\"d10\">" +                          str(citacao['isInfluential']) + "</data></edge>\n" 
            if not citation_id + "|" + artigo['doi'] in edges_cadastrados:  #verifico se já existe aquela aresta antes de criar uma nova                       
              testwritefile.write(edge) #escrevo a aresta
              edges_cadastrados.append(citation_id + "|" + artigo['doi'])
              i = i + 1       
        
        print(title)
        print("ano publicação: " + str(publication_date))
        print("ano retratação: " + str(artigo['retractionDate']))
        print("contem " + str(i) + " citacoes")
        print("contem " + str(citado_apos_retratacao) + " citacoes apos retratacao")
        print("---------------")
       
    testwritefile.write("</graph></graphml>") 

print("Arquivo gerado com sucesso em: " + nomeArquivo)    
print(str(j) + " artigos nao encontrados no Semantic Scholar")