import os
import requests
import pandas as pd

class Variables(object):
    def __init__(self,name,frequencia,codigo, dictParameters,APIadress,ColumnNames,codeCreateSQL,codeInsertSQL):
        self.name = name
        self.frequencia = frequencia
        self.codigo = codigo
        self.dictParameters = dictParameters
        self.APIadress = APIadress
        self.ColumnNames = ColumnNames
        self.codeCreateSQL = codeCreateSQL
        self.codeInsertSQL = codeInsertSQL

class Models:
    def __init__(self,name,codigo,frequencia,codeCreateSQL,codeInsertSQL):
        self.name = name
        self.codigo = codigo
        self.frequencia = frequencia
        self.codeCreateSQL = codeCreateSQL
        self.codeInsertSQL = codeInsertSQL

listVariables = []
listModels = []

#grupo do ipea, corre bem tranquilo


#variavel IPCA - geral - taxa de variação  mensa % a.m.
listVariables.append(Variables('ipca_mensal_taxa_variação',"mensal","'PRECOS12_IPCAG12'","01/01/1980","ipea",
                               {"VALDATA": "data","VALVALOR": "valor"},
    """
    CREATE TABLE IF NOT EXISTS IPCA_mensal_taxa_variação (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO IPCA_mensal_taxa_variação (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))

#variavel IPCA - núcleo médias aparadas com suavização - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_médias_aparadas_suavização',"mensal","'BM12_IPCA2012'","01/01/1992","ipea",
                               {"VALDATA": "data","VALVALOR": "valor"},
    """
    CREATE TABLE IF NOT EXISTS IPCA_mensal_taxa_núcleo_médias_aparadas_suavização (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO IPCA_mensal_taxa_núcleo_médias_aparadas_suavização (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))

#variavel IPCA - núcleo médias aparadas sem suavização - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_médias_aparadas_sem_suavização',"mensal","'BM12_IPCA20N12'","01/01/1992","ipea",
                               {"VALDATA": "data","VALVALOR": "valor"},
    """
    CREATE TABLE IF NOT EXISTS IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))

#variavel IPCA - núcleo por exclusão - EX1 - taxa de variação % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_exclusão',"mensal","'BM12_IPCAEXCEX212'","01/01/1992","ipea",
                               {"VALDATA": "data","VALVALOR": "valor"},
    """
    CREATE TABLE IF NOT EXISTS IPCA_mensal_taxa_núcleo_exclusão (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO IPCA_mensal_taxa_núcleo_exclusão (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))

#variavel IPCA - núcleo por exclusão - sem monitorados e alimentos no domicílio % a.m.
listVariables.append(Variables('ipca_mensal_taxa_núcleo_exclusão_domiciliar',"mensal","'BM12_IPCAEXC12'","01/01/1992","ipea",
                               {"VALDATA": "data","VALVALOR": "valor"},
    """
    CREATE TABLE IF NOT EXISTS IPCA_mensal_taxa_núcleo_exclusão_domiciliar (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO IPCA_mensal_taxa_núcleo_exclusão_domiciliar (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))

#variavel IPCA - preços livres - serviços % a.m.
listVariables.append(Variables('ipca_mensal_taxa_preços_livres_serviços',"mensal","'BM12_IPCAPLSER12'","01/01/1992","ipea",
                               {"VALDATA": "data","VALVALOR": "valor"},
    """
    CREATE TABLE IF NOT EXISTS IPCA_mensal_taxa_preços_livres_serviços (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO IPCA_mensal_taxa_preços_livres_serviços (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))

#variavel PIB - Mensal % a.m.
listVariables.append(Variables('pib_mensal_taxa_variação',"mensal","'BM12_PIB12'","01/01/1990","ipea",
                               {"VALDATA": "data","VALVALOR": "valor"},
    """
    CREATE TABLE IF NOT EXISTS PIB_mensal_taxa_variação (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO PIB_mensal_taxa_variação (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))


#grupo do bcb, as vezes da erro de api call


#variavel Dívida líquida do governo geral (% PIB) % a.m.
listVariables.append(Variables('divida_mensal_publica__liquida_consolidado_pib',"mensal","4513","01/12/2001","bcb",
                               {"data": "data","valor": "valor"},
    """
    CREATE TABLE IF NOT EXISTS Divida_mensal_publica__liquida_consolidado_PIB (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO Divida_mensal_publica__liquida_consolidado_PIB (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))

#variavel Dívida bruta do governo geral (% PIB) % a.m.
listVariables.append(Variables('divida_mensal_publica__bruta_pib',"mensal","13762","01/12/2006","bcb",
                               {"data": "data","valor": "valor"},
    """
    CREATE TABLE IF NOT EXISTS Divida_mensal_publica__bruta_PIB (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO Divida_mensal_publica__bruta_PIB (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))

#variavel SELIC Mensal % a.m.
listVariables.append(Variables('selic_mensal',"mensal","4189","01/01/2000","bcb",
                               {"data": "data","valor": "valor"},
    """
    CREATE TABLE IF NOT EXISTS Selic_mensal (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO Selic_mensal (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))

#variavel SELIC diaria % a.a.
listVariables.append(Variables('selic_diaria',"diaria","11","01/01/2000","bcb",
                               {"data": "data","valor": "valor"},
    """
    CREATE TABLE IF NOT EXISTS Selic_diaria (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO Selic_diaria (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))


#grupo do sidra


#variavel IPCA - geral - taxa de variação  mensa % a.m.
listVariables.append(Variables('pim_pf_mensal',"mensal","8888",
                               {"periodos":"202001|202002|202003|202004|202005|202006|202007|202008|202009|202010|202011|202012|202101|202102|202103|202104|202105|202106|202107|202108|202109|202110|202111|202112|202201|202202|202203|202204|202205|202206|202207|202208|202209|202210|202211|202212|202301|202302|202303|202304|202305|202306|202307|202308|202309|202310|202311|202312|202401|202402|202403|202404|202405|202406|202407",
                                "variaveis":"12606","localidade":"N3[42]","classificacao":"544[all]"},"sidra",
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
                               },
                               
                               
                               
    """
    CREATE TABLE IF NOT EXISTS IPCA_mensal_taxa_variação (
        `data` VARCHAR(255),
        `valor` FLOAT,
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO IPCA_mensal_taxa_variação (`data`,`valor`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `valor` = VALUES(`valor`);
    """
    ))


#models estabelecidos

listModels.append(Models("Model_mensal","mensal", "mensal",
    """
    CREATE TABLE IF NOT EXISTS Model_mensal (
        `data` VARCHAR(255),
        `IPCA_mensal_taxa_variação` float,
        `IPCA_mensal_taxa_núcleo_médias_aparadas_suavização` float,
        `IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização` float,
        `IPCA_mensal_taxa_núcleo_exclusão` float,
        `IPCA_mensal_taxa_núcleo_exclusão_domiciliar` float,
        `IPCA_mensal_taxa_preços_livres_serviços` float,
        `PIB_mensal_taxa_variação` float,
        `Divida_mensal_publica__liquida_consolidado_PIB` float,
        `Divida_mensal_publica__bruta_PIB` float,
        `Selic_mensal` float,        
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO Model_mensal (`data`,
                            `IPCA_mensal_taxa_variação`,
                            `IPCA_mensal_taxa_núcleo_médias_aparadas_suavização`,
                            `IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização`,
                            `IPCA_mensal_taxa_núcleo_exclusão`,
                            `IPCA_mensal_taxa_núcleo_exclusão_domiciliar`,
                            `PIB_mensal_taxa_variação`,
                            `IPCA_mensal_taxa_preços_livres_serviços`,
                            `Divida_mensal_publica__liquida_consolidado_PIB`,
                            `Divida_mensal_publica__bruta_PIB`,
                            `Selic_mensal`
                            )
    Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        `IPCA_mensal_taxa_variação` = VALUES(`IPCA_mensal_taxa_variação`),
        `IPCA_mensal_taxa_núcleo_médias_aparadas_suavização` = VALUES(`IPCA_mensal_taxa_núcleo_médias_aparadas_suavização`),
        `IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização` = VALUES(`IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização`),
        `IPCA_mensal_taxa_núcleo_exclusão` = VALUES(`IPCA_mensal_taxa_núcleo_exclusão`),
        `IPCA_mensal_taxa_núcleo_exclusão_domiciliar` = VALUES(`IPCA_mensal_taxa_núcleo_exclusão_domiciliar`),
        `IPCA_mensal_taxa_preços_livres_serviços` = VALUES(`IPCA_mensal_taxa_preços_livres_serviços`),
        `PIB_mensal_taxa_variação` = VALUES(`PIB_mensal_taxa_variação`),
        `Divida_mensal_publica__liquida_consolidado_PIB` = VALUES(`Divida_mensal_publica__liquida_consolidado_PIB`),
        `Divida_mensal_publica__bruta_PIB` = VALUES(`Divida_mensal_publica__bruta_PIB`),
        `Selic_mensal` = VALUES(`Selic_mensal`);
    """
    ))




