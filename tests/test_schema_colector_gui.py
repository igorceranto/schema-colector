import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import tkinter as tk

try:
    tk.Tk()
except tk.TclError:
    pytest.skip("Tkinter não disponível", allow_module_level=True)

from schema_colector import SchemaColector
from schema_colector_gui import SchemaColectorGUI

@pytest.fixture
def root():
    return tk.Tk()

@pytest.fixture
def app(root):
    return SchemaColectorGUI(root)

def test_gui_initialization(app):
    assert app is not None
    assert app.root is not None

def test_gui_components(app):
    # Verifica se alguns componentes principais foram criados
    assert hasattr(app, 'root')
    assert hasattr(app, 'log_text')
    assert hasattr(app, 'progress_bar')
    assert hasattr(app, 'progress_label')