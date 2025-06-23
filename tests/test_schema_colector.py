import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from schema_colector import SchemaColector

@pytest.fixture
def colector():
    return SchemaColector()

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

def test_initialization(colector):
    """Testa a inicialização do SchemaColector"""
    assert colector.connection is None
    assert colector.cursor is None
    assert colector.output_dir == "schema_objects"
    assert colector.total_objects == 0
    assert colector.processed_objects == 0

@patch('cx_Oracle.connect')
def test_connect_success(mock_connect, colector, mock_connection):
    """Testa conexão bem-sucedida com o banco de dados"""
    mock_connect.return_value = mock_connection
    colector.connect()
    assert colector.connection is not None
    assert colector.cursor is not None

@patch('cx_Oracle.connect')
def test_connect_exception_logging(mock_connect, colector, caplog):
    mock_connect.side_effect = Exception("Erro de conexão")
    with pytest.raises(Exception):
        colector.connect()
    assert any("Erro ao conectar ao banco de dados" in m for m in caplog.text.splitlines())

@patch('os.getenv')
def test_get_object_definition(mock_getenv, colector, mock_cursor):
    """Testa a obtenção da definição de um objeto"""
    mock_getenv.return_value = "TEST_SCHEMA"
    colector.cursor = mock_cursor
    
    # Testa diferentes tipos de objetos
    object_types = ['TABLE', 'VIEW', 'PROCEDURE', 'FUNCTION', 'PACKAGE', 'TRIGGER', 'SEQUENCE']
    for obj_type in object_types:
        definition = colector.get_object_definition("TEST_OBJECT", obj_type)
        assert definition is not None
        assert isinstance(definition, str)

@patch('os.getenv')
def test_get_object_definition_invalid_type(mock_getenv, colector):
    """Testa a obtenção de definição para tipo de objeto inválido"""
    mock_getenv.return_value = "TEST_SCHEMA"
    definition = colector.get_object_definition("TEST_OBJECT", "INVALID_TYPE")
    assert definition is None

@patch('os.getenv')
def test_get_object_definition_exception(mock_getenv, colector):
    mock_getenv.return_value = "TEST_SCHEMA"
    class DummyCursor:
        def execute(self, *a, **kw):
            raise Exception("Erro de execução")
    colector.cursor = DummyCursor()
    result = colector.get_object_definition("OBJ", "TABLE")
    assert result is None

@patch('os.getenv')
def test_collect_objects(mock_getenv, colector, mock_cursor):
    """Testa a coleta de objetos"""
    mock_getenv.return_value = "TEST_SCHEMA"
    colector.cursor = mock_cursor
    
    colector.collect_objects()
    assert colector.total_objects == 3
    assert colector.processed_objects == 3

@patch('os.getenv')
def test_collect_objects_exception(mock_getenv, colector):
    mock_getenv.return_value = "TEST_SCHEMA"
    class DummyCursor:
        def execute(self, *a, **kw):
            raise Exception("Erro de execução")
    colector.cursor = DummyCursor()
    with pytest.raises(Exception):
        colector.collect_objects()

def test_close(colector, mock_connection, mock_cursor):
    """Testa o fechamento da conexão"""
    colector.connection = mock_connection
    colector.cursor = mock_cursor
    colector.close()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()

def test_close_without_connection(colector):
    # Não deve lançar exceção se não houver conexão/cursor
    colector.close() 