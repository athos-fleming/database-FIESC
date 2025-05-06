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

#IPCA
#variavel IPCA - geral - taxa de variação  mensa % a.m.
listVariables.append(Variables('ipca_mensal_taxa_variação',"'PRECOS12_IPCAG12'","ipea",
                               "01/01/1980",["rolling"],{"rolling":"-12-MovelMensal"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_variação"}
    ))

#variavel IPCA - núcleo médias aparadas com suavização - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_médias_aparadas_suavização',"'BM12_IPCA2012'","ipea",
                               "01/01/1992",["rolling"],{"rolling":"-12-MovelMensal"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_médias_aparadas_suavização"}
    ))

#variavel IPCA - núcleo médias aparadas sem suavização - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_médias_aparadas_sem_suavização',"'BM12_IPCA20N12'","ipea",
                               "01/01/1992",[""],{},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_médias_aparadas_sem_suavização"}
    ))

#variavel IPCA - núcleo por exclusão - EX1 - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_exclusão',"'BM12_IPCAEXCEX212'","ipea",
                               "01/01/1992",["rolling"],{"rolling":"-12-MovelMensal"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_exclusão"}
    ))

#variavel IPCA - núcleo por exclusão - sem monitorados e alimentos no domicílio % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_exclusão_domiciliar',"'BM12_IPCAEXC12'","ipea",
                               "01/01/1992",[""],{},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_núcleo_exclusão_domiciliar"}
    ))

#variavel IPCA - preços livres - serviços % a.m.
listVariables.append(Variables('ipca_mensal_taxa_preços_livres_serviços',"'BM12_IPCAPLSER12'","ipea",
                               "01/01/1992",["rolling"],{"rolling":"-12-MovelMensal"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_taxa_preços_livres_serviços"}
    ))

#variavel IPCA - vestuário: taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_vestuario',"'PRECOS12_IPCAVE12'","ipea",
                               "01/01/1992",["rolling"],{"rolling":"-12-MovelMensal"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_vestuario"}
    ))

#variavel IPCA - Alimentos e bebidas: taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_alimentos_bebidas',"'PRECOS12_IPCAAB12'","ipea",
                               "01/01/1992",["rolling"],{"rolling":"-12-MovelMensal"},
                               {"VALDATA": "date","VALVALOR": "ipca_mensal_alimentos_bebidas"}
    ))


#IPP
#variavel IPP industria da transformação em Base movel % a.m.
listVariables.append(Variables('ipp_transformacao_taxa_mensal',"'IPP12_IPPCG12'","ipea",
                               "01/01/2010",["rolling"],{"rolling":"-12-MovelMensal"},
                               {"VALDATA": "date","VALVALOR": "ipp_transformacao_taxa_mensal"}
    ))

#variavel IPP industria da transformação indice dez 2018 % a.m.
listVariables.append(Variables('ipp_transformacao_basefixa',"'IPP12_IPPC12'","ipea",
                               "01/01/2010",["rolling"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_transformacao_basefixa"}
    ))

#variavel IPP industria de alimentos indice dez 2018 % a.m.
listVariables.append(Variables('ipp_alimentos_basefixa',"'IPP12_IPPC10ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_alimentos_basefixa"}
    ))

#variavel IPP industria de borracha e plástico indice dez 2018 % a.m.
listVariables.append(Variables('ipp_borracha_plastico_basefixa',"'IPP12_IPPC22ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_borracha_plastico_basefixa"}
    ))

#variavel IPP industria de madeira indice dez 2018 % a.m.
listVariables.append(Variables('ipp_madeira_basefixa',"'IPP12_IPPC16ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_madeira_basefixa"}
    ))

#variavel IPP industria de máquinas e equipamentos indice dez 2018 % a.m.
listVariables.append(Variables('ipp_maquinas_equipamentos_basefixa',"'IPP12_IPPC28ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_maquinas_equipamentos_basefixa"}
    ))

#variavel IPP industria de metalurgia indice dez 2018 % a.m.
listVariables.append(Variables('ipp_metalurgia_basefixa',"'IPP12_IPPC24ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_metalurgia_basefixa"}
    ))

#variavel IPP industria de minerais não-metálicos indice dez 2018 % a.m.
listVariables.append(Variables('ipp_minerais_não_metalicos_basefixa',"'IPP12_IPPC23ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_minerais_não_metalicos_basefixa"}
    ))

#variavel IPP industria de outros produtos químicos indice dez 2018 % a.m.
listVariables.append(Variables('ipp_outros_quimicos_basefixa',"'IPP12_IPPC20CATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_outros_quimicos_basefixa"}
    ))

#variavel IPP industria de papel e celulose indice dez 2018 % a.m.
listVariables.append(Variables('ipp_papel_celulose_basefixa',"'IPP12_IPPC17ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_papel_celulose_basefixa"}
    ))

#variavel IPP industria de petroleo indice dez 2018 % a.m.
listVariables.append(Variables('ipp_petroleo_basefixa',"'IPP12_IPPC19ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_petroleo_basefixa"}
    ))

#variavel IPP industria de metal indice dez 2018 % a.m.
listVariables.append(Variables('ipp_metal_basefixa',"'IPP12_IPPC25ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_metal_basefixa"}
    ))

#variavel IPP industria de veiculos indice dez 2018 % a.m.
listVariables.append(Variables('ipp_veiculos_basefixa',"'IPP12_IPPC29ATIV12'","ipea",
                               "01/01/2010",["rolling","getallbases"],{"rolling":"-12-basefixa"},
                               {"VALDATA": "date","VALVALOR": "ipp_veiculos_basefixa"}
    ))


#IBC-BR
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


#cambio
#Taxa de câmbio - efetiva real - fabricação de produtos alimentícios (média 2010 = 100) % a.m.
listVariables.append(Variables('cambio_alimentos',"'GAC12_TCERXTS1012'","ipea",
                               "01/01/2000",[""],{},
                               {"VALDATA": "date","VALVALOR": "cambio_alimentos"}
    ))

#Taxa de câmbio - efetiva real - fabricação de artigos do vestuário e acessórios (média 2010 = 100) % a.m.
listVariables.append(Variables('cambio_confeccao',"'GAC12_TCERXTS1412'","ipea",
                               "01/01/2000",[""],{},
                               {"VALDATA": "date","VALVALOR": "cambio_confeccao"}
    ))

#Taxa de câmbio - efetiva real - fabricação de produtos de minerais não-metálicos (média 2010 = 100) % a.m.
listVariables.append(Variables('cambio_minerais_nao_metalicos',"'GAC12_TCERXTS2312'","ipea",
                               "01/01/2000",[""],{},
                               {"VALDATA": "date","VALVALOR": "cambio_minerais_nao_metalicos"}
    ))

