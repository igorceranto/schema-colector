import os
import cx_Oracle
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

class SchemaCollector:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.output_dir = "schema_objects"
        self.total_objects = 0
        self.processed_objects = 0
        
    def connect(self):
        """Estabelece conexão com o banco de dados Oracle"""
        try:
            self.connection = cx_Oracle.connect(
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                dsn=os.getenv('DB_DSN')
            )
            self.cursor = self.connection.cursor()
            logger.info("Conexão estabelecida com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
            raise

    def create_output_directories(self):
        """Cria diretórios para cada tipo de objeto"""
        object_types = ['TABLE', 'VIEW', 'PROCEDURE', 'FUNCTION', 'PACKAGE', 'TRIGGER', 'SEQUENCE']
        for obj_type in object_types:
            path = os.path.join(self.output_dir, obj_type.lower())
            os.makedirs(path, exist_ok=True)
            logger.info(f"Diretório criado: {path}")

    def get_object_definition(self, object_name, object_type):
        """Obtém a definição do objeto do banco de dados"""
        try:
            query = None
            
            if object_type == 'TABLE':
                query = """
                SELECT DBMS_METADATA.GET_DDL('TABLE', :1, :2) FROM DUAL
                """
            elif object_type == 'VIEW':
                query = """
                SELECT DBMS_METADATA.GET_DDL('VIEW', :1, :2) FROM DUAL
                """
            elif object_type == 'PROCEDURE':
                query = """
                SELECT DBMS_METADATA.GET_DDL('PROCEDURE', :1, :2) FROM DUAL
                """
            elif object_type == 'FUNCTION':
                query = """
                SELECT DBMS_METADATA.GET_DDL('FUNCTION', :1, :2) FROM DUAL
                """
            elif object_type == 'PACKAGE':
                query = """
                SELECT DBMS_METADATA.GET_DDL('PACKAGE', :1, :2) FROM DUAL
                """
            elif object_type == 'TRIGGER':
                query = """
                SELECT DBMS_METADATA.GET_DDL('TRIGGER', :1, :2) FROM DUAL
                """
            elif object_type == 'SEQUENCE':
                query = """
                SELECT DBMS_METADATA.GET_DDL('SEQUENCE', :1, :2) FROM DUAL
                """
            
            if query is None:
                logger.error(f"Tipo de objeto não suportado: {object_type}")
                return None
                
            self.cursor.execute(query, (object_name, os.getenv('DB_SCHEMA')))
            result = self.cursor.fetchone()[0]
            if result is not None:
                return str(result)
            return None
        except Exception as e:
            logger.error(f"Erro ao obter definição do objeto {object_name}: {str(e)}")
            return None

    def collect_objects(self):
        """Coleta todos os objetos do schema"""
        try:
            self.create_output_directories()
            
            # Consulta para obter todos os objetos do schema
            query = """
            SELECT OBJECT_NAME, OBJECT_TYPE 
            FROM ALL_OBJECTS 
            WHERE OWNER = :1 
            AND OBJECT_TYPE IN ('TABLE', 'VIEW', 'PROCEDURE', 'FUNCTION', 'PACKAGE', 'TRIGGER', 'SEQUENCE')
            ORDER BY OBJECT_TYPE, OBJECT_NAME
            """
            
            self.cursor.execute(query, (os.getenv('DB_SCHEMA'),))
            objects = self.cursor.fetchall()
            
            self.total_objects = len(objects)
            self.processed_objects = 0
            
            logger.info(f"Iniciando coleta de {self.total_objects} objetos...")
            
            for obj_name, obj_type in objects:
                definition = self.get_object_definition(obj_name, obj_type)
                
                if definition:
                    file_path = os.path.join(self.output_dir, obj_type.lower(), f"{obj_name}.sql")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(definition)
                    logger.info(f"Objeto {obj_name} ({obj_type}) coletado com sucesso!")
                
                self.processed_objects += 1
                progress = (self.processed_objects / self.total_objects) * 100
                logger.info(f"Objeto {obj_name} ({obj_type}) coletado com sucesso!")
                
        except Exception as e:
            logger.error(f"Erro durante a coleta dos objetos: {str(e)}")
            raise

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("Conexão fechada.")

def main():
    collector = SchemaCollector()
    try:
        collector.connect()
        collector.collect_objects()
    finally:
        collector.close()

if __name__ == "__main__":
    main() 