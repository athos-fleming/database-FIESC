import os
import requests
import pandas as pd

class Variables(object):
    def __init__(self,name,frequencia,codigo, dataInicial,APIadress,ColumnNames,codeCreateSQL,codeInsertSQL):
        self.name = name
        self.frequencia = frequencia
        self.codigo = codigo
        self.dataInicial = dataInicial
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
listVariables.append(Variables('IPCA_mensal_taxa_variação',"mensal","'PRECOS12_IPCAG12'","01/01/1980","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_núcleo_médias_aparadas_suavização',"mensal","'BM12_IPCA2012'","01/01/1992","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização',"mensal","'BM12_IPCA20N12'","01/01/1992","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_núcleo_exclusão',"mensal","'BM12_IPCAEXCEX212'","01/01/1992","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_núcleo_exclusão_domiciliar',"mensal","'BM12_IPCAEXC12'","01/01/1992","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_preços_livres_serviços',"mensal","'BM12_IPCAPLSER12'","01/01/1992","ipea",
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
listVariables.append(Variables('PIB_mensal_taxa_variação',"mensal","'BM12_PIB12'","01/01/1990","ipea",
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
listVariables.append(Variables('Divida_mensal_publica__liquida_consolidado_PIB',"mensal","4513","01/12/2001","bcb",
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
listVariables.append(Variables('Divida_mensal_publica__bruta_PIB',"mensal","13762","01/12/2006","bcb",
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
listVariables.append(Variables('Selic_mensal',"mensal","4189","01/01/2000","bcb",
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
listVariables.append(Variables('Selic_diaria',"diaria","11","01/01/2000","bcb",
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




