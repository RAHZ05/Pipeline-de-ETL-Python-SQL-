import pandas as pd
import sqlite3
import logging
from datetime import datetime

# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class OrganizadorDados:
    """
    Classe responsável por realizar o ETL (Extract, Transform, Load) de planilhas.
    """

    def __init__(self, arquivo_origem, banco_destino):
        self.arquivo_origem = arquivo_origem
        self.banco_destino = banco_destino

    def extrair(self):
        """Lê o arquivo CSV e retorna um DataFrame Pandas."""
        logging.info(f"Iniciando extração do arquivo: {self.arquivo_origem}")
        try:
            df = pd.read_csv(self.arquivo_origem)
            logging.info(f"Extração concluída. Total de registros: {len(df)}")
            return df
        except FileNotFoundError:
            logging.error(f"Arquivo {self.arquivo_origem} não encontrado.")
            return None
        except Exception as e:
            logging.error(f"Erro inesperado na extração: {e}")
            return None

    def padronizar_cidades(self, df):
        """Padroniza nomes de cidades e estados."""
        mapeamento = {
            'SP': 'SAO PAULO',
            'SAO PAULO': 'SAO PAULO',
            'RJ': 'RIO DE JANEIRO',
            'RIO DE JANEIRO': 'RIO DE JANEIRO',
            'MINAS GERAIS': 'MINAS GERAIS',
            'MG': 'MINAS GERAIS'
        }
        
        # Converte para maiúsculo e remove espaços extras
        df['Cidade'] = df['Cidade'].str.strip().str.upper()
        # Aplica o mapeamento
        df['Cidade'] = df['Cidade'].replace(mapeamento)
        logging.info("Cidades padronizadas com sucesso.")
        return df

    def transformar(self, df):
        """Realiza a limpeza e padronização dos dados."""
        logging.info("Iniciando transformação dos dados...")
        df_limpo = df.copy()

        # 1. Remover Duplicatas
        linhas_antes = len(df_limpo)
        df_limpo = df_limpo.drop_duplicates()
        if linhas_antes > len(df_limpo):
            logging.info(f"Removidas {linhas_antes - len(df_limpo)} duplicatas.")

        # 2. Padronizar Nomes
        df_limpo['Nome'] = df_limpo['Nome'].fillna('SEM NOME').astype(str).str.upper()

        # 3. Padronizar Cidades (Chamando o método de padronização)
        df_limpo = self.padronizar_cidades(df_limpo)

        # 4. Corrigir Data
        df_limpo['Data'] = pd.to_datetime(df_limpo['Data'], dayfirst=True, errors='coerce')
        df_limpo['Data'] = df_limpo['Data'].fillna(datetime.now())

        # 5. Tratar Valor
        df_limpo['Valor'] = pd.to_numeric(df_limpo['Valor'], errors='coerce').fillna(0)

        logging.info("Transformação concluída.")
        return df_limpo

    def carregar(self, df_limpo, nome_tabela="vendas"):
        """Carrega o DataFrame limpo para o banco de dados SQLite."""
        if df_limpo is None or len(df_limpo) == 0:
            logging.warning("Nenhum dado para carregar.")
            return

        logging.info(f"Carregando dados para a tabela '{nome_tabela}' no banco {self.banco_destino}...")
        try:
            with sqlite3.connect(self.banco_destino) as conexao:
                df_limpo.to_sql(nome_tabela, conexao, if_exists='replace', index=False)
            logging.info("Carga concluída com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao carregar dados no SQL: {e}")

    def executar_pipeline(self):
        """Executa o fluxo completo de ETL."""
        df_bruto = self.extrair()
        if df_bruto is not None:
            df_tratado = self.transformar(df_bruto)
            self.carregar(df_tratado)
            logging.info("Pipeline de ETL finalizado com sucesso.")

# Execução
pipeline = OrganizadorDados(arquivo_origem='vendas_baguncadas.csv', banco_destino='meu_banco_profissional.db')
pipeline.executar_pipeline()