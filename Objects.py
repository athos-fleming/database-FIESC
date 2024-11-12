import os
import requests
import pandas as pd

class Variables(object):
    def __init__(self,name,codigo,APIadress,APIparameters,Operadores,OperadorParameters,ColumnNames):
        self.name = name
        self.codigo = codigo
        self.APIadress = APIadress
        self.APIparameters = APIparameters
        self.Operadores = Operadores
        self.OperadorParameters = OperadorParameters
        self.ColumnNames = ColumnNames
        
class Models(object):
    def __init__(self,name,date,regressor,variables,mergeParameters):
        self.name = name
        self.date = date
        self.regressor = regressor
        self.variables = variables
        self.mergeParameters = mergeParameters
        

listVariables = []
listModels = []

#grupo do ipea, corre bem tranquilo

#variavel IPCA - geral - taxa de variação  mensa % a.m.
listVariables.append(Variables('ipca_mensal_taxa_variação',"'PRECOS12_IPCAG12'","ipea",
                               "01/01/1980",["rolling"],{"especial":"ipca_juros_real","rolling":"-12"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_variação"}
    ))

#variavel IPCA - núcleo médias aparadas com suavização - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_médias_aparadas_suavização',"'BM12_IPCA2012'","ipea",
                               "01/01/1992",["rolling"],{"rolling":"-12"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_médias_aparadas_suavização"}
    ))

#variavel IPCA - núcleo médias aparadas sem suavização - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_médias_aparadas_sem_suavização',"'BM12_IPCA20N12'","ipea",
                               "01/01/1992",[""],{},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_médias_aparadas_sem_suavização"}
    ))

#variavel IPCA - núcleo por exclusão - EX1 - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_exclusão',"'BM12_IPCAEXCEX212'","ipea",
                               "01/01/1992",["rolling"],{"rolling":"-12"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_exclusão"}
    ))

#variavel IPCA - núcleo por exclusão - sem monitorados e alimentos no domicílio % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_exclusão_domiciliar',"'BM12_IPCAEXC12'","ipea",
                               "01/01/1992",[""],{},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_exclusão_domiciliar"}
    ))

