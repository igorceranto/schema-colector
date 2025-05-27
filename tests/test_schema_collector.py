import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from schema_collector import SchemaCollector

@pytest.fixture
def collector():
    return SchemaCollector()

@pytest.fixture
def mock_cursor():
    cursor = MagicMock()
    cursor.fetchone.return_value = ["CREATE TABLE TEST_TABLE..."]
    cursor.fetchall.return_value = [
        ("TEST_TABLE", "TABLE"),
        ("TEST_VIEW", "VIEW"),
        ("TEST_PROC", "PROCEDURE")
    ]
    return cursor

@pytest.fixture
def mock_connection(mock_cursor):
    connection = MagicMock()
    connection.cursor.return_value = mock_cursor
    return connection

def test_initialization(collector):
    """Testa a inicialização do SchemaCollector"""
    assert collector.connection is None
    assert collector.cursor is None
    assert collector.output_dir == "schema_objects"
    assert collector.total_objects == 0
    assert collector.processed_objects == 0

@patch('cx_Oracle.connect')
def test_connect_success(mock_connect, collector, mock_connection):
    """Testa conexão bem-sucedida com o banco de dados"""
    mock_connect.return_value = mock_connection
    collector.connect()
    assert collector.connection is not None
    assert collector.cursor is not None

@patch('cx_Oracle.connect')
def test_connect_exception_logging(mock_connect, collector, caplog):
    mock_connect.side_effect = Exception("Erro de conexão")
    with pytest.raises(Exception):
        collector.connect()
    assert any("Erro ao conectar ao banco de dados" in m for m in caplog.text.splitlines())

def test_create_output_directories(collector):
    """Testa a criação dos diretórios de saída"""
    collector.create_output_directories()
    for obj_type in ['table', 'view', 'procedure', 'function', 'package', 'trigger', 'sequence']:
        path = os.path.join(collector.output_dir, obj_type)
        assert os.path.exists(path)

@patch('os.getenv')
def test_get_object_definition(mock_getenv, collector, mock_cursor):
    """Testa a obtenção da definição de um objeto"""
    mock_getenv.return_value = "TEST_SCHEMA"
    collector.cursor = mock_cursor
    
    # Testa diferentes tipos de objetos
    object_types = ['TABLE', 'VIEW', 'PROCEDURE', 'FUNCTION', 'PACKAGE', 'TRIGGER', 'SEQUENCE']
    for obj_type in object_types:
        definition = collector.get_object_definition("TEST_OBJECT", obj_type)
        assert definition is not None
        assert isinstance(definition, str)

@patch('os.getenv')
def test_get_object_definition_invalid_type(mock_getenv, collector):
    """Testa a obtenção de definição para tipo de objeto inválido"""
    mock_getenv.return_value = "TEST_SCHEMA"
    definition = collector.get_object_definition("TEST_OBJECT", "INVALID_TYPE")
    assert definition is None

@patch('os.getenv')
def test_get_object_definition_exception(mock_getenv, collector):
    mock_getenv.return_value = "TEST_SCHEMA"
    class DummyCursor:
        def execute(self, *a, **kw):
            raise Exception("Erro de execução")
    collector.cursor = DummyCursor()
    result = collector.get_object_definition("OBJ", "TABLE")
    assert result is None

@patch('os.getenv')
def test_collect_objects(mock_getenv, collector, mock_cursor):
    """Testa a coleta de objetos"""
    mock_getenv.return_value = "TEST_SCHEMA"
    collector.cursor = mock_cursor
    
    collector.collect_objects()
    assert collector.total_objects == 3
    assert collector.processed_objects == 3

@patch('os.getenv')
def test_collect_objects_exception(mock_getenv, collector):
    mock_getenv.return_value = "TEST_SCHEMA"
    class DummyCursor:
        def execute(self, *a, **kw):
            raise Exception("Erro de execução")
    collector.cursor = DummyCursor()
    with pytest.raises(Exception):
        collector.collect_objects()

def test_close(collector, mock_connection, mock_cursor):
    """Testa o fechamento da conexão"""
    collector.connection = mock_connection
    collector.cursor = mock_cursor
    collector.close()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()

def test_close_without_connection(collector):
    # Não deve lançar exceção se não houver conexão/cursor
    collector.close() 