

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