#	Taxa de câmbio - R$ / US$ - comercial - venda - média % a.m.
listVariables.append(Variables('cambio_media',"'BM12_ERC12'","ipea",
                               "01/01/2000",[""],{},
                               {"VALDATA": "date","VALVALOR": "cambio_media"}
    ))


#extras
#PIB consumo final das familias % a.t.
listVariables.append(Variables('pib_consumo_familias_trimestral_corrente',"'SCN104_CFPPN104'","ipea",
                               "01/01/2003",["trimonth"],{"trimonth":False},
                               {"VALDATA": "date","VALVALOR": "pib_consumo_familias_trimestral_corrente"}
    ))

#variavel PIB - Mensal em Reais % a.m.
listVariables.append(Variables('pib_mensal_reais',"'BM12_PIB12'","ipea",
                               "01/01/1990",[""],{},
                               {"VALDATA": "date","VALVALOR": "pib_mensal_reais"}
    ))

#Taxa de juros - Selic - fixada % a.d.
listVariables.append(Variables('selic_fixada',"'BM366_TJOVER366'","ipea",
                               "01/07/1996",["dailytomonth"],{},
                               {"VALDATA": "date","VALVALOR": "selic_fixada"}
    ))

#Vendas reais - varejo - tecidos, vestuário e calçados - índice (média 2022 = 100) % a.m.
listVariables.append(Variables('venda_varejo_textil_confeccoes',"'PMC12_VRVESTN12'","ipea",
                               "01/01/2000",[""],{},
                               {"VALDATA": "date","VALVALOR": "venda_varejo_textil_confeccoes"}
    ))

#Vendas reais - varejo - tecidos, vestuário e calçados - índice dessazonalizado (média 2022 = 100) % a.m.
listVariables.append(Variables('venda_varejo_textil_confeccoes_dessazonalizado',"'PMC12_VRVESTNSA12'","ipea",
                               "01/01/2000",[""],{},
                               {"VALDATA": "date","VALVALOR": "venda_varejo_textil_confeccoes"}
    ))

#Importações - confecção de artigos do vestuário e acessórios (FOB) % a.m.
listVariables.append(Variables('importacoes_confeccao',"'FUNCEX12_MVVEST2N12'","ipea",
                               "01/01/2000",["seasonal"],{},
                               {"VALDATA": "date","VALVALOR": "importacoes_confeccao"}
    ))

#Índice nacional de custo da construção do mercado (INCC-M) % a.m.
listVariables.append(Variables('incc_m',"'IGP12_INCCMG12'","ipea",
                               "01/01/2000",["rolling"],{"rolling":"-12-MovelMensal"},
                               {"VALDATA": "date","VALVALOR": "incc_m"}
    ))




#grupo do bcb, as vezes da erro de api call



#Saldo de crédito
#variavel Saldo da carteira de crédito com recursos livres - Pessoas físicas - Total % a.m.
listVariables.append(Variables('saldo_credito_pf_total',"20570","bcb",
                               "01/03/2011",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_credito_pf_total"}
    ))

#variavel Saldo da carteira de crédito com recursos livres - Pessoas físicas - Aquisição de veículos % a.m.
listVariables.append(Variables('saldo_credito_pf_veiculos',"20581","bcb",
                               "01/03/2011",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_credito_pf_veiculos"}
    ))

#variavel Saldo da carteira de crédito com recursos livres - Pessoas físicas - Aquisição de outros bens % a.m.
listVariables.append(Variables('saldo_credito_pf_outros',"20582","bcb",
                               "01/03/2011",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_credito_pf_outros"}
    ))

#variavel Saldo da carteira de crédito com recursos livres - Pessoas físicas - Aquisição de bens total % a.m.
listVariables.append(Variables('saldo_credito_pf_bens_total',"20583","bcb",
                               "01/03/2011",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_credito_pf_bens_total"}
    ))

#Saldo de crédito com Recursos Direcionados
#variavel Saldo - Pessoas jurídicas - Financiamento imobiliário- Taxas de Mercado % a.m.
listVariables.append(Variables('saldo_imobiliário_pj_mercado',"20598","bcb",
                               "01/03/2007",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_imobiliário_pj_mercado"}
    ))

#variavel Saldo - Pessoas jurídicas - Financiamento imobiliário - Taxas Reguladas % a.m.
listVariables.append(Variables('saldo_imobiliário_pj_reguladas',"20599","bcb",
                               "01/03/2007",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_imobiliário_pj_reguladas"}
    ))

#variavel Saldo - Pessoas jurídicas - Financiamento imobiliário- Total % a.m.
listVariables.append(Variables('saldo_imobiliário_pj_total',"20600","bcb",
                               "01/03/2007",["defl","defl_seasonal"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_imobiliário_pj_total"}
    ))

#variavel Saldo - Pessoas Física - Financiamento imobiliário- Taxas de Mercado % a.m.
listVariables.append(Variables('saldo_imobiliário_pf_mercado',"20610","bcb",
                               "01/03/2007",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_imobiliário_pf_mercado"}
    ))

#variavel Saldo - Pessoas Física - Financiamento imobiliário - Taxas Reguladas % a.m.
listVariables.append(Variables('saldo_imobiliário_pf_reguladas',"20611","bcb",
                               "01/03/2007",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_imobiliário_pf_reguladas"}
    ))

#variavel Saldo - Pessoas Física - Financiamento imobiliário- Total % a.m.
listVariables.append(Variables('saldo_imobiliário_pf_total',"20612","bcb",
                               "01/03/2007",["defl","defl_seasonal"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_imobiliário_pf_total"}
    ))

#Saldo de crédito por atividade economica
#variavel Saldo ao setor industrial - Total % a.m
listVariables.append(Variables('saldo_industrial_total',"22043","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_total"}
    ))

#variavel Saldo ao setor industrial - Serviços industriais de utilidade pública % a.m
listVariables.append(Variables('saldo_industrial_siup',"22034","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_siup"}
    ))

#variavel Saldo ao setor industrial - Construção % a.m
listVariables.append(Variables('saldo_industrial_construção',"22030","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_construção"}
    ))

#variavel Saldo ao setor industrial - Alimentos % a.m
listVariables.append(Variables('saldo_industrial_alimentos',"27743","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_alimentos"}
    ))

#variavel Saldo ao setor industrial - Açúcar % a.m
listVariables.append(Variables('saldo_industrial_açúcar',"27744","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_açúcar"}
    ))

#variavel Saldo ao setor industrial - Têxtil, vestuário, couro e calçados % a.m
listVariables.append(Variables('saldo_industrial_textil_vestuário_couro',"27745","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_textil_vestuário_couro"}
    ))

