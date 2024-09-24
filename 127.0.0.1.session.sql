

--create table de agrupamento para importar no excel com maior coerencia e sem repetição
CREATE TABLE IF NOT EXISTS agrupamento.agrupamento_mensal (
        `data` VARCHAR(255),
        `Selic_mensal_taxa_variação` float,
        `IPCA_mensal_taxa_variação` float,
        `IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização` float,
        `IPCA_mensal_taxa_núcleo_médias_aparadas_suavização` float,
        `IPCA_mensal_taxa_núcleo_exclusão` float,
        `IPCA_mensal_taxa_núcleo_exclusão_domiciliar` float,
        `IPCA_mensal_taxa_preços_livres_serviços` float,
        PRIMARY KEY (`data`)
    );

/*talvez nao funcione, possivel problema de ON DUPLICATE nao entender pq cada uma das variaveis vem de um lugar, entao a PRIMARY KEY é bugada
ter que fazer para cada um talvez? e ai importa a variavel e a data em todos, usando a data para verificar duplicata
INSERT INTO newTable (col1, col2, col3)
    SELECT column1, column2, column3
    FROM oldTable
    ON DUPLICATE KEY UPDATE
*/

/*
INSERT INTO agrupamento.agrupamento_mensal (`data`,`Selic_mensal_taxa_variação`,
                                `IPCA_mensal_taxa_variação`,
                                `IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização`,
                                `IPCA_mensal_taxa_núcleo_médias_aparadas_suavização`,
                                `IPCA_mensal_taxa_núcleo_exclusão`,
                                `IPCA_mensal_taxa_núcleo_exclusão_domiciliar`,
                                `IPCA_mensal_taxa_preços_livres_serviços`)
    Values(%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        `Selic_mensal_taxa_variação` = VALUES(`Selic_mensal_taxa_variação`),
        `IPCA_mensal_taxa_variação` = VALUES(`IPCA_mensal_taxa_variação`),
        `IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização` = VALUES(`IPCA_mensal_taxa_núcleo_médias_aparadas_sem_suavização`),
        `IPCA_mensal_taxa_núcleo_médias_aparadas_suavização` = VALUES(`IPCA_mensal_taxa_núcleo_médias_aparadas_suavização`),
        `IPCA_mensal_taxa_núcleo_exclusão` = VALUES(`IPCA_mensal_taxa_núcleo_exclusão`),
        `IPCA_mensal_taxa_núcleo_exclusão_domiciliar` = VALUES(`IPCA_mensal_taxa_núcleo_exclusão_domiciliar`),
        `IPCA_mensal_taxa_preços_livres_serviços` = VALUES(`IPCA_mensal_taxa_preços_livres_serviços`);
    """
*/


