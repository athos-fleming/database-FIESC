import os
import requests
import pandas as pd

class Variables(object):
    def __init__(self,name,codigo,APIadress,APIparameters,Operadores,Series,ColumnNames):
        self.name = name
        self.codigo = codigo
        self.APIadress = APIadress
        self.APIparameters = APIparameters
        self.Operadores = Operadores
        self.Series = Series
        self.ColumnNames = ColumnNames

listVariables = []
listModels = []

#grupo do ipea, corre bem tranquilo


#variavel IPCA - geral - taxa de variação  mensa % a.m.
listVariables.append(Variables('ipca_mensal_taxa_variação',"'PRECOS12_IPCAG12'","ipea",
                               "01/01/1980",[""],["mensal"],
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_variação"}
    ))

#variavel IPCA - núcleo médias aparadas com suavização - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_médias_aparadas_suavização',"'BM12_IPCA2012'","ipea",
                               "01/01/1992",[""],["mensal"],
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_médias_aparadas_suavização"}
    ))

#variavel IPCA - núcleo médias aparadas sem suavização - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_médias_aparadas_sem_suavização',"'BM12_IPCA20N12'","ipea",
                               "01/01/1992",[""],["mensal"],
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_médias_aparadas_sem_suavização"}
    ))

#variavel IPCA - núcleo por exclusão - EX1 - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_exclusão',"'BM12_IPCAEXCEX212'","ipea",
                               "01/01/1992",[""],["mensal"],
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_exclusão"}
    ))

#variavel IPCA - núcleo por exclusão - sem monitorados e alimentos no domicílio % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_exclusão_domiciliar',"'BM12_IPCAEXC12'","ipea",
                               "01/01/1992",[""],["mensal"],
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_exclusão_domiciliar"}
    ))

#variavel IPCA - preços livres - serviços % a.m.
listVariables.append(Variables('ipca_mensal_taxa_preços_livres_serviços',"'BM12_IPCAPLSER12'","ipea",
                               "01/01/1992",[""],["mensal"],
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_preços_livres_serviços"}
    ))

#variavel PIB - Mensal % a.m.
listVariables.append(Variables('pib_mensal_taxa_variação',"'BM12_PIB12'","ipea",
                               "01/01/1990",[""],["mensal"],
                               {"VALDATA": "date","VALVALOR": "pib_mensal_taxa_variação"}
    ))


#grupo do bcb, as vezes da erro de api call


#variavel Dívida líquida do governo geral (% PIB) % a.m.
listVariables.append(Variables('divida_mensal_publica__liquida_consolidado_pib',"4513","bcb",
                               "01/12/2001",[""],["mensal"],
                               {"data": "date","valor": "divida_mensal_publica__liquida_consolidado_pib"}
    ))

#variavel Dívida bruta do governo geral (% PIB) % a.m.
listVariables.append(Variables('divida_mensal_publica__bruta_pib',"13762","bcb",
                               "01/12/2006",[""],["mensal"],
                               {"data": "date","valor": "divida_mensal_publica__bruta_pib"}
    ))

#variavel SELIC Mensal % a.m.
listVariables.append(Variables('selic_mensal',"4189","bcb",
                               "01/01/2000",[""],["mensal"],
                               {"data": "date","valor": "selic_mensal"}
    ))

#variavel SELIC diaria % a.a.
listVariables.append(Variables('selic_diaria',"11","bcb",
                               "01/01/2000",[""],["diaria"],
                               {"data": "date","valor": "selic_diaria"}
    ))


#grupo do sidra, grande volume de dados, pode ser lento