#variavel Saldo ao setor industrial - Papel e celulose % a.m
listVariables.append(Variables('saldo_industrial_papel_celulose',"27746","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_papel_celulose"}
    ))

#variavel Saldo ao setor industrial - Petróleo, gás e álcool % a.m
listVariables.append(Variables('saldo_industrial_petroleo',"27747","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_petroleo"}
    ))

#variavel Saldo ao setor industrial - Total % a.m
listVariables.append(Variables('saldo_industrial_metalurgia_siderurgia',"27748","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_metalurgia_siderurgia"}
    ))

#variavel Saldo ao setor industrial - Química e farmacêutica % a.m
listVariables.append(Variables('saldo_industrial_química',"27722","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_química"}
    ))

#variavel Saldo ao setor industrial - Bens de capital % a.m
listVariables.append(Variables('saldo_industrial_bens',"27723","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_bens"}
    ))

#variavel Saldo ao setor industrial - Automobilística % a.m
listVariables.append(Variables('saldo_industrial_automobilística',"27724","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_automobilística"}
    ))

#variavel Saldo ao setor industrial - Mineração % a.m
listVariables.append(Variables('saldo_industrial_mineração',"27749","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_mineração"}
    ))

#variavel Saldo ao setor industrial - Obras de infraestrutura % a.m
listVariables.append(Variables('saldo_industrial_obras',"27725","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_obras"}
    ))

#variavel Saldo ao setor industrial - Outros bens de consumo duráveis % a.m
listVariables.append(Variables('saldo_industrial_outros_bens',"27726","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_outros_bens"}
    ))

#variavel Saldo ao setor industrial - Embalagens % a.m
listVariables.append(Variables('saldo_industrial_embalagens',"27727","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_embalagens"}
    ))

#variavel Saldo ao setor industrial - Bens de consumo não duráveis % a.m
listVariables.append(Variables('saldo_industrial_bens_não_duráveis',"27728","bcb",
                               "01/01/2012",["defl"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"data": "date","valor": "saldo_industrial_bens_não_duráveis"}
    ))



#ICC
#variavel Indicador de Custo do Crédito - ICC - Recursos/Crédito livre - Pessoas jurídicas % a.m.
listVariables.append(Variables('icc_rescursos_livres_pj',"25355","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "icc_rescursos_livres_pj"}
    ))

#variavel Indicador de Custo do Crédito - ICC - Recursos/Crédito livre - Pessoas jurídicas - Aquisição de veículos % a.m.
listVariables.append(Variables('icc_rescursos_livres_pj_veiculos',"27658","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "icc_rescursos_livres_pj_veiculos"}
    ))

#variavel Indicador de Custo do Crédito - ICC - Recursos/Crédito livre - Pessoas jurídicas - Aquisição de outros bens % a.m.
listVariables.append(Variables('icc_rescursos_livres_pj_outros',"27659","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "icc_rescursos_livres_pj_outros"}
    ))

#variavel Indicador de Custo do Crédito - ICC - Recursos/Crédito livre - Pessoas fisica % a.m.
listVariables.append(Variables('icc_rescursos_livres_pf',"25356","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "icc_rescursos_livres_pf"}
    ))

#variavel Indicador de Custo do Crédito - ICC - Recursos/Crédito livre - Pessoas fisica - Aquisição de veículos % a.m.
listVariables.append(Variables('icc_rescursos_livres_pf_veiculos',"27680","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "icc_rescursos_livres_pf_veiculos"}
    ))

#variavel Indicador de Custo do Crédito - ICC - Recursos/Crédito livre - Pessoas fisica - Aquisição de outros bens % a.m.
listVariables.append(Variables('icc_rescursos_livres_pf_outros',"27681","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "icc_rescursos_livres_pf_outros"}
    ))

#Concessões
#Concessões de crédito com recursos livres - Pessoas físicas - Total % a.m.
listVariables.append(Variables('concessoes_credito_recursos_livres_pf',"20675","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "concessoes_recursos_livres_pf"}
    ))

#Concessões de crédito com recursos livres - Pessoas físicas - Aquisição de veículos % a.m.
listVariables.append(Variables('concessoes_credito_recursos_livres_pf_veiculos',"20673","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "concessoes_recursos_livres_pf_veiculos"}
    ))

#Concessões de crédito com recursos livres - Pessoas físicas - Aquisição de outros bens % a.m.
listVariables.append(Variables('concessoes_credito_recursos_livres_pf_outros',"20674","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "concessoes_recursos_livres_pf_outros"}
    ))

#Concessões de crédito com recursos livres - Pessoas jurídicas - Total % a.m.
listVariables.append(Variables('concessoes_credito_recursos_livres_pj',"20647","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "concessoes_recursos_livres_pj"}
    ))

#Concessões de crédito com recursos livres - Pessoas jurídicas - Aquisição de veículos % a.m.
listVariables.append(Variables('concessoes_credito_recursos_livres_pj_veiculos',"20645","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "concessoes_recursos_livres_pj_veiculos"}
    ))

#Concessões de crédito com recursos livres - Pessoas jurídicas - Aquisição de outros bens % a.m.
listVariables.append(Variables('concessoes_credito_recursos_livres_pj_outros',"20646","bcb",
                               "01/01/2013",["seasonal"],{},
                               {"data": "date","valor": "concessoes_recursos_livres_pj_outros"}
    ))

#extras
#variavel IPCA Industrias, subcategoria de serviços % a.m.
listVariables.append(Variables('ipca_industrial',"27863","bcb",
                               "01/01/2000",["rolling"],{"rolling":"-12-MovelMensal"},
                               {"data": "date","valor": "ipca_industrial"}
    ))

#variavel Endividamento das familias em relação a renda acumulada dos 12 meses % a.m.
listVariables.append(Variables('endividamento_familias_total',"29037","bcb",
                               "01/01/2005",[""],{""},
                               {"data": "date","valor": "endividamento_familias_total"}
    ))

