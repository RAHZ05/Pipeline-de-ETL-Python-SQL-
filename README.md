Data Pipeline: ETL de Vendas (Python + SQL)
* Sobre o Projeto
Este projeto demonstra a construção de um pipeline de ETL (Extract, Transform, Load) robusto, focado na limpeza e estruturação de dados. O objetivo é transformar uma planilha de vendas "bagunçada" — contendo inconsistências, duplicatas e erros de formatação — em um banco de dados relacional organizado e pronto para análise estratégica.

O pipeline foi desenvolvido seguindo boas práticas de engenharia de software, utilizando Programação Orientada a Objetos (POO), tratamento de erros e logs de monitoramento.

* Tecnologias
Linguagem: Python 3

Manipulação de Dados: Pandas

Banco de Dados: SQLite

Monitoramento: Logging (Biblioteca padrão do Python)

* Funcionalidades Implementadas
Extração: Leitura eficiente de arquivos CSV.

Transformação:

Remoção de registros duplicados.

Padronização de strings (nomes e cidades).

Normalização categórica (mapeamento de abreviações de cidades).

Tratamento de datas e valores numéricos com coerção de erros.

Carga: Persistência dos dados tratados em um banco de dados relacional.

Resiliência: Tratamento de exceções (try/except) e logs detalhados de cada etapa.

* Estrutura do Fluxo de Dados
O processo segue uma lógica de arquitetura de dados profissional:

Extract: Importa o CSV bruto.

Transform: Limpa e padroniza as informações (limpeza de nomes, datas, valores e normalização de cidades).

Load: Insere os dados processados em um banco SQLite.

<img width="1750" height="782" alt="carbon" src="https://github.com/user-attachments/assets/d6ccc428-7f38-4f44-a86d-59a7d82e1ee2" />
