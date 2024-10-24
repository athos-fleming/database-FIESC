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
                               "01/01/1992",[""],{},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_médias_aparadas_suavização"}
    ))

#variavel IPCA - núcleo médias aparadas sem suavização - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_médias_aparadas_sem_suavização',"'BM12_IPCA20N12'","ipea",
                               "01/01/1992",[""],{},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_médias_aparadas_sem_suavização"}
    ))

#variavel IPCA - núcleo por exclusão - EX1 - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_exclusão',"'BM12_IPCAEXCEX212'","ipea",
                               "01/01/1992",[""],{},
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
                               "01/01/2003",["seasonal_getallbases"],{},
                               {"VALDATA": "date","VALVALOR": "ibc_br_mensal"}
    ))

#IBC-BR dessazonalizado % a.m.
listVariables.append(Variables('ibc_br_mensal_dessazonalizado',"'SGS12_IBCBRDESSAZ12'","ipea",
                               "01/01/2003",[""],{},
                               {"VALDATA": "date","VALVALOR": "ibc_br_mensal_dessazonalizado"}
    ))

#PIB consumo final das familias % a.t.
listVariables.append(Variables('pib_consumo_familias_trimestral_corrente',"'SCN104_CFPPN104'","ipea",
                               "01/01/2003",[""],{},
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
                               "01/01/2003",["seasonal","seasonal_getallbases"],{""},
                               {"data": "date","valor": "ibcr_sc_mensal"}
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



#variavel Produção Física Industrial de SC, por seções e atividades industriais mensal % a.m.
listVariables.append(Variables('pim_pf_mensal_sc',"8888-12606-sc","sidra",
                               {"periodos":"-500","variaveis":"12606","localidade":"N3[42]","classificacao":"544[all]"},
                               ["seasonal","seasonal_getallbases"],{},
                               {"date":"date",
                                "1 Indústria geral":"1_Industria_Geral_sc",
                                "2 Indústrias extrativas":"2_Industria_Extrativa_sc",
                                "3 Indústrias de transformação":"3_Industrias_Transformacao_sc",
                                "3.10 Fabricação de produtos alimentícios":"3.10_Alimenticios_sc",
                                "3.11 Fabricação de bebidas":"3.11_bebidas_sc",
                                "3.12 Fabricação de produtos do fumo":"3.12_fumo_sc",
                                "3.13 Fabricação de produtos têxteis":"3.13_texteis_sc",
                                "3.14 Confecção de artigos do vestuário e acessórios":"3.14_confeccoes_sc",
                                "3.15 Preparação de couros e fabricação de artefatos de couro, artigos para viagem e calçados":"3.15_couro_sc",
                                "3.16 Fabricação de produtos de madeira":"3.16_madeira_sc",
                                "3.17 Fabricação de celulose, papel e produtos de papel":"3.17_celulose_sc",
                                "3.18 Impressão e reprodução de gravações":"3.18_gravacoes_sc",
                                "3.19 Fabricação de coque, de produtos derivados do petróleo e de biocombustíveis":"3.19_petroleo_biocombustiveis_sc",
                                "3.20 Fabricação de produtos químicos":"3.20_quimicos_sc",
                                "3.21 Fabricação de produtos farmoquímicos e farmacêuticos":"3.21_farmoquimicos_farmaceuticos_sc",
                                "3.22 Fabricação de produtos de borracha e de material plástico":"3.22_borracha_plastico_sc",
                                "3.23 Fabricação de produtos de minerais não metálicos":"3.23_minerais_nao_metalicos_sc",
                                "3.24 Metalurgia":"3.24_Metalurgia_sc",
                                "3.25 Fabricação de produtos de metal, exceto máquinas e equipamentos":"3.25_metal_exceto_maquinas_equipamentos_sc",
                                "3.26 Fabricação de equipamentos de informática, produtos eletrônicos e ópticos":"3.26_informática_eletrônicos_opticos_sc",
                                "3.27 Fabricação de máquinas, aparelhos e materiais elétricos":"3.27_maquinas_aparelhos_eletricos_sc",
                                "3.28 Fabricação de máquinas e equipamentos":"3.28_maquinas_equipamentos_sc",
                                "3.29 Fabricação de veículos automotores, reboques e carrocerias":"3.29_veiculos_sc",
                                "3.30 Fabricação de outros equipamentos de transporte, exceto veículos automotores":"3.30_outros_transporte_sc",
                                "3.31 Fabricação de móveis":"3.31_moveis_sc",
                                "3.32 Fabricação de produtos diversos":"3.32_diversos_sc",
                                "3.33 Manutenção, reparação e instalação de máquinas e equipamentos":"3.33_Manutenção_maquinas_equipamentos_sc"                            
                               }
    ))

#variavel Produção Física Industrial BR, por seções e atividades industriais mensal % a.m.
listVariables.append(Variables('pim_pf_mensal_br',"8888-12606-br","sidra",
                               {"periodos":"-500","variaveis":"12606","localidade":"N1[all]","classificacao":"544[all]"},
                               ["seasonal","","seasonal_getallbases"],{},
                               {"date":"date",
                                "1 Indústria geral":"1_Industria_Geral_br",
                                "2 Indústrias extrativas":"2_Industria_Extrativa_br",
                                "3 Indústrias de transformação":"3_Industrias_Transformacao_br",
                                "3.10 Fabricação de produtos alimentícios":"3.10_Alimenticios_br",
                                "3.11 Fabricação de bebidas":"3.11_bebidas_br",
                                "3.12 Fabricação de produtos do fumo":"3.12_fumo_br",
                                "3.13 Fabricação de produtos têxteis":"3.13_texteis_br",
                                "3.14 Confecção de artigos do vestuário e acessórios":"3.14_confeccoes_br",
                                "3.15 Preparação de couros e fabricação de artefatos de couro, artigos para viagem e calçados":"3.15_couro_br",
                                "3.16 Fabricação de produtos de madeira":"3.16_madeira_br",
                                "3.17 Fabricação de celulose, papel e produtos de papel":"3.17_celulose_br",
                                "3.18 Impressão e reprodução de gravações":"3.18_gravacoes_br",
                                "3.19 Fabricação de coque, de produtos derivados do petróleo e de biocombustíveis":"3.19_petroleo_biocombustiveis_br",
                                "3.20 Fabricação de produtos químicos":"3.20_quimicos_br",
                                "3.21 Fabricação de produtos farmoquímicos e farmacêuticos":"3.21_farmoquimicos_farmaceuticos_br",
                                "3.22 Fabricação de produtos de borracha e de material plástico":"3.22_borracha_plastico_br",
                                "3.23 Fabricação de produtos de minerais não metálicos":"3.23_minerais_nao_metalicos_br",
                                "3.24 Metalurgia":"3.24_Metalurgia_br",
                                "3.25 Fabricação de produtos de metal, exceto máquinas e equipamentos":"3.25_metal_exceto_maquinas_equipamentos_br",
                                "3.26 Fabricação de equipamentos de informática, produtos eletrônicos e ópticos":"3.26_informática_eletrônicos_opticos_br",
                                "3.27 Fabricação de máquinas, aparelhos e materiais elétricos":"3.27_maquinas_aparelhos_eletricos_br",
                                "3.28 Fabricação de máquinas e equipamentos":"3.28_maquinas_equipamentos_br",
                                "3.29 Fabricação de veículos automotores, reboques e carrocerias":"3.29_veiculos_br",
                                "3.30 Fabricação de outros equipamentos de transporte, exceto veículos automotores":"3.30_outros_transporte_br",
                                "3.31 Fabricação de móveis":"3.31_moveis_br",
                                "3.32 Fabricação de produtos diversos":"3.32_diversos_br",
                                "3.33 Manutenção, reparação e instalação de máquinas e equipamentos":"3.33_Manutenção_maquinas_equipamentos_br"                            
                               }
    ))

#pesquisa nacional de serviços volume por atividades e subdivisões mensal % a.m.
listVariables.append(Variables('pms_br_volume_mensal',"8688-7167-volume","sidra",
                               {"periodos":"-500","variaveis":"7167","localidade":"N1[all]","classificacao":"11046[56726]|12355[all]"},
                               ["seasonal","","seasonal_getallbases"],{},
                               {"date":"date",
                                "Total":"total",
                                "1. Serviços prestados às famílias":"1_prestados_familias",
                                "1.1 Serviços de alojamento e alimentação":"1.1_alojamento_alimentacao",
                                "1.1.1 Alojamento":"1.1.1_Alojamento",
                                "1.1.2 Alimentação":"1.1.2_Alimentacao",
                                "1.2 Outros serviços prestados às famílias":"1.2_outros_prestados_familias",
                                "2. Serviços de informação e comunicação":"2_informacao_comunicacao",
                                "2.1 Serviços de Tecnologia de Informação e Comunicação (TIC)":"2.1_tecnologia__informacao_comunicacao",
                                "2.1.1 Telecomunicações":"2.1.1_telecomunicacoes",
                                "2.1.2 Serviços de Tecnologia da Informação":"2.1.2_tecnologia_informacao",
                                "2.2 Serviços audiovisuais, de edição e agências de notícias":"2.2_audiovisuais_edicao_agencias_noticias",
                                "3. Serviços profissionais, administrativos e complementares":"3_profissionais_administrativos_complementares",
                                "3.1 Serviços técnico-profissionais":"3.1__tecnico_profissionais",
                                "3.2 Serviços administrativos e complementares":"3.2_administrativos_complementares",
                                "3.2.1 Aluguéis não imobiliários":"3.2.1_Alugueis_nao_imobiliarios",
                                "3.2.2 Serviços de apoio às atividades empresariais":"3.2.2_apoio_atividades_empresariais",
                                "4. Transportes, serviços auxiliares aos transportes e correio":"4_transportes_auxiliares_transportes_correio",
                                "4.1 Transporte terrestre":"4.1_transporte_terrestre",
                                "4.1.1 Rodoviário de cargas":"4.1.1_rodoviario_cargas",
                                "4.1.2 Rodoviário de passageiros":"4.1.2_rodoviario_passageiros",
                                "4.1.3 Outros segmentos do transporte terrestre":"4.1.3_outros_segmentos_transporte_terrestre",
                                "4.2 Transporte aquaviário":"4.2_transporte_aquaviario",
                                "4.3 Transporte aéreo":"4.3_transporte_aereo",
                                "4.4 Armazenagem, serviços auxiliares aos transportes e correio":"4.4_armazenagem_auxiliares_transportes_correio",
                                "5. Outros serviços":"5_outros",
                                "5.1 Esgoto, gestão de resíduos, recuperação de materiais e descontaminação":"5.1_esgoto_gestao_residuos_recuperacao_materiais_descontaminacao",
                                "5.2 Atividades auxiliares dos serviços financeiros":"5.2_auxiliares_financeiros",
                                "5.3 Atividades imobiliárias":"5.3_atividade_imobiliarias",
                                "5.4 Outros serviços não especificados anteriormente":"5.4_outros_nao_especificados"
                                }
    ))

#variavel Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade (%) Total, Trimestre Móvel % a.m.
listVariables.append(Variables('taxa_desocupacao_mensal_trimestre_movel',"6381-4099-br","sidra",
                               {"periodos":"-500","variaveis":"4099","localidade":"N1[all]","classificacao":""},[""],{},
                               {"date":"date",
                                "Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade":"taxa_desocupacao_mensal_trimestre_movel"
                                }
    ))

#variavel Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade (%) Total de SC, Trimestre Móvel % a.m.
listVariables.append(Variables('taxa_desocupacao_mensal_trimestre_movel_sc',"6468-4099-sc","sidra",
                               {"periodos":"-500","variaveis":"4099","localidade":"N3[42]","classificacao":""},[""],{},
                               {"date":"date",
                                "Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade":"taxa_desocupacao_mensal_trimestre_movel_sc"
                                }
    ))

#variavel Rendimento médio mensal real, efetivamente recebido em todos os trabalhos % a.m.
listVariables.append(Variables('rendimento_medio_mensal_todos_trabalhos',"6387-5935-br","sidra",
                               {"periodos":"-500", "variaveis":"5935","localidade":"N1[all]","classificacao":""},["seasonal"],{},
                               {"date":"date",
                                "Rendimento médio mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, efetivamente recebido em todos os trabalhos":"rendimento_medio_mensal_todos_trabalhos"
                                }
    ))

#variavel Rendimento médio trimestral real, efetivamente recebido em todos os trabalhos - SC % a.t.
listVariables.append(Variables('rendimento_medio_trimestral_todos_trabalhos_sc',"6469-5935-br","sidra",
                               {"periodos":"-500", "variaveis":"5935","localidade":"N3[42]","classificacao":""},[""],{},
                               {"date":"date",
                                "Rendimento médio mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, efetivamente recebido em todos os trabalhos":"rendimento_medio_trimestral_todos_trabalhos_sc"
                                }
    ))

#variavel Massa de Rendimento mensal real, efetivamente recebido em todos os trabalhos - BR % a.m.
listVariables.append(Variables('rendimento_massa_mensal_real_todos_trabalhos',"6392-6293-br","sidra",
                               {"periodos":"-500", "variaveis":"6293","localidade":"N1[all]","classificacao":""},[""],{},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_massa_mensal_real_todos_trabalhos"
                                }
    ))

#variavel Massa de Rendimento trimestral real, efetivamente recebido em todos os trabalhos - BR % a.m.
listVariables.append(Variables('rendimento_massa_trimestral_real_todos_trabalhos',"6474-6293-br","sidra",
                               {"periodos":"-500","variaveis":"6293","localidade":"N1[all]","classificacao":""},[""],{},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_massa_trimestral_real_todos_trabalhos"
                                }
    ))