#variavel Endividamento das familias em relação a renda acumulada dos 12 meses exceto credito habitacional % a.m.
listVariables.append(Variables('endividamento_familias_exceto_hab',"29038","bcb",
                               "01/01/2005",[""],{""},
                               {"data": "date","valor": "endividamento_familias_exceto_hab"}
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

listVariables.append(Variables('selic_diaria',"11","#bcb",
                               "01/01/2000",[""],{},
                               {"data": "date","valor": "selic_diaria"}
    ))

#variavel Inadimplência da carteira de crédito - Pessoas físicas - Total % a.m.
listVariables.append(Variables('inadimplencia_pf_total',"21084","bcb",
                               "01/03/2011",["seasonal"],{},
                               {"data": "date","valor": "inadimplencia_pf_total"}
    ))



#grupo do bcb - focus, dados em painel, process mais complicado e demorado



#variavel expectativa IPCA
listVariables.append(Variables('expectativa_ipca_2024',"ipca_focus","bcb_focus",
                               {"subrecurso": "ExpectativaMercadoMensais",
                                "filter": "endswith(Indicador%2C'IPCA')%20and%20baseCalculo%20eq%200%20and%20Data%20gt%20'2022-12-31'",
                                "select": "Data,DataReferencia,Mediana"},
                               ["transpose_rolling_transpose","latest_transpose","latest_transpose_rolling","firstdayofmonth_transpose_rolling"],
                               {"rolling":"ipca_mensal_taxa_variação-12-MovelMensal"},
                               {""}    
    ))

#variavel expectativa IPCA serviços
listVariables.append(Variables('expectativa_ipca_servicos_2024',"ipca_servicos_focus","bcb_focus",
                               {"subrecurso": "ExpectativaMercadoMensais",
                                "filter": "endswith(Indicador%2C'IPCA%20Servi%C3%A7os')%20and%20baseCalculo%20eq%200%20and%20Data%20gt%20'2022-12-31'",
                                "select": "Data,DataReferencia,Mediana"},
                               ["transpose_rolling_transpose","latest_transpose","latest_transpose_rolling","firstdayofmonth_transpose_rolling"],
                               {"rolling":"ipca_mensal_taxa_preços_livres_serviços-12-MovelMensal"},
                               {""}    
    ))

#variavel expectativa taxa de desocupação
listVariables.append(Variables('expectativa_desocupacao_2024',"taxa_desocupacao_focus","bcb_focus",
                               {"subrecurso": "ExpectativaMercadoMensais",
                                "filter": "endswith(Indicador%2C'desocupa%C3%A7%C3%A3o')%20and%20baseCalculo%20eq%200%20and%20Data%20gt%20'2022-12-31'",
                                "select": "Data,DataReferencia,Mediana"},
                               ["latest_transpose"],
                               {""},
                               {""}    
    ))

#variavel expectativa Câmbio
listVariables.append(Variables('expectativa_cambio_2024',"cambio_focus","bcb_focus",
                               {"subrecurso": "ExpectativaMercadoMensais",
                                "filter": "endswith(Indicador%2C'C%C3%A2mbio')%20and%20baseCalculo%20eq%200%20and%20Data%20gt%20'2022-12-31'",
                                "select": "Data,DataReferencia,Mediana"},
                               ["latest_transpose"],
                               {""},
                               {""}    
    ))

#variavel expectativa Selic
listVariables.append(Variables('expectativa_selic',"selic_focus","bcb_focus",
                               {"subrecurso": "ExpectativasMercadoSelic",
                                "filter": "Data%20gt%20'2022-12-31'",
                                "select": "Data,Reuniao,Mediana"},
                               ["transpose_copomtomonth_transpose","latest_transpose_copomtomonth"],
                               {"copomtomonth":"selic_fixada"},
                               {""} 
))

#variavel expectativa PIB total Trimestral
listVariables.append(Variables('expectativa_pib_tri',"pib_total_focus","bcb_focus",
                               {"subrecurso": "ExpectativasMercadoTrimestrais",
                                "filter": "endswith(Indicador%2C'PIB%20Total')%20and%20baseCalculo%20eq%200%20and%20Data%20gt%20'2024-12-31'",
                                "select": "Data,DataReferencia,Mediana"},
                               ["latest_transpose","latest_transpose_trimonth"],
                               {"trimonth":True},
                               {""} 
))



#grupo do sidra, grande volume de dados, pode ser lento



#PIM PF
#variavel Produção Física Industrial de SC, por seções e atividades industriais mensal % a.m.
listVariables.append(Variables('pim_pf_mensal_sc',"8888-12606-sc","sidra",
                               {"periodos":"-500","variaveis":"12606","localidade":"N3[42]","classificacao":"544[all]"},
                               ["seasonal","seasonal_getallbases","variation","getallbases"],{"variation":"12"},
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

#variavel Produção Física Industrial BR, por indicadores especiais mensal % a.m.
listVariables.append(Variables('pim_pf_mensal_br_especiais',"8889-12606","sidra",
                               {"periodos":"-500","variaveis":"12606","localidade":"N1[all]","classificacao":"25[all]"},
                               ["seasonal","#seasonal_getallbases","variation","getallbases"],{"variation":"12"},
                               {"date":"date",
                                "1.1 Bens de Capital para fins industriais": "1.1_CapInd_sc",
                                "1.1.1 Bens de Capital para fins industriais seriados": "1.1.1_CapInd_Ser_sc",
                                "1.1.2 Bens de Capital para fins industriais não seriados": "1.1.2_CapInd_NSer_sc",
                                "1.2 Bens de Capital agrícolas": "1.2_CapAgro_sc",
                                "1.3 Bens de Capital peças agrícolas": "1.3_CapPeçasAgro_sc",
                                "1.4 Bens de Capital para construção": "1.4_CapConstr_sc",
                                "1.5 Bens de Capital para o setor de energia elétrica": "1.5_CapEnergia_sc",
                                "1.6 Bens de Capital para equipamentos de transporte": "1.6_CapTransp_sc",
                                "1.7 Bens de Capital de uso misto": "1.7_CapMisto_sc",
                                "2 Insumos Típicos da Construção Civil": "2_InsumosConstr_sc",
                                "3 Total de Embalagens": "3_EmbTotal_sc",
                                "3.1 Embalagens de vidro": "3.1_EmbVidro_sc",
                                "3.2 Embalagens de metal": "3.2_EmbMetal_sc",
                                "3.3 Embalagens de madeira": "3.3_EmbMadeira_sc",
                                "3.4 Embalagens de papel e papelão": "3.4_EmbPapel_sc",
                                "3.5 Embalagens de material plástico": "3.5_EmbPlast_sc",
                                "4 Eletrodomésticos": "4_Eletro_sc",
                                "5.1.1 Bens de capital por atividade - Equipamentos de informática, produtos eletrônicos e ópticos": "5.1.1_CapInfoEletr_sc",
                                "5.1.2 Bens de capital por atividade - Máquinas, aparelhos e materiais elétricos": "5.1.2_CapEletr_sc",
                                "5.1.3 Bens de capital por atividade - Máquinas e equipamentos": "5.1.3_CapMaqEquip_sc",
                                "5.1.4 Bens de capital por atividade - Veículos automotores, reboques e carrocerias": "5.1.4_CapVeic_sc",
                                "5.1.5 Bens de capital por atividade - Outros equipamentos de transporte": "5.1.5_CapOutTransp_sc",
                                "5.1.6 Bens de capital por atividade - Demais atividades*": "5.1.6_CapOutros_sc",
                                "5.2.1 Bens intermediários por atividade - Indústrias extrativas": "5.2.1_IntExtr_sc",
                                "5.2.2 Bens intermediários por atividade - Produtos alimentícios": "5.2.2_IntAlim_sc",
                                "5.2.3 Bens intermediários por atividade - Produtos têxteis": "5.2.3_IntTex_sc",
                                "5.2.4 Bens intermediários por atividade - Celulose, papel e produtos de papel": "5.2.4_IntCelPapel_sc",
                                "5.2.5 Bens intermediários por atividade - Coque, produtos derivados do petróleo e biocombustíveis": "5.2.5_IntComb_sc",
                                "5.2.6 Bens intermediários por atividade - Produtos químicos": "5.2.6_IntQuim_sc",
                                "5.2.7 Bens intermediários por atividade - Produtos de borracha e de material plástico": "5.2.7_IntBorracha_sc",
                                "5.2.8 Bens intermediários por atividade - Produtos de minerais não metálicos": "5.2.8_IntMiner_sc",
                                "5.2.9 Bens intermediários por atividade - Metalurgia": "5.2.9_IntMet_sc",
                                "5.2.10 Bens intermediários por atividade - Produtos de metal - exceto máquinas e equipamentos": "5.2.10_IntProdMet_sc",
                                "5.2.11 Bens intermediários por atividade - Máquinas e equipamentos": "5.2.11_IntMaqEquip_sc",
                                "5.2.12 Bens intermediários por atividade - Veículos automotores, reboques e carrocerias": "5.2.12_IntVeic_sc",
                                "5.2.13 Bens intermediários por atividade - Demais atividades*": "5.2.13_IntOutros_sc",
                                "5.3.1 Bens de consumo duráveis por atividade - Equipamentos de informática, produtos eletrônicos e ópticos": "5.3.1_DurInfoEletr_sc",
                                "5.3.2 Bens de consumo duráveis por atividade - Máquinas, aparelhos e materiais elétricos": "5.3.2_DurEletr_sc",
                                "5.3.3 Bens de consumo duráveis por atividade - Veículos automotores, reboques e carrocerias": "5.3.3_DurVeic_sc",
                                "5.3.4 Bens de consumo duráveis por atividade - Outros equipamentos de transporte": "5.3.4_DurOutTransp_sc",
                                "5.3.5 Bens de consumo duráveis por atividade - Móveis": "5.3.5_DurMoveis_sc",
                                "5.3.6 Bens de consumo duráveis por atividade - Demais atividades*": "5.3.6_DurOutros_sc",
                                "5.4.1 Bens de consumo semi e não duráveis por atividade - Produtos alimentícios": "5.4.1_SemiAlim_sc",
                                "5.4.2 Bens de consumo semi e não duráveis por atividade - Bebidas": "5.4.2_SemiBeb_sc",
                                "5.4.3 Bens de consumo semi e não duráveis por atividade - Produtos têxteis": "5.4.3_SemiTex_sc",
                                "5.4.4 Bens de consumo semi e não duráveis por atividade - Confecção de artigos do vestuário e acessórios": "5.4.4_SemiVest_sc",
                                "5.4.5 Bens de consumo semi e não duráveis por atividade - Preparação de couros e fabricação de artefatos de couro, artigos para viagem e calçados": "5.4.5_SemiCouro_sc",
                                "5.4.6 Bens de consumo semi e não duráveis por atividade - Impressão e reprodução de gravações": "5.4.6_SemiImp_sc",
                                "5.4.7 Bens de consumo semi e não duráveis por atividade - Coque, produtos derivados do petróleo e biocombustíveis": "5.4.7_SemiComb_sc",
                                "5.4.8 Bens de consumo semi e não duráveis por atividade - Produtos químicos": "5.4.8_SemiQuim_sc",
                                "5.4.9 Bens de consumo semi e não duráveis por atividade - Produtos Farmoquímicos e farmacêuticos": "5.4.9_SemiFarm_sc",
                                "5.4.10 Bens de consumo semi e não duráveis por atividade - Demais atividades*": "5.4.10_SemiOutros_sc",
                                "6.1 Alta Intensidade do Gasto com Energia Elétrica - Total": "6.1_AltaEnergia_sc",
                                "6.1.1 Bens intermediários - Alta intensidade": "6.1.1_Interm_Alta_sc",
                                "6.1.2 Bens de consumo - Alta intensidade": "6.1.2_Consumo_Alta_sc",
                                "6.1.2.1 Bens de consumo semi e não duráveis - Alta intensidade": "6.1.2.1_SemiDur_Alta_sc",
                                "6.2 Média Intensidade do Gasto com Energia Elétrica - Total": "6.2_MediaEnergia_sc",
                                "6.2.1 Bens de capital - Média intensidade": "6.2.1_Capital_Media_sc",
                                "6.2.2 Bens intermediários - Média intensidade": "6.2.2_Interm_Media_sc",
                                "6.2.3 Bens de consumo - Média intensidade": "6.2.3_Consumo_Media_sc",
                                "6.2.3.1 Bens de consumo duráveis - Média intensidade": "6.2.3.1_Duravel_Media_sc",
                                "6.2.3.2 Bens de consumo semi e não duráveis - Média intensidade": "6.2.3.2_SemiDur_Media_sc",
                                "6.3 Baixa Intensidade do Gasto com Energia Elétrica - Total": "6.3_BaixaEnergia_sc",
                                "6.3.1 Bens de capital - Baixa intensidade": "6.3.1_Capital_Baixa_sc",
                                "6.3.2 Bens intermediários - Baixa intensidade": "6.3.2_Interm_Baixa_sc",
                                "6.3.3 Bens de consumo - Baixa intensidade": "6.3.3_Consumo_Baixa_sc",
                                "6.3.3.1 Bens de consumo duráveis - Baixa intensidade": "6.3.3.1_Duravel_Baixa_sc",
                                "6.3.3.2 Bens de consumo semi e não duráveis - Baixa intensidade": "6.3.3.2_SemiDur_Baixa_sc",
                                "6.3.4 Sem categoria econômica - Baixa intensidade": "6.3.4_SemCat_Baixa_sc"
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
                               {"periodos":"-500","variaveis":"4099","localidade":"N1[all]","classificacao":""},["trimonth"],{"trimonth":True},
                               {"date":"date",
                                "Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade":"taxa_desocupacao_mensal_trimestre_movel"
                                }
    ))

#variavel Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade (%) Total de SC, Trimestre Móvel % a.m.
listVariables.append(Variables('taxa_desocupacao_mensal_trimestre_movel_sc',"6468-4099-sc","sidra",
                               {"periodos":"-500","variaveis":"4099","localidade":"N3[42]","classificacao":""},["trimonth"],{"trimonth":True},
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

#variavel Rendimento médio mensal real, habitualmente recebido em todos os trabalhos % a.m.
listVariables.append(Variables('rendimento_medio_mensal_hab',"6390-5933-br","sidra",
                               {"periodos":"-500", "variaveis":"5933","localidade":"N1[all]","classificacao":""},["seasonal"],{},
                               {"date":"date",
                                "Rendimento médio mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_medio_mensal_hab"
                                }
    ))

#variavel Rendimento médio trimestral real, efetivamente recebido em todos os trabalhos - SC % a.t.
listVariables.append(Variables('rendimento_medio_tri_sc',"6469-5935-br","sidra",
                               {"periodos":"-500", "variaveis":"5935","localidade":"N3[42]","classificacao":""},["trimonth","trimonth_seasonal"],{"trimonth":True},
                               {"date":"date",
                                "Rendimento médio mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, efetivamente recebido em todos os trabalhos":"rendimento_medio_trimestral_sc"
                                }
    ))

#variavel Rendimento médio trimestral real, habitualmente recebido em todos os trabalhos - SC % a.t.
listVariables.append(Variables('rendimento_medio_tri_sc_hab',"6472-5933-br","sidra",
                               {"periodos":"-500", "variaveis":"5933","localidade":"N3[42]","classificacao":""},["trimonth_seasonal"],{"trimonth":True},
                               {"date":"date",
                                "Rendimento médio mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_medio_tri_sc_hab"
                                }
    ))

#variavel Massa de Rendimento mensal real, efetivamente recebido em todos os trabalhos - BR % a.m.
listVariables.append(Variables('rendimento_massa_mensal_real',"6393-6295-br","sidra",
                               {"periodos":"-500", "variaveis":"6295","localidade":"N1[all]","classificacao":""},["seasonal","defl_seasonal"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, efetivamente recebido em todos os trabalhos":"rendimento_massa_mensal_real"
                                }
    ))

#variavel Massa de Rendimento mensal real, habitualmente recebido em todos os trabalhos - BR % a.m.
listVariables.append(Variables('rendimento_massa_mensal_real_hab',"6392-6293-br","sidra",
                               {"periodos":"-500", "variaveis":"6293","localidade":"N1[all]","classificacao":""},["seasonal"],{},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_massa_mensal_real_hab"
                                }
    ))

#variavel Massa de Rendimento trimestral real, efetivamente recebido em todos os trabalhos - BR % a.m.
listVariables.append(Variables('rendimento_massa_trimestral_real',"5606-6295-br","sidra",
                               {"periodos":"-500","variaveis":"6295","localidade":"N1[all]","classificacao":""},["trimonth_seasonal"],{"trimonth":True},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, efetivamente recebido em todos os trabalhos":"rendimento_massa_trimestral_real"
                                }
    ))

#variavel Massa de Rendimento trimestral real, habitualmente recebido em todos os trabalhos - BR % a.m.
listVariables.append(Variables('rendimento_massa_tri_real_hab',"5606-6293-br","sidra",
                               {"periodos":"-500","variaveis":"6293","localidade":"N1[all]","classificacao":""},["trimonth_seasonal"],{"trimonth":True},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_massa_tri_real_hab"
                                }
    ))

#variavel Massa de Rendimento trimestral real, efetivamente recebido em todos os trabalhos - SC % a.m.
listVariables.append(Variables('rendimento_massa_tri_real_sc',"5606-6295-sc","sidra",
                               {"periodos":"-500","variaveis":"6295","localidade":"N3[42]","classificacao":""},["trimonth","trimonth_seasonal","trimonth_defl_seasonal"],{"trimonth":True,"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, efetivamente recebido em todos os trabalhos":"rendimento_massa_trimestral_real_sc"
                                }
    ))

#variavel Massa de Rendimento trimestral real, habitualmente recebido em todos os trabalhos - SC % a.m.
listVariables.append(Variables('rendimento_massa_tri_real_sc_hab',"5606-6293-sc","sidra",
                               {"periodos":"-500","variaveis":"6293","localidade":"N3[42]","classificacao":""},["trimonth_seasonal"],{"trimonth":True},
                               {"date":"date",
                                "Massa de rendimento mensal real das pessoas de 14 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos":"rendimento_massa_tri_real_sc_hab"
                                }
    ))

#variavel Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade (%) Total, Trimestre Móvel % a.m.
listVariables.append(Variables('rendimento_medio_tri_educacao_br',"5438-5932-br","sidra",
                               {"periodos":"-500","variaveis":"5932","localidade":"N1[all]","classificacao":"1568[120704,120706,11779,11628,11629,11630,11631,11632]"},
                               ["trimonth"],{"trimonth":True},
                               {"date":"date",
                                "Total":"Total",
                                "Sem instrução e menos de 1 ano de estudo":"sem estudo",
                                "Ensino fundamental incompleto ou equivalente":"fundamental incompleto",
                                "Ensino fundamental completo ou equivalente":"fundamental completo",
                                "Ensino médio incompleto ou equivalente":"medio incompleto",
                                "Ensino médio completo ou equivalente":"medio completo",
                                "Ensino superior incompleto ou equivalente":"superior incompleto",
                                "Ensino superior completo ou equivalente":"superior completo",
                                "Não determinado":"não determinado"
                                }
    ))

#variavel Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade (%) Total, Trimestre Móvel % a.m.
listVariables.append(Variables('rendimento_medio_tri_educacao_sc',"5438-5932-sc","sidra",
                               {"periodos":"-500","variaveis":"5932","localidade":"N3[42]","classificacao":"1568[120704,120706,11779,11628,11629,11630,11631,11632]"},
                               ["trimonth"],{"trimonth":True},
                               {"date":"date",
                                "Total":"Total",
                                "Sem instrução e menos de 1 ano de estudo":"sem estudo",
                                "Ensino fundamental incompleto ou equivalente":"fundamental incompleto",
                                "Ensino fundamental completo ou equivalente":"fundamental completo",
                                "Ensino médio incompleto ou equivalente":"medio incompleto",
                                "Ensino médio completo ou equivalente":"medio completo",
                                "Ensino superior incompleto ou equivalente":"superior incompleto",
                                "Ensino superior completo ou equivalente":"superior completo"
                                }
    ))


#extras
#despesa de consumo das familias
#variavel PIB despesa de consumo das familias Valores encadeados a preços de 1995 % a.t.
listVariables.append(Variables('pib_consumo_familias_trimestral',"6612-9318-br","sidra",
                               {"periodos":"-500", "variaveis":"9318","localidade":"N1[all]","classificacao":"11255[93404]"},["trimonth"],{"trimonth":True},
                               {"date":"date",
                                "Despesa de consumo das famílias": "pib_consumo_familias_trimestral_base_fixa",
                                }
    ))

#variavel PIB despesa de consumo das familias Valores encadeados a preços de 1995 % a.t.
listVariables.append(Variables('pib_consumo_familias_trimestral_dessazonalizado',"6613-9319-br","sidra",
                               {"periodos":"-500", "variaveis":"9319","localidade":"N1[all]","classificacao":"11255[93404]"},["trimonth"],{"trimonth":True},
                               {"date":"date",
                                "Despesa de consumo das famílias": "pib_consumo_familias_trimestral_base_fixa_dessazonalizado",
                                }
    ))

#variavel PIB construção civil preços correntes (milhoes R$) % a.t.
listVariables.append(Variables('pib_construcao_trimestral_corrente',"1846-585","sidra",
                               {"periodos":"-500", "variaveis":"585","localidade":"N1[all]","classificacao":"11255[90694]"},["trimonth"],{"trimonth":True},
                               {"date":"date",
                                "Construção": "pib_construcao_milhoes",
                                }
    ))

#variavel PIB construção civil preços correntes (milhoes R$) % a.t.
listVariables.append(Variables('pib_construcao_trimestral_volume',"1620-583","sidra",
                               {"periodos":"-500", "variaveis":"583","localidade":"N1[all]","classificacao":"11255[90694]"},["trimonth"],{"trimonth":True},
                               {"date":"date",
                                "Construção": "pib_construcao_volume",
                                }
    ))

#variavel PIB construção civil preços correntes (milhoes R$) % a.t.
listVariables.append(Variables('construcao_medio_m_2_sc',"2296-48","sidra",
                               {"periodos":"-500", "variaveis":"48","localidade":"N3[42]","classificacao":""},
                               ["defl","defl_seasonal"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"date":"date",
                                "Custo médio m² - moeda corrente": "construcao_m_2_sc",
                                }
    ))



#grupo externo, dados que não tem por API então tenho que pegar por excel



#variavel IPCA - geral - taxa de variação  mensal % a.m.
listVariables.append(Variables('trccrb_daily',"TRCCRB","externas",
                               "01/01/1980",["dailytomonth"],{},
                               {"date": "date","valor": "trccrb_daily"}
    ))

#Meta de Inflação do Brasil % a.m.
listVariables.append(Variables('meta_inflacao',"meta_inflacao","externas",
                               "01/01/1980",[],{},
                               {"date": "date","valor": "meta_inflacao"}
    ))

#Valor Liquidado pelo Governo do Estado na área de transporte (rodovias, ferrovias, portos e outros) e urbanismo. % a.m.
listVariables.append(Variables('invest_liq_sc_transporte',"invest_liq_sc_transporte","externas",
                               "01/01/2011",["defl","defl_seasonal"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"date": "date","valor": "invest_liq_sc_transporte"}
    ))


#Valor Liquidado pelo Governo do Estado na área de transporte (rodovias, ferrovias, portos e outros) e urbanismo. % a.m.
listVariables.append(Variables('invest_infra_sc',"invest_infra_sc","externas",
                               "01/01/2011",["defl","defl_seasonal"],{"defl":"ipca_mensal_taxa_variação,2018/12/01"},
                               {"date": "date","valor": "invest_infra_sc"}
    ))



#models estabelecidos


#model ipca para o power BI
listModels.append(Models('ipca_evolucao',"2002-01-01", "",
                         ["selic_mensal",
                          "ipca_mensal_taxa_variação",
                          "ipca_mensal_taxa_preços_livres_serviços",
                          "ipca_mensal_taxa_variação_rolling",
                          "ipca_mensal_taxa_preços_livres_serviços_rolling",
                          "ipca_mensal_taxa_núcleo_médias_aparadas_suavização_rolling",
                          "ipca_mensal_taxa_núcleo_exclusão_rolling",
                          "meta_inflacao",
                          "expectativa_ipca_2024_latest_transpose_rolling",
                          "expectativa_ipca_servicos_2024_latest_transpose_rolling",
                          "expectativa_selic_latest_transpose_copomtomonth",
                          "expectativa_ipca_2024_firstdayofmonth_transpose_rolling",
                          "expectativa_ipca_servicos_2024_firstdayofmonth_transpose_rolling"
                          ],
                         ["date"]
    
    ))

#model produção setorial para power BI
listModels.append(Models('producao_setorial',"2003-01-01", "",
                         ["ibc_br_mensal_dessazonalizado_getallbases",
                          "ibcr_sc_mensal_dessazonalizado_getallbases",
                          "pim_pf_mensal_br_dessazonalizado_getallbases",
                          "pim_pf_mensal_sc_dessazonalizado_getallbases",
                          "pim_pf_mensal_sc_seasonal_getallbases"
                          ],
                         ["dateBase","date"]
    
    ))

#model serviços setorial para power BI
listModels.append(Models('servicos_setorial',"2011-01-01", "",
                         ["ibc_br_mensal_dessazonalizado_getallbases",
                          "pms_volume_mensal_br_dessazonalizado_getallbases"
                          ],
                         ["dateBase","date"]
    
    ))

#model rendimentos para power BI
listModels.append(Models('rendimentos',"2012-01-01", "",
                         ["ibc_br_mensal_dessazonalizado",
                          "ibcr_sc_mensal_dessazonalizado",
                          "rendimento_massa_mensal_real",
                          "rendimento_medio_mensal",
                          "rendimento_massa_tri_real_sc_trimonth",
                          "rendimento_medio_tri_sc_trimonth",
                          "taxa_desocupacao_mensal_trimestre_movel",
                          "taxa_desocupacao_mensal_trimestre_movel_sc_trimonth"
                          ],
                         ["date"]
    
    ))

#model Saldo de crédito PF para power BI
listModels.append(Models('saldo_credito_pf',"2008-01-01", "",
                         ["selic_mensal",
                          "saldo_credito_pf_outros_defl",
                          "saldo_credito_pf_veiculos_defl",
                          "saldo_credito_pf_total_defl"
                          ],
                         ["date"]
    
    ))

#model evolução grandes setores para power BI
listModels.append(Models('grandes_setores',"2011-01-01", "",
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
listModels.append(Models('bens',"2002-01-01", "",
                         ["pim_pf_bens_categorias_dessazonalizado_getallbases"
                          ],
                         ["dateBase","date"]
    
    ))

#model crédito+concessoes+icc para power BI
listModels.append(Models('credito_consessoes_icc',"2008-01-01", "",
                         ["selic_mensal",
                          "saldo_credito_pf_outros_defl",
                          "saldo_credito_pf_veiculos_defl",
                          "saldo_credito_pf_total_defl",
                          "icc_rescursos_livres_pj",
                          "icc_rescursos_livres_pj_veiculos",
                          "icc_rescursos_livres_pj_outros",
                          "icc_rescursos_livres_pf",
                          "icc_rescursos_livres_pf_veiculos",
                          "icc_rescursos_livres_pf_outros",
                          "concessoes_credito_recursos_livres_pf",
                          "concessoes_credito_recursos_livres_pf_veiculos",
                          "concessoes_credito_recursos_livres_pf_outros",
                          "concessoes_credito_recursos_livres_pj",
                          "concessoes_credito_recursos_livres_pj_veiculos",
                          "concessoes_credito_recursos_livres_pj_outros"
                          ],
                         ["date"]
    
    ))

#model Endividamento das familias
listModels.append(Models('endividamento',"2002-01-01", "",
                         ["selic_mensal",
                          "endividamento_familias_total",
                          "endividamento_familias_exceto_hab",
                          "rendimento_massa_mensal_real"
                          ],
                         ["date"]
    
    ))

#model evolução setores industria para power BI
listModels.append(Models('ipp_setores',"2010-01-01", "",
                         ["ipp_transformacao_basefixa",
                          "ipp_alimentos_basefixa",
                          "ipp_borracha_plastico_basefixa",
                          "ipp_madeira_basefixa",
                          "ipp_maquinas_equipamentos_basefixa",
                          "ipp_metalurgia_basefixa",
                          "ipp_minerais_não_metalicos_basefixa",
                          "ipp_outros_quimicos_basefixa",
                          "ipp_papel_celulose_basefixa",
                          "ipp_petroleo_basefixa",
                          "ipp_metal_basefixa",
                          "ipp_veiculos_basefixa"
                          ],
                         ["date"]
    ))



#Modelos para analise de previsão dos setores de SC

#model evolução Industria Tranformação
listModels.append(Models('modelo_transformacao',"2002-01-01", "",
                          ["pim_pf_mensal_sc_dessazonalizado",
                           "pim_pf_mensal_br_dessazonalizado[1_Geral_br]",
                           "ibc_br_mensal_dessazonalizado",
                           "ibcr_sc_mensal_dessazonalizado",
                           "expectativa_pib_tri_latest_transpose_trimonth",
                           "selic_mensal",                           
                           "expectativa_selic_latest_transpose_copomtomonth",
                           "ipca_mensal_taxa_variação_rolling",
                           "expectativa_ipca_2024_latest_transpose_rolling",
                           "ipp_transformacao_basefixa_rolling",
                           "cambio_media",
                           "expectativa_cambio_2024_latest_transpose",
                           "trccrb_daily_dailytomonth"
                          ],
                         ["date"]
    ))

#model evolução alimentação
listModels.append(Models('modelo_alimentacao',"2002-01-01", "",
                          ["pim_pf_mensal_sc_seasonal[3.10_Alimentícios_sc_seas]",
                           #adicionar preço de frango e porco nacional e internacional
                           "ipca_mensal_alimentos_bebidas_rolling",
                           "ipca_mensal_taxa_variação_rolling",
                           "rendimento_massa_mensal_real_defl_seasonal",
                           "rendimento_massa_tri_real_sc_trimonth_defl_seasonal"
                          ],
                         ["date"]
    ))

#model evolução textil
listModels.append(Models('modelo_textil',"2002-01-01", "",
                          ["pim_pf_mensal_sc_seasonal[3.13_Têxteis_sc_seas]",
                          "pim_pf_mensal_sc_seasonal[3.14_confecções_sc_seas]",
                          "rendimento_massa_mensal_real_defl_seasonal",
                          "rendimento_massa_tri_real_sc_trimonth_defl_seasonal",
                          "saldo_credito_pf_outros_defl",
                          "concessoes_credito_recursos_livres_pf_outros_seasonal",
                          "saldo_industrial_textil_vestuário_couro_defl",
                          "importacoes_confeccao_seasonal",
                          "cambio_media",
                          "cambio_confeccao",
                          "expectativa_cambio_2024_latest_transpose"
                          ],
                         ["date"]
    ))

#model evolução confecção
listModels.append(Models('modelo_confecao',"2002-01-01", "",
                          ["pim_pf_mensal_sc_seasonal[3.14_confecções_sc_seas]",
                          "rendimento_massa_mensal_real_defl_seasonal",
                          "rendimento_massa_tri_real_sc_trimonth_defl_seasonal",
                          "saldo_credito_pf_outros_defl",
                          "concessoes_credito_recursos_livres_pf_outros_seasonal",
                          "saldo_industrial_textil_vestuário_couro_defl",
                          "importacoes_confeccao_seasonal",
                          "cambio_media",
                          "cambio_confeccao",
                          "expectativa_cambio_2024_latest_transpose"
                          ],
                         ["date"]
    ))

#model evolução madeira
listModels.append(Models('modelo_madeira',"2002-01-01", "",
                          ["pim_pf_mensal_sc_seasonal[3.16_Madeira_sc_seas]"
                           #adicionar saldo imobiliario total, juros Reais BR e 30 year mortgage
                          ],
                         ["date"]
    ))

#model evolução Borracha e Plástico
listModels.append(Models('modelo_borracha_plastico',"2002-01-01", "",
                          ["pim_pf_mensal_sc_seasonal[3.22_Borracha_Plástico_sc_seas]"
                           #adicionar icc rl pj, inscc (?) e IBCBR
                          ],
                         ["date"]
    ))

#model evolução Minerais não Metálicos
listModels.append(Models('modelo_minerais_nao_metalicos',"2002-01-01", "",
                          ["pim_pf_mensal_sc_seasonal[3.23_Minerais_nâo_metálicos_sc_seas]",
                           "pim_pf_mensal_br_especiais_seasonal[2_InsumosConstr_sc_seas]",
                           "incc_m_rolling",
                           "construcao_medio_m_2_sc_defl_seasonal",
                           "invest_infra_sc_defl_seasonal",
                           "invest_liq_sc_transporte_defl_seasonal",
                           "rendimento_massa_mensal_real_defl_seasonal",
                           "rendimento_massa_tri_real_sc_trimonth_defl_seasonal",
                           "saldo_imobiliário_pj_total_defl_seasonal",
                           "saldo_imobiliário_pf_total_defl_seasonal",
                           "saldo_industrial_construção",
                           "saldo_industrial_obras",
                           "selic_mensal",                           
                           "expectativa_selic_latest_transpose_copomtomonth",
                           "ipca_mensal_taxa_variação_rolling",
                           "expectativa_ipca_2024_latest_transpose_rolling",
                           "cambio_minerais_nao_metalicos"
                          ],
                         ["date"]
    ))