#variavel IPCA - preços livres - serviços % a.m.
listVariables.append(Variables('ipca_mensal_taxa_preços_livres_serviços',"'BM12_IPCAPLSER12'","ipea",
                               "01/01/1992",["rolling"],{"rolling":"-12"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_preços_livres_serviços"}
    ))

#variavel PIB - Mensal em Reais % a.m.
listVariables.append(Variables('pib_mensal_reais',"'BM12_PIB12'","ipea",
                               "01/01/1990",[""],{},
                               {"VALDATA": "date","VALVALOR": "pib_mensal_reais"}
    ))

#variavel IPP industria da transformação indice dez 2018 % a.m.
listVariables.append(Variables('ipp_transformacao_dez18',"'IPP12_IPPC12'","ipea",
                               "01/01/2010",[""],{},
                               {"VALDATA": "date","VALVALOR": "ipp_transformacao_dez18"}
    ))

#variavel IPP industria da transformação indice dez 2018 % a.m.
listVariables.append(Variables('ipp_transformacao_taxa_mensal',"'IPP12_IPPCG12'","ipea",
                               "01/01/2010",[""],{},
                               {"VALDATA": "date","VALVALOR": "ipp_transformacao_taxa_mensal"}
    ))

#IBC-BR base 2002=100 % a.m.
listVariables.append(Variables('ibc_br_mensal',"'SGS12_IBCBR12'","ipea",
                               "01/01/2003",["seasonal_getallbases","variation"],{"variation":"12"},
                               {"VALDATA": "date","VALVALOR": "ibc_br_mensal"}
    ))

#IBC-BR dessazonalizado % a.m.
listVariables.append(Variables('ibc_br_mensal_dessazonalizado',"'SGS12_IBCBRDESSAZ12'","ipea",
                               "01/01/2003",["getallbases","variation"],{"variation":"12"},
                               {"VALDATA": "date","VALVALOR": "ibc_br_mensal_dessazonalizado"}
    ))

#PIB consumo final das familias % a.t.
listVariables.append(Variables('pib_consumo_familias_trimestral_corrente',"'SCN104_CFPPN104'","ipea",
                               "01/01/2003",["#trimestertomonth"],{"trimestertomonth":False},
                               {"VALDATA": "date","VALVALOR": "pib_consumo_familias_trimestral_corrente"}
    ))



#grupo do bcb, as vezes da erro de api call



#variavel Dívida líquida do governo geral (% PIB) % a.m.
listVariables.append(Variables('divida_mensal_publica__liquida_consolidado_pib',"4513","bcb",
                               "01/12/2001",[""],{},
                               {"data": "date","valor": "divida_mensal_publica__liquida_consolidado_pib"}
    ))

#variavel Dívida bruta do governo geral (% PIB) % a.m.
listVariables.append(Variables('divida_mensal_publica__bruta_pib',"13762","bcb",
                               "01/12/2006",[""],{},
                               {"data": "date","valor": "divida_mensal_publica__bruta_pib"}
    ))

#variavel SELIC Mensal % a.m.
listVariables.append(Variables('selic_mensal',"4189","bcb",
                               "01/01/2000",[""],{},
                               {"data": "date","valor": "selic_mensal"}
    ))

#variavel SELIC diaria % a.a.
listVariables.append(Variables('selic_diaria',"11","bcb",
                               "01/01/2000",[""],{},
                               {"data": "date","valor": "selic_diaria"}
    ))


#variavel Indicador de Custo do Crédito - ICC - Recursos/Crédito livre - Pessoas jurídicas % a.m.
listVariables.append(Variables('icc_rescursos_livres_pj',"25355","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "icc_rescursos_livres_pj"}
    ))

#variavel Inadimplência da carteira de crédito - Pessoas físicas - Total % a.m.
listVariables.append(Variables('inadimplencia_pf_total',"21084","bcb",
                               "01/03/2011",["seasonal"],{},
                               {"data": "date","valor": "inadimplencia_pf_total"}
    ))

#variavel 	Saldo da carteira de crédito com recursos livres - Pessoas físicas - Total % a.m.
listVariables.append(Variables('saldo_credito_pf_total',"20580","bcb",
                               "01/03/2011",["seasonal_deflacionar"],{"deflacionar":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_credito_pf_total"}
    ))

#variavel 	Saldo da carteira de crédito com recursos livres - Pessoas físicas - Aquisição de outros bens % a.m.
listVariables.append(Variables('saldo_credito_pf_outros',"20582","bcb",
                               "01/03/2011",["seasonal"],{},
                               {"data": "date","valor": "saldo_credito_pf_outros"}
    ))

#variavel 	Saldo da carteira de crédito com recursos livres - Pessoas físicas - Aquisição de outros bens % a.m.
listVariables.append(Variables('icc_rescursos_livres_pj_outros',"27659","bcb",
                               "01/01/2013",[""],{},
                               {"data": "date","valor": "icc_rescursos_livres_pj_outros"}
    ))

#variavel IPCA Industrias, subcategoria de serviços % a.m.
listVariables.append(Variables('ipca_industrial',"27863","bcb",
                               "01/01/2000",["rolling"],{"rolling":"-12"},
                               {"data": "date","valor": "ipca_industrial"}
    ))

#variavel Endividamento das familias em relação a renda acumulada dos 12 meses % a.m.
listVariables.append(Variables('endividamento_familias_relacao_renda_acumulada',"29037","bcb",
                               "01/01/2005",[""],{""},
                               {"data": "date","valor": "endividamento_familias_relacao_renda_acumulada"}
    ))

#variavel IBCR-SC Indice de Atividade Economica de Santa Catarina % a.m.
listVariables.append(Variables('ibcr_sc_mensal',"25402","bcb",
                               "01/01/2003",["seasonal","seasonal_getallbases","seasonal_variation"],{"variation":"12"},
                               {"data": "date","valor": "ibcr_sc_mensal"}
    ))

#variavel IBCR-SC Indice de Atividade Economica de Santa Catarina dessazonalizado % a.m.
listVariables.append(Variables('ibcr_sc_mensal_dessazonalizado',"25405","bcb",
                               "01/01/2003",["getallbases","variation"],{"variation":"12"},
                               {"data": "date","valor": "ibcr_sc_mensal_dessazonalizado"}
    ))


#grupo do bcb - focus, dados em painel, process mais complicado e demorado



#variavel expectativa IPCA
listVariables.append(Variables('expectativa_ipca_2024',"IPCA-ipca focus","bcb_focus",
                               "2022-12-31",["transpose_rolling_transpose","latest_transpose_rolling","firstdayofmonth_transpose_rolling"],
                               {"rolling":"ipca_mensal_taxa_variação-12"},
                               {""}    
    ))

#variavel expectativa IPCA serviços
listVariables.append(Variables('expectativa_ipca_servicos_2024',"IPCA%20Servi%C3%A7os-ipca servicos focus","bcb_focus",
                               "2022-12-31",["transpose_rolling_transpose","latest_transpose_rolling","firstdayofmonth_transpose_rolling"],
                               {"rolling":"ipca_mensal_taxa_preços_livres_serviços-12"},
                               {""}    
    ))



#grupo do sidra, grande volume de dados, pode ser lento


#PIM PF
#variavel Produção Física Industrial de SC, por seções e atividades industriais mensal % a.m.
listVariables.append(Variables('pim_pf_mensal_sc',"8888-12606-sc","sidra",
                               {"periodos":"-500","variaveis":"12606","localidade":"N3[42]","classificacao":"544[all]"},
                               ["seasonal","seasonal_getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "1 Indústria geral":"1_Geral_sc",
                                "2 Indústrias extrativas":"2_Extrativa_sc",
                                "3 Indústrias de transformação":"3_Transformacao_sc",
                                "3.10 Fabricação de produtos alimentícios":"3.10_Alimentícios_sc",
                                "3.11 Fabricação de bebidas":"3.11_Bebidas_sc",
                                "3.12 Fabricação de produtos do fumo":"3.12_Fumo_sc", 
                                "3.13 Fabricação de produtos têxteis":"3.13_Têxteis_sc",
                                "3.14 Confecção de artigos do vestuário e acessórios":"3.14_confecções_sc",
                                "3.15 Preparação de couros e fabricação de artefatos de couro, artigos para viagem e calçados":"3.15_Couro_sc",
                                "3.16 Fabricação de produtos de madeira":"3.16_Madeira_sc",
                                "3.17 Fabricação de celulose, papel e produtos de papel":"3.17_Celulose_sc",
                                "3.18 Impressão e reprodução de gravações":"3.18_Gravações_sc",
                                "3.19 Fabricação de coque, de produtos derivados do petróleo e de biocombustíveis":"3.19_combustiveis_sc",
                                "3.20 Fabricação de produtos químicos":"3.20_Químicos_sc",
                                "3.21 Fabricação de produtos farmoquímicos e farmacêuticos":"3.21_Farmo_sc",
                                "3.22 Fabricação de produtos de borracha e de material plástico":"3.22_Borracha_Plástico_sc",
                                "3.23 Fabricação de produtos de minerais não metálicos":"3.23_Minerais_nâo_metálicos_sc",
                                "3.24 Metalurgia":"3.24_Metalurgia_sc",
                                "3.25 Fabricação de produtos de metal, exceto máquinas e equipamentos":"3.25_Produtos_metal_sc",
                                "3.26 Fabricação de equipamentos de informática, produtos eletrônicos e ópticos":"3.26_info_eletro_optico_sc",
                                "3.27 Fabricação de máquinas, aparelhos e materiais elétricos":"3.27_Materiais_elétricos_sc",
                                "3.28 Fabricação de máquinas e equipamentos":"3.28_Maquinas_equipamentos_sc",
                                "3.29 Fabricação de veículos automotores, reboques e carrocerias":"3.29_Veículos_sc",
                                "3.30 Fabricação de outros equipamentos de transporte, exceto veículos automotores":"3.30_outros_transporte_sc",
                                "3.31 Fabricação de móveis":"3.31_Móveis_sc",
                                "3.32 Fabricação de produtos diversos":"3.32_Diversos_sc",
                                "3.33 Manutenção, reparação e instalação de máquinas e equipamentos":"3.33_Manutenção_sc"                            
                               }
    ))

#variavel Produção Física Industrial de SC já dessazonalizada, por seções e atividades industriais mensal % a.m.
listVariables.append(Variables('pim_pf_mensal_sc_dessazonalizado',"8888-12607-sc","sidra",
                               {"periodos":"-500","variaveis":"12607","localidade":"N3[42]","classificacao":"544[129314]"},
                               ["getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "1 Indústria geral":"1_Geral_sc"
                                 }
    ))

#variavel Produção Física Industrial BR, por seções e atividades industriais mensal % a.m.
listVariables.append(Variables('pim_pf_mensal_br',"8888-12606-br","sidra",
                               {"periodos":"-500","variaveis":"12606","localidade":"N1[all]","classificacao":"544[all]"},
                               ["seasonal","","seasonal_getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "1 Indústria geral":"1_Geral_br",
                                "2 Indústrias extrativas":"2_Extrativa_br",
                                "3 Indústrias de transformação":"3_Transformacao_br",
                                "3.10 Fabricação de produtos alimentícios":"3.10_Alimentícios_br",
                                "3.11 Fabricação de bebidas":"3.11_Bebidas_br",
                                "3.12 Fabricação de produtos do fumo":"3.12_Fumo_br", 
                                "3.13 Fabricação de produtos têxteis":"3.13_Têxteis_br",
                                "3.14 Confecção de artigos do vestuário e acessórios":"3.14_confecções_br",
                                "3.15 Preparação de couros e fabricação de artefatos de couro, artigos para viagem e calçados":"3.15_Couro_br",
                                "3.16 Fabricação de produtos de madeira":"3.16_Madeira_br",
                                "3.17 Fabricação de celulose, papel e produtos de papel":"3.17_Celulose_br",
                                "3.18 Impressão e reprodução de gravações":"3.18_Gravações_br",
                                "3.19 Fabricação de coque, de produtos derivados do petróleo e de biocombustíveis":"3.19_combustiveis_br",
                                "3.20 Fabricação de produtos químicos":"3.20_Químicos_br",
                                "3.21 Fabricação de produtos farmoquímicos e farmacêuticos":"3.21_Farmo_br",
                                "3.22 Fabricação de produtos de borracha e de material plástico":"3.22_Borracha_Plástico_br",
                                "3.23 Fabricação de produtos de minerais não metálicos":"3.23_Minerais_nâo_metálicos_br",
                                "3.24 Metalurgia":"3.24_Metalurgia_br",
                                "3.25 Fabricação de produtos de metal, exceto máquinas e equipamentos":"3.25_Produtos_metal_br",
                                "3.26 Fabricação de equipamentos de informática, produtos eletrônicos e ópticos":"3.26_info_eletro_optico_br",
                                "3.27 Fabricação de máquinas, aparelhos e materiais elétricos":"3.27_Materiais_elétricos_br",
                                "3.28 Fabricação de máquinas e equipamentos":"3.28_Maquinas_equipamentos_br",
                                "3.29 Fabricação de veículos automotores, reboques e carrocerias":"3.29_Veículos_br",
                                "3.30 Fabricação de outros equipamentos de transporte, exceto veículos automotores":"3.30_outros_transporte_br",
                                "3.31 Fabricação de móveis":"3.31_Móveis_br",
                                "3.32 Fabricação de produtos diversos":"3.32_Diversos_br",
                                "3.33 Manutenção, reparação e instalação de máquinas e equipamentos":"3.33_Manutenção_br"
                               }
    ))

#variavel Produção Física Industrial BR já dessazonalizada, por seções e atividades industriais mensal % a.m.
listVariables.append(Variables('pim_pf_mensal_br_dessazonalizado',"8888-12607-br","sidra",
                               {"periodos":"-500","variaveis":"12607","localidade":"N1[all]","classificacao":"544[all]"},
                               ["getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "1 Indústria geral":"1_Geral_br",
                                "2 Indústrias extrativas":"2_Extrativa_br",
                                "3 Indústrias de transformação":"3_Transformacao_br",
                                "3.10 Fabricação de produtos alimentícios":"3.10_Alimentícios_br",
                                "3.11 Fabricação de bebidas":"3.11_Bebidas_br",
                                "3.12 Fabricação de produtos do fumo":"3.12_Fumo_br", 
                                "3.13 Fabricação de produtos têxteis":"3.13_Têxteis_br",
                                "3.14 Confecção de artigos do vestuário e acessórios":"3.14_confecções_br",
                                "3.15 Preparação de couros e fabricação de artefatos de couro, artigos para viagem e calçados":"3.15_Couro_br",
                                "3.16 Fabricação de produtos de madeira":"3.16_Madeira_br",
                                "3.17 Fabricação de celulose, papel e produtos de papel":"3.17_Celulose_br",
                                "3.18 Impressão e reprodução de gravações":"3.18_Gravações_br",
                                "3.19 Fabricação de coque, de produtos derivados do petróleo e de biocombustíveis":"3.19_combustiveis_br",
                                "3.20 Fabricação de produtos químicos":"3.20_Químicos_br",
                                "3.21 Fabricação de produtos farmoquímicos e farmacêuticos":"3.21_Farmo_br",
                                "3.22 Fabricação de produtos de borracha e de material plástico":"3.22_Borracha_Plástico_br",
                                "3.23 Fabricação de produtos de minerais não metálicos":"3.23_Minerais_nâo_metálicos_br",
                                "3.24 Metalurgia":"3.24_Metalurgia_br",
                                "3.25 Fabricação de produtos de metal, exceto máquinas e equipamentos":"3.25_Produtos_metal_br",
                                "3.26 Fabricação de equipamentos de informática, produtos eletrônicos e ópticos":"3.26_info_eletro_optico_br",
                                "3.27 Fabricação de máquinas, aparelhos e materiais elétricos":"3.27_Materiais_elétricos_br",
                                "3.28 Fabricação de máquinas e equipamentos":"3.28_Maquinas_equipamentos_br",
                                "3.29 Fabricação de veículos automotores, reboques e carrocerias":"3.29_Veículos_br",
                                "3.30 Fabricação de outros equipamentos de transporte, exceto veículos automotores":"3.30_outros_transporte_br",
                                "3.31 Fabricação de móveis":"3.31_Móveis_br",
                                "3.32 Fabricação de produtos diversos":"3.32_Diversos_br",
                                "3.33 Manutenção, reparação e instalação de máquinas e equipamentos":"3.33_Manutenção_br"                            
                               }
    ))

#variavel Produção Física Industrial de SC já dessazonalizada, por seções e atividades industriais mensal % a.m.
listVariables.append(Variables('pim_pf_mensal_br_dessazonalizado_single',"8888-12607-br-single","sidra",
                               {"periodos":"-500","variaveis":"12607","localidade":"N1[all]","classificacao":"544[129314]"},
                               ["getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "1 Indústria geral":"1_Geral_br"
                                 }
    ))

#PMS
#pesquisa nacional de serviços volume por atividades e subdivisões mensal % a.m.
listVariables.append(Variables('pms_volume_mensal_br',"8688-7167-br","sidra",
                               {"periodos":"-500","variaveis":"7167","localidade":"N1[all]","classificacao":"11046[56726]|12355[all]"},
                               ["seasonal","","seasonal_getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "Total":"total_br",
                                "1. Serviços prestados às famílias":"1_Prestados_às_famílias_br",
                                "1.1 Serviços de alojamento e alimentação":"1.1_Alojamento_alimentção_br",
                                "1.1.1 Alojamento":"1.1.1_Alojamento_br",
                                "1.1.2 Alimentação":"1.1.2_Alimentação_br",
                                "1.2 Outros serviços prestados às famílias":"1.2_Outros_famílias_br",
                                "2. Serviços de informação e comunicação":"2_Informação_comunicação_br",
                                "2.1 Serviços de Tecnologia de Informação e Comunicação (TIC)":"2.1_Tecno__Info_comu_br",
                                "2.1.1 Telecomunicações":"2.1.1_Telecomunicações_br",
                                "2.1.2 Serviços de Tecnologia da Informação":"2.1.2_Tecno_info_br",
                                "2.2 Serviços audiovisuais, de edição e agências de notícias":"2.2_Audiovisuais_br",
                                "3. Serviços profissionais, administrativos e complementares":"3_Profi_adm_compl_br",
                                "3.1 Serviços técnico-profissionais":"3.1_Técnico-profi_br",
                                "3.2 Serviços administrativos e complementares":"3.2_Adm_compl_br",
                                "3.2.1 Aluguéis não imobiliários":"3.2.1_Aluguel_não_imobi_br",
                                "3.2.2 Serviços de apoio às atividades empresariais":"3.2.2_Apoio_empresarial_br",
                                "4. Transportes, serviços auxiliares aos transportes e correio":"4_Transporte_auxiliar_br",
                                "4.1 Transporte terrestre":"4.1_Transporte_terrestre_br",
                                "4.1.1 Rodoviário de cargas":"4.1.1_Rodoviário_cargas_br",
                                "4.1.2 Rodoviário de passageiros":"4.1.1_Rodoviário_passageiros_br",
                                "4.1.3 Outros segmentos do transporte terrestre":"4.1.3_Outros_terrestre_br",
                                "4.2 Transporte aquaviário":"4.2_Transporte_aquaviário_br",
                                "4.3 Transporte aéreo":"4.3_Transporte_aéreo_br",
                                "4.4 Armazenagem, serviços auxiliares aos transportes e correio":"4.4_Armazenagem_auxiliar_br",
                                "5. Outros serviços":"5_outros_br",
                                "5.1 Esgoto, gestão de resíduos, recuperação de materiais e descontaminação":"5.1_Esgoto_br",
                                "5.2 Atividades auxiliares dos serviços financeiros":"5.2_Auxiliar_financeiro_br",
                                "5.3 Atividades imobiliárias":"5.3_Atividade_imobiliária_br",
                                "5.4 Outros serviços não especificados anteriormente":"5.4_Outros_não_especificados_br"
                                }
    ))

#pesquisa mensal de serviços volume por atividades e subdivisões dessazonalizado mensal % a.m.
listVariables.append(Variables('pms_volume_mensal_br_dessazonalizado',"8688-7168-br","sidra",
                               {"periodos":"-500","variaveis":"7168","localidade":"N1[all]","classificacao":"11046[56726]|12355[all]"},
                               ["getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "Total":"total_br",
                                "1. Serviços prestados às famílias":"1_Prestados_às_famílias_br",
                                "1.1 Serviços de alojamento e alimentação":"1.1_Alojamento_alimentção_br",
                                "1.1.1 Alojamento":"1.1.1_Alojamento_br",
                                "1.1.2 Alimentação":"1.1.2_Alimentação_br",
                                "1.2 Outros serviços prestados às famílias":"1.2_Outros_famílias_br",
                                "2. Serviços de informação e comunicação":"2_Informação_comunicação_br",
                                "2.1 Serviços de Tecnologia de Informação e Comunicação (TIC)":"2.1_Tecno__Info_comu_br",
                                "2.1.1 Telecomunicações":"2.1.1_Telecomunicações_br",
                                "2.1.2 Serviços de Tecnologia da Informação":"2.1.2_Tecno_info_br",
                                "2.2 Serviços audiovisuais, de edição e agências de notícias":"2.2_Audiovisuais_br",
                                "3. Serviços profissionais, administrativos e complementares":"3_Profi_adm_compl_br",
                                "3.1 Serviços técnico-profissionais":"3.1_Técnico-profi_br",
                                "3.2 Serviços administrativos e complementares":"3.2_Adm_compl_br",
                                "3.2.1 Aluguéis não imobiliários":"3.2.1_Aluguel_não_imobi_br",
                                "3.2.2 Serviços de apoio às atividades empresariais":"3.2.2_Apoio_empresarial_br",
                                "4. Transportes, serviços auxiliares aos transportes e correio":"4_Transporte_auxiliar_br",
                                "4.1 Transporte terrestre":"4.1_Transporte_terrestre_br",
                                "4.1.1 Rodoviário de cargas":"4.1.1_Rodoviário_cargas_br",
                                "4.1.2 Rodoviário de passageiros":"4.1.1_Rodoviário_passageiros_br",
                                "4.1.3 Outros segmentos do transporte terrestre":"4.1.3_Outros_terrestre_br",
                                "4.2 Transporte aquaviário":"4.2_Transporte_aquaviário_br",
                                "4.3 Transporte aéreo":"4.3_Transporte_aéreo_br",
                                "4.4 Armazenagem, serviços auxiliares aos transportes e correio":"4.4_Armazenagem_auxiliar_br",
                                "5. Outros serviços":"5_outros_br",
                                "5.1 Esgoto, gestão de resíduos, recuperação de materiais e descontaminação":"5.1_Esgoto_br",
                                "5.2 Atividades auxiliares dos serviços financeiros":"5.2_Auxiliar_financeiro_br",
                                "5.3 Atividades imobiliárias":"5.3_Atividade_imobiliária_br",
                                "5.4 Outros serviços não especificados anteriormente":"5.4_Outros_não_especificados_br"
                                }
    ))

#pesquisa mensal de serviços - indice do volume de serviços dessazonalizado BR % a.m.
listVariables.append(Variables('pms_volume_serviços_br_dessazonalizado',"5906-7168-br","sidra",
                               {"periodos":"-500","variaveis":"7168","localidade":"N1[all]","classificacao":"11046[56726]"},
                               ["getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "Índice de volume de serviços":"pms_volume_serviços_br_desazonalizado"
                                }
    ))

#pesquisa mensal de serviços - indice do volume de serviços SC % a.m.
listVariables.append(Variables('pms_volume_serviços_sc',"5906-7167-sc","sidra",
                               {"periodos":"-500","variaveis":"7167","localidade":"N3[42]","classificacao":"11046[56726]"},
                               ["seasonal","seasonal_getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "Índice de volume de serviços":"pms_volume_serviços_sc"
                                }
    ))

#pesquisa mensal de serviços - indice do volume de serviços dessazonalizado BR % a.m.
listVariables.append(Variables('pms_volume_serviços_sc_dessazonalizado',"5906-7168-sc","sidra",
                               {"periodos":"-500","variaveis":"7168","localidade":"N3[42]","classificacao":"11046[56726]"},
                               ["getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "Índice de volume de serviços":"pms_volume_serviços_sc_desazonalizado"
                                }
    ))

#PMC
#pesquisa mensal de comercio - indice do volume de  vendas no comercio varejista BR % a.m.
listVariables.append(Variables('pmc_volume_varejista_br',"8880-7169-br","sidra",
                               {"periodos":"-500","variaveis":"7169","localidade":"N1[all]","classificacao":"11046[56734]"},
                               ["getallbases","seasonal_getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "Índice de volume de vendas no comércio varejista":"pmc_volume_varejista_br"
                                }
    ))

#pesquisa mensal de comercio - indice do volume de  vendas no comercio varejista dessazonalizado BR % a.m.
listVariables.append(Variables('pmc_volume_varejista_br_dessazonalizado',"8880-7170-br","sidra",
                               {"periodos":"-500","variaveis":"7170","localidade":"N1[all]","classificacao":"11046[56734]"},
                               ["getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "Índice de volume de vendas no comércio varejista":"pmc_volume_varejista_br_desazonalizado"
                                }
    ))

#pesquisa mensal de comercio - indice do volume de  vendas no comercio varejista SC % a.m.
listVariables.append(Variables('pmc_volume_varejista_sc',"8880-7169-sc","sidra",
                               {"periodos":"-500","variaveis":"7169","localidade":"N3[42]","classificacao":"11046[56734]"},
                               ["seasonal","seasonal_getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "Índice de volume de vendas no comércio varejista":"pmc_volume_varejista_sc"
                                }
    ))

#pesquisa mensal de comercio - indice do volume de  vendas no comercio varejista dessazonalizado SC % a.m.
listVariables.append(Variables('pmc_volume_varejista_sc_dessazonalizado',"8880-7170-sc","sidra",
                               {"periodos":"-500","variaveis":"7170","localidade":"N3[42]","classificacao":"11046[56734]"},
                               ["getallbases","variation"],{"variation":"12"},
                               {"date":"date",
                                "Índice de volume de vendas no comércio varejista":"pmc_volume_varejista_sc_dessazonalizado"
                                }
    ))

#PIM PF Grandes Categorias
#variavel produção fisica industrial por grandes categorias economicas (bens de capital/intermediarios/duraveis e tals) % a.m.
listVariables.append(Variables('pim_pf_bens_categorias',"8887-12606","sidra",
                               {"periodos":"-500","variaveis":"12606","localidade":"N1[all]","classificacao":"543[all]"},
                               ["seasonal","seasonal_getallbases"],{},
                               {"date":"date",
                                "1 Bens de capital":"1._Bens_capital",
                                "110 Bens de capital, exceto equipamentos de transporte industrial":"1.1 Bens_capital_exceto_equipamentos_transporte",
                                "120 Equipamentos de transporte industrial":"1.2_Equipamentos_transporte,",
                                "2 Bens intermediários":"2._Bens_intermediários",
                                "210 Alimentos e bebidas básicos, destinados principalmente à indústria":"2.1_Alimentos_bebidas_básicos_indústria",
                                "220 Alimentos e bebidas elaborados, destinados principalmente à indústria":"2.2_Alimentos_bebidas_elaborados_indústria",
                                "230 Insumos industriais básicos":"2.3_Insumos_básicos",
                                "240 Insumos industriais elaborados":"2.4_Insumos_elaborados",
                                "250 Combustíveis e lubrificantes básicos":"2.5_Combustíveis_básicos",
                                "260 Combustíveis e lubrificantes elaborados - exceto gasolinas para automóvel":"2.6_Combustíveis_elaborados_exceto_gasolina",
                                "270 Peças e acessórios para bens de capital":"2.7_Peças_acessórios_bens_capital",
                                "280 Peças e acessórios para equipamentos de transporte":"2.8_Peças_acessórios_equipamentos_transporte",
                                "3 Bens de consumo":"3._Bens_consumo",
                                "31 Bens de consumo duráveis":"3.1_Bens_consumo_duráveis",
                                "311 Bens de consumo duráveis - exceto automóveis para passageiros e equipamentos de transporte não industrial":"3.1.1_duráveis_exceto_automóveis",
                                "312 Automóveis para passageiros":"3.1.2_Automóveis",
                                "313 Equipamentos de transporte não industrial":"3.1.3_Equipamentos_transporte",
                                "32 Bens de consumo semiduráveis e não duráveis":"3.2_Bens_consumo_semiduráveis_não_duráveis",
                                "321 Bens de consumo semiduráveis":"3.2.1_semiduráveis",
                                "322 Bens de consumo não duráveis":"3.2.2_duráveis",
                                "323 Alimentos e bebidas básicos, destinados principalmente ao consumo doméstico":"3.2.3_Alimentos_bebidas_básicos_consumo",
                                "324 Alimentos e bebidas elaborados, destinados principalmente ao consumo doméstico":"3.2.4_Alimentos_bebidas_elaborados_consumo",
                                "325 Gasolinas para automóvel (motor spirit)":"3.2.5_Gasolinas",
                                "9 Bens não especificados anteriormente":"9_Outros"
                                }
    ))

#variavel produção fisica industrial por grandes categorias economicas (bens de capital/intermediarios/duraveis e tals) % a.m.
listVariables.append(Variables('pim_pf_bens_categorias_dessazonalizado',"8887-12607","sidra",
                               {"periodos":"-500","variaveis":"12607","localidade":"N1[all]","classificacao":"543[all]"},
                               ["getallbases"],{},
                               {"date":"date",
                                "1 Bens de capital":"1._Bens_capital",
                                "110 Bens de capital, exceto equipamentos de transporte industrial":"1.1 Bens_capital_exceto_equipamentos_transporte",
                                "120 Equipamentos de transporte industrial":"1.2_Equipamentos_transporte,",
                                "2 Bens intermediários":"2._Bens_intermediários",
                                "210 Alimentos e bebidas básicos, destinados principalmente à indústria":"2.1_Alimentos_bebidas_básicos_indústria",
                                "220 Alimentos e bebidas elaborados, destinados principalmente à indústria":"2.2_Alimentos_bebidas_elaborados_indústria",
                                "230 Insumos industriais básicos":"2.3_Insumos_básicos",
                                "240 Insumos industriais elaborados":"2.4_Insumos_elaborados",
                                "250 Combustíveis e lubrificantes básicos":"2.5_Combustíveis_básicos",
                                "260 Combustíveis e lubrificantes elaborados - exceto gasolinas para automóvel":"2.6_Combustíveis_elaborados_exceto_gasolina",
                                "270 Peças e acessórios para bens de capital":"2.7_Peças_acessórios_bens_capital",
                                "280 Peças e acessórios para equipamentos de transporte":"2.8_Peças_acessórios_equipamentos_transporte",
                                "3 Bens de consumo":"3._Bens_consumo",
                                "31 Bens de consumo duráveis":"3.1_Bens_consumo_duráveis",
                                "311 Bens de consumo duráveis - exceto automóveis para passageiros e equipamentos de transporte não industrial":"3.1.1_duráveis_exceto_automóveis",
                                "312 Automóveis para passageiros":"3.1.2_Automóveis",
                                "313 Equipamentos de transporte não industrial":"3.1.3_Equipamentos_transporte",
                                "32 Bens de consumo semiduráveis e não duráveis":"3.2_Bens_consumo_semiduráveis_não_duráveis",
                                "321 Bens de consumo semiduráveis":"3.2.1_semiduráveis",
                                "322 Bens de consumo não duráveis":"3.2.2_duráveis",
                                "323 Alimentos e bebidas básicos, destinados principalmente ao consumo doméstico":"3.2.3_Alimentos_bebidas_básicos_consumo",
                                "324 Alimentos e bebidas elaborados, destinados principalmente ao consumo doméstico":"3.2.4_Alimentos_bebidas_elaborados_consumo",
                                "325 Gasolinas para automóvel (motor spirit)":"3.2.5_Gasolinas",
                                "9 Bens não especificados anteriormente":"9_Outros"
                                }
    ))

#descoupação
#variavel Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade (%) Total, Trimestre Móvel % a.m.
listVariables.append(Variables('taxa_desocupacao_mensal_trimestre_movel',"6381-4099-br","sidra",
                               {"periodos":"-500","variaveis":"4099","localidade":"N1[all]","classificacao":""},[""],{},
                               {"date":"date",
                                "Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade":"taxa_desocupacao_mensal_trimestre_movel"
                                }
    ))

#variavel Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade (%) Total de SC, Trimestre Móvel % a.m.
listVariables.append(Variables('taxa_desocupacao_mensal_trimestre_movel_sc',"6468-4099-sc","sidra",
                               {"periodos":"-500","variaveis":"4099","localidade":"N3[42]","classificacao":""},["trimestertomonth"],{"trimestertomonth":True},
                               {"date":"date",
                                "Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade":"taxa_desocupacao_mensal_trimestre_movel_sc"
                                }
    ))

#rendimento
#variavel Rendimento médio mensal real, efetivamente recebido em todos os trabalhos % a.m.
listVariables.append(Variables('rendimento_medio_mensal',"6387-5935-br","sidra",
                               {"periodos":"-500", "variaveis":"5935","localidade":"N1[all]","classificacao":""},["seasonal"],{},
                               {"date":"date",
                                "Rendimento médio mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, efetivamente recebido em todos os trabalhos":"rendimento_medio_mensal"
                                }
    ))

#variavel Rendimento médio trimestral real, efetivamente recebido em todos os trabalhos - SC % a.t.
listVariables.append(Variables('rendimento_medio_trimestral_sc',"6469-5935-br","sidra",
                               {"periodos":"-500", "variaveis":"5935","localidade":"N3[42]","classificacao":""},["trimestertomonth_seasonal"],{"trimestertomonth":True},
                               {"date":"date",
                                "Rendimento médio mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, efetivamente recebido em todos os trabalhos":"rendimento_medio_trimestral_sc"
                                }
    ))

#variavel Massa de Rendimento mensal real, efetivamente recebido em todos os trabalhos - BR % a.m.
listVariables.append(Variables('rendimento_massa_mensal_real',"6392-6293-br","sidra",
                               {"periodos":"-500", "variaveis":"6293","localidade":"N1[all]","classificacao":""},["seasonal"],{},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_massa_mensal_real"
                                }
    ))

#variavel Massa de Rendimento trimestral real, efetivamente recebido em todos os trabalhos - BR % a.m.
listVariables.append(Variables('rendimento_massa_trimestral_real',"6474-6293-br","sidra",
                               {"periodos":"-500","variaveis":"6293","localidade":"N1[all]","classificacao":""},["trimestertomonth_seasonal"],{"trimestertomonth":True},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_massa_trimestral_real"
                                }
    ))

