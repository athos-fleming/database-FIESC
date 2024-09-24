import os
import requests
import pandas as pd

class Variables(object):
    def __init__(self,name,codigoId, dataInicial,APIadress,ColumnNames,codeCreateSQL,codeInsertSQL):
        self.name = name
        self.codigoId = codigoId
        self.dataInicial = dataInicial
        self.APIadress = APIadress
        self.ColumnNames = ColumnNames
        self.codeCreateSQL = codeCreateSQL
        self.codeInsertSQL = codeInsertSQL

listVariables = []

'''
#variavel teste
listVariables.append(Variables('top_scorers',"0", "01/01/2000", "RapidAPI", {"nome da coluna"},
    """
    CREATE TABLE IF NOT EXISTS top_scorers (
        `position` INT,
        `player` VARCHAR(255),
        `club` VARCHAR(255),
        `total_goals` INT,
        `penalty_goals` INT,
        `assists` INT,
        `matches` INT,
        `mins` INT,
        `age` INT,
        PRIMARY KEY (`player`, `club`)
    );
    """,
    """
    INSERT INTO top_scorers (`position`, `player`, `club`, `total_goals`, `penalty_goals`, `assists`, `matches`, `mins`, `age`)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        `total_goals` = VALUES(`total_goals`),
        `penalty_goals` = VALUES(`penalty_goals`),
        `assists` = VALUES(`assists`),
        `matches` = VALUES(`matches`),
        `mins` = VALUES(`mins`),
        `age` = VALUES(`age`)
    """
    ))
'''

#variavel SELIC Mensal % a.m. de teste
listVariables.append(Variables('Selic_mensal',"4189","01/01/2000","bcb",
                               {"data": "data","valor": "valor"},
    """
    CREATE TABLE IF NOT EXISTS Selic_mensal (
        `data` VARCHAR(255),
        `valor` DECIMAL(4,2),
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
listVariables.append(Variables('Selic_diaria',"11","01/01/2000","bcb",
                               {"data": "data","valor": "valor"},
    """
    CREATE TABLE IF NOT EXISTS Selic_diaria (
        `data` VARCHAR(255),
        `valor` DECIMAL(8,6),
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

#variavel IPCA - geral - taxa de variação  mensa % a.m.
listVariables.append(Variables('IPCA_mensal_taxa_variação',"'PRECOS12_IPCAG12'","01/01/1980","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_núcleo_médias_aparadas_suavização',"'BM12_IPCA2012'","01/01/1992","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização',"'BM12_IPCA20N12'","01/01/1992","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_núcleo_exclusão',"'BM12_IPCAEXCEX212'","01/01/1992","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_núcleo_exclusão_domiciliar',"'BM12_IPCAEXC12'","01/01/1992","ipea",
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
listVariables.append(Variables('IPCA_mensal_taxa_preços_livres_serviços',"'BM12_IPCAPLSER12'","01/01/1992","ipea",
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