#variavel Massa de Rendimento trimestral real, efetivamente recebido em todos os trabalhos - SC % a.m.
listVariables.append(Variables('rendimento_massa_trimestral_real_todos_trabalhos_sc',"6474-6293-sc","sidra",
                               {"periodos":"-500","variaveis":"6293","localidade":"N3[42]","classificacao":""},[""],{},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_massa_trimestral_real_todos_trabalhos_sc"
                                }
    ))


#variavel PIB despesa de consumo das familias Valores encadeados a preços de 1995 % a.t.
listVariables.append(Variables('pib_consumo_familias_trimestral_base_fixa',"6612-9318-br","sidra",
                               {"periodos":"-500", "variaveis":"9318","localidade":"N1[all]","classificacao":"11255[93404]"},[""],{},
                               {"date":"date",
                                "Despesa de consumo das famílias": "pib_consumo_familias_trimestral_base_fixa",
                                }
    ))

#variavel PIB despesa de consumo das familias Valores encadeados a preços de 1995 % a.t.
listVariables.append(Variables('pib_consumo_familias_trimestral_base_fixa_dessazonalizado',"6613-9319-br","sidra",
                               {"periodos":"-500", "variaveis":"9319","localidade":"N1[all]","classificacao":"11255[93404]"},[""],{},
                               {"date":"date",
                                "Despesa de consumo das famílias": "pib_consumo_familias_trimestral_base_fixa_dessazonalizado",
                                }
    ))


#models estabelecidos


#model para o power BI do ipca
listModels.append(Models('ipca_evolucao',"'2000-01-01'", "",
                         ["ipca_mensal_taxa_variação_rolling",
                          "ipca_mensal_taxa_preços_livres_serviços_rolling",
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
                         ["ibc_br_mensal_seasonal_getallbases",
                          "ibcr_sc_mensal_seasonal_getallbases",
                          "pim_pf_mensal_br_seasonal_getallbases",
                          "pim_pf_mensal_sc_seasonal_getallbases"
                          ],
                         ["dateBase","date"]
    
    ))

#model produção setorial para power BI
listModels.append(Models('servicos_setorial',"'2011-01-01'", "",
                         ["pms_br_volume_mensal_seasonal_getallbases"
                          ],
                         ["dateBase","date"]
    
    ))


#model trimestre para mensal
listModels.append(Models('trimestral_para_mensal',"'1996-01-01'", "",
                         ["ipca_mensal_taxa_variação",
                          "pib_consumo_familias_trimestral_base_fixa",
                          "pib_consumo_familias_trimestral_base_fixa_dessazonalizado"
                          ],
                         ["date"]
    
    ))