#variavel IPCA - geral - taxa de variação  mensa % a.m.
listVariables.append(Variables('pim_pf_mensal',"8888-12606","sidra",
                               {"periodos":"200201|200202|200203|200204|200205|200206|200207|200208|200209|200210|200211|200212|200301|200302|200303|200304|200305|200306|200307|200308|200309|200310|200311|200312|200401|200402|200403|200404|200405|200406|200407|200408|200409|200410|200411|200412|200501|200502|200503|200504|200505|200506|200507|200508|200509|200510|200511|200512|200601|200602|200603|200604|200605|200606|200607|200608|200609|200610|200611|200612|200701|200702|200703|200704|200705|200706|200707|200708|200709|200710|200711|200712|200801|200802|200803|200804|200805|200806|200807|200808|200809|200810|200811|200812|200901|200902|200903|200904|200905|200906|200907|200908|200909|200910|200911|200912|201001|201002|201003|201004|201005|201006|201007|201008|201009|201010|201011|201012|201101|201102|201103|201104|201105|201106|201107|201108|201109|201110|201111|201112|201201|201202|201203|201204|201205|201206|201207|201208|201209|201210|201211|201212|201301|201302|201303|201304|201305|201306|201307|201308|201309|201310|201311|201312|201401|201402|201403|201404|201405|201406|201407|201408|201409|201410|201411|201412|201501|201502|201503|201504|201505|201506|201507|201508|201509|201510|201511|201512|201601|201602|201603|201604|201605|201606|201607|201608|201609|201610|201611|201612|201701|201702|201703|201704|201705|201706|201707|201708|201709|201710|201711|201712|201801|201802|201803|201804|201805|201806|201807|201808|201809|201810|201811|201812|201901|201902|201903|201904|201905|201906|201907|201908|201909|201910|201911|201912|202001|202002|202003|202004|202005|202006|202007|202008|202009|202010|202011|202012|202101|202102|202103|202104|202105|202106|202107|202108|202109|202110|202111|202112|202201|202202|202203|202204|202205|202206|202207|202208|202209|202210|202211|202212|202301|202302|202303|202304|202305|202306|202307|202308|202309|202310|202311|202312|202401|202402|202403|202404|202405|202406|202407",
                                "variaveis":"12606","localidade":"N3[42]","classificacao":"544[all]"},["seasonal"],[""],
                               {"date":"date",
                                "1 Indústria geral":"1_Industria_Geral",
                                "2 Indústrias extrativas":"2_Industria_Extrativa",
                                "3 Indústrias de transformação":"3_Industrias_Transformacao",
                                "3.10 Fabricação de produtos alimentícios":"3.10_Alimenticios",
                                "3.11 Fabricação de bebidas":"3.11_bebidas",
                                "3.12 Fabricação de produtos do fumo":"3.12_fumo",
                                "3.13 Fabricação de produtos têxteis":"3.13_texteis",
                                "3.14 Confecção de artigos do vestuário e acessórios":"3.14_vestuário_acessorios",
                                "3.15 Preparação de couros e fabricação de artefatos de couro, artigos para viagem e calçados":"3.15_couro",
                                "3.16 Fabricação de produtos de madeira":"3.16_madeira",
                                "3.17 Fabricação de celulose, papel e produtos de papel":"3.17_celulose",
                                "3.18 Impressão e reprodução de gravações":"3.18_gravacoes",
                                "3.19 Fabricação de coque, de produtos derivados do petróleo e de biocombustíveis":"3.19_petroleo_biocombustiveis",
                                "3.20 Fabricação de produtos químicos":"3.20_quimicos",
                                "3.21 Fabricação de produtos farmoquímicos e farmacêuticos":"3.21_farmoquimicos_farmaceuticos",
                                "3.22 Fabricação de produtos de borracha e de material plástico":"3.22_borracha_plastico",
                                "3.23 Fabricação de produtos de minerais não metálicos":"3.23_minerais_nao_metalicos",
                                "3.24 Metalurgia":"3.24_Metalurgia",
                                "3.25 Fabricação de produtos de metal, exceto máquinas e equipamentos":"3.25_metal_exceto_maquinas_equipamentos",
                                "3.26 Fabricação de equipamentos de informática, produtos eletrônicos e ópticos":"3.26_informática_eletrônicos_opticos",
                                "3.27 Fabricação de máquinas, aparelhos e materiais elétricos":"3.27_maquinas_aparelhos_eletricos",
                                "3.28 Fabricação de máquinas e equipamentos":"3.28_maquinas_equipamentos",
                                "3.29 Fabricação de veículos automotores, reboques e carrocerias":"3.29_veiculos",
                                "3.30 Fabricação de outros equipamentos de transporte, exceto veículos automotores":"3.30_outros_transporte",
                                "3.31 Fabricação de móveis":"3.31_moveis",
                                "3.32 Fabricação de produtos diversos":"3.32_diversos",
                                "3.33 Manutenção, reparação e instalação de máquinas e equipamentos":"3.33_Manutenção_maquinas_equipamentos"                            
                               }
    ))

#models estabelecidos


