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

#variavel SELIC
listVariables.append(Variables('Selic',"4189","01/01/2000","bcb",{"data": "data","valor": "Selic"},
    """
    CREATE TABLE IF NOT EXISTS Selic_mensal (
        `data` VARCHAR(255),
        `Selic` DECIMAL(4,2),
        PRIMARY KEY (`data`)
    );

    """,
    """
    INSERT INTO Selic_mensal (`data`,`Selic`)
    Values(%s, %s)
    ON DUPLICATE KEY UPDATE
        `Selic` = VALUES(`Selic`);
    """
    ))