#variavel Massa de Rendimento trimestral real, efetivamente recebido em todos os trabalhos - SC % a.m.
listVariables.append(Variables('rendimento_massa_trimestral_real_sc',"6474-6293-sc","sidra",
                               {"periodos":"-500","variaveis":"6293","localidade":"N3[42]","classificacao":""},["trimestertomonth_seasonal"],{"trimestertomonth":True},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_massa_trimestral_real_sc"
                                }
    ))

#despesa de consumo das familias
#variavel PIB despesa de consumo das familias Valores encadeados a preços de 1995 % a.t.
listVariables.append(Variables('pib_consumo_familias_trimestral',"6612-9318-br","sidra",
                               {"periodos":"-500", "variaveis":"9318","localidade":"N1[all]","classificacao":"11255[93404]"},["trimestertomonth"],{"trimestertomonth":True},
                               {"date":"date",
                                "Despesa de consumo das famílias": "pib_consumo_familias_trimestral_base_fixa",
                                }
    ))

#variavel PIB despesa de consumo das familias Valores encadeados a preços de 1995 % a.t.
listVariables.append(Variables('pib_consumo_familias_trimestral_dessazonalizado',"6613-9319-br","sidra",
                               {"periodos":"-500", "variaveis":"9319","localidade":"N1[all]","classificacao":"11255[93404]"},["trimestertomonth"],{"trimestertomonth":True},
                               {"date":"date",
                                "Despesa de consumo das famílias": "pib_consumo_familias_trimestral_base_fixa_dessazonalizado",
                                }
    ))


#models estabelecidos


#model ipca para o power BI
listModels.append(Models('ipca_evolucao',"'2000-01-01'", "",
                         ["ipca_mensal_taxa_variação_rolling",
                          "ipca_mensal_taxa_preços_livres_serviços_rolling",
                          "ipca_mensal_taxa_núcleo_médias_aparadas_suavização_rolling",
                          "ipca_mensal_taxa_núcleo_exclusão_rolling",
                          "expectativa_ipca_2024_latest_transpose_rolling",
                          "expectativa_ipca_servicos_2024_latest_transpose_rolling",
                          "meta_inflacao",
                          "expectativa_ipca_2024_firstdayofmonth_transpose_rolling",
                          "expectativa_ipca_servicos_2024_firstdayofmonth_transpose_rolling"
                          ],
                         ["date"]
    
    ))

#model produção setorial para power BI
listModels.append(Models('producao_setorial',"'2003-01-01'", "",
                         ["ibc_br_mensal_dessazonalizado_getallbases",
                          "ibcr_sc_mensal_dessazonalizado_getallbases",
                          "pim_pf_mensal_br_dessazonalizado_getallbases",
                          "pim_pf_mensal_sc_dessazonalizado_getallbases",
                          "pim_pf_mensal_sc_seasonal_getallbases"
                          ],
                         ["dateBase","date"]
    
    ))

#model serviços setorial para power BI
listModels.append(Models('servicos_setorial',"'2011-01-01'", "",
                         ["ibc_br_mensal_dessazonalizado_getallbases",
                          "pms_volume_mensal_br_dessazonalizado_getallbases"
                          ],
                         ["dateBase","date"]
    
    ))

#model rendimentos para power BI
listModels.append(Models('rendimentos',"'2012-01-01'", "",
                         ["rendimento_massa_mensal_real",
                          "rendimento_medio_mensal",
                          "rendimento_medio_mensal_seasonal",
                          "rendimento_massa_trimestral_real_sc_trimestertomonth",
                          "rendimento_medio_trimestral_sc_trimestertomonth",
                          "rendimento_medio_trimestral_sc_trimestertomonth_seasonal"
                          ],
                         ["date"]
    
    ))

#model evolução grandes setores para power BI
listModels.append(Models('grandes_setores',"'2011-01-01'", "",
                         ["pim_pf_mensal_br_dessazonalizado_single_getallbases",
                          "pms_volume_serviços_br_dessazonalizado_getallbases",
                          "pmc_volume_varejista_br_dessazonalizado_getallbases",
                          "pim_pf_mensal_sc_dessazonalizado_getallbases",
                          "pms_volume_serviços_sc_dessazonalizado_getallbases",
                          "pmc_volume_varejista_sc_dessazonalizado_getallbases"
                          ],
                         ["dateBase","date"]
    
    ))

#model bens para power BI
listModels.append(Models('bens',"'2002-01-01'", "",
                         ["pim_pf_bens_categorias_dessazonalizado_getallbases"
                          ],
                         ["dateBase","date"]
    
    ))


