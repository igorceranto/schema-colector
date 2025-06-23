import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from schema_colector import SchemaColector
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import re

class ModernTheme:
    # Cores
    PRIMARY = "#2196F3"
    SECONDARY = "#757575"
    SUCCESS = "#4CAF50"
    ERROR = "#F44336"
    WARNING = "#FFC107"
    INFO = "#2196F3"
    BACKGROUND = "#FFFFFF"
    SURFACE = "#F5F5F5"
    TEXT = "#212121"
    TEXT_SECONDARY = "#757575"
    ERROR_BG = "#ffeaea"
    
    # Estilos
    @staticmethod
    def apply_theme(root):
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Configurar cores dos widgets
        style.configure('TFrame', background=ModernTheme.BACKGROUND)
        style.configure('TLabel', background=ModernTheme.BACKGROUND, foreground=ModernTheme.TEXT)
        
        # Configurar botões
        style.configure('TButton', 
                       background=ModernTheme.PRIMARY,
                       foreground='white',
                       padding=(8, 2),
                       font=('Segoe UI', 9),
                       relief='groove',
                       borderwidth=1)
        
        # Configurar estado dos botões
        style.map('TButton',
                 background=[('active', ModernTheme.PRIMARY),
                           ('disabled', ModernTheme.SECONDARY)],
                 foreground=[('active', 'white'),
                           ('disabled', 'white')])
        
        # Configurar campos de entrada
        style.configure('TEntry', 
                       fieldbackground=ModernTheme.SURFACE,
                       foreground=ModernTheme.TEXT,
                       padding=3)
        
        # Configurar frames
        style.configure('TLabelframe', 
                       background=ModernTheme.BACKGROUND,
                       foreground=ModernTheme.TEXT)
        style.configure('TLabelframe.Label', 
                       background=ModernTheme.BACKGROUND,
                       foreground=ModernTheme.TEXT)
        
        # Configurar barra de progresso
        style.configure("Horizontal.TProgressbar",
                       background=ModernTheme.PRIMARY,
                       troughcolor=ModernTheme.SURFACE)

class SchemaColectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Schema colector")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        self.root.configure(bg=ModernTheme.BACKGROUND)
        
        # Aplicar tema moderno
        ModernTheme.apply_theme(root)
        
        # Variáveis
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.dsn_var = tk.StringVar()
        self.schema_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value="schema_objects")
        
        # Carregar configurações do .env se existir
        load_dotenv()
        self.username_var.set(os.getenv('DB_USER', ''))
        self.password_var.set(os.getenv('DB_PASSWORD', ''))
        self.dsn_var.set(os.getenv('DB_DSN', ''))
        self.schema_var.set(os.getenv('DB_SCHEMA', ''))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Título e descrição
        ttk.Label(self.root, text="Schema colector", font=("Segoe UI", 15, "bold"), background=ModernTheme.BACKGROUND, foreground=ModernTheme.PRIMARY).pack(pady=(8,0))
        ttk.Label(self.root, text="Ferramenta para exportar objetos de um schema Oracle", font=("Segoe UI", 9), background=ModernTheme.BACKGROUND, foreground=ModernTheme.SECONDARY).pack(pady=(0,6))

        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(1, weight=1)
        
        # Frame de configuração
        config_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="6")
        config_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 6))
        for i in range(3):
            config_frame.rowconfigure(i, pad=4)
        for j in range(2):
            config_frame.columnconfigure(j, weight=1)
        # Primeira coluna
        ttk.Label(config_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=(0,5), pady=2)
        ttk.Entry(config_frame, textvariable=self.username_var, width=22).grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Label(config_frame, text="DSN:").grid(row=1, column=0, sticky=tk.W, padx=(0,5), pady=2)
        ttk.Entry(config_frame, textvariable=self.dsn_var, width=22).grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Label(config_frame, text="Diretório de Saída:").grid(row=2, column=0, sticky=tk.W, padx=(0,5), pady=2)
        output_frame = ttk.Frame(config_frame)
        output_frame.grid(row=2, column=1, sticky=tk.W, pady=2)
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=14).pack(side=tk.LEFT, padx=2)
        ttk.Button(output_frame, text="Procurar", command=self.browse_output_dir).pack(side=tk.LEFT)
        # Segunda coluna
        ttk.Label(config_frame, text="Password:").grid(row=0, column=2, sticky=tk.W, padx=(20,5), pady=2)
        ttk.Entry(config_frame, textvariable=self.password_var, show="*", width=22).grid(row=0, column=3, sticky=tk.W, pady=2)
        ttk.Label(config_frame, text="Schema:").grid(row=1, column=2, sticky=tk.W, padx=(20,5), pady=2)
        ttk.Entry(config_frame, textvariable=self.schema_var, width=22).grid(row=1, column=3, sticky=tk.W, pady=2)
        # Adicionar campo para nome do objeto específico
        ttk.Label(config_frame, text="Nome do Objeto:").grid(row=2, column=2, sticky=tk.W, padx=(20,5), pady=2)
        self.object_name_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.object_name_var, width=22).grid(row=2, column=3, sticky=tk.W, pady=2)
        # Ajustar colunas
        for j in range(4):
            config_frame.columnconfigure(j, weight=1)
        
        # Frame de progresso
        progress_frame = ttk.LabelFrame(main_frame, text="Progresso", padding="6")
        progress_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 6))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                          length=400, 
                                          mode='determinate', 
                                          variable=self.progress_var,
                                          style="Horizontal.TProgressbar")
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=3, pady=3)
        
        self.progress_label = ttk.Label(progress_frame, text="0%", font=("Segoe UI", 9, "bold"))
        self.progress_label.grid(row=0, column=1, padx=6)
        
        # Frame de log
        log_frame = ttk.LabelFrame(main_frame, text="Log de Execução", padding="6")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 6))
        
        # Área de log com fonte monoespaçada
        self.log_text = tk.Text(log_frame, 
                              height=8, 
                              width=70,
                              font=('Consolas', 9),
                              wrap=tk.WORD,
                              bg=ModernTheme.SURFACE,
                              fg=ModernTheme.TEXT,
                              borderwidth=0,
                              highlightthickness=0)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para o log
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Configurar grid do log_frame
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Tags para logs
        self.log_text.tag_configure("INFO", foreground=ModernTheme.INFO)
        self.log_text.tag_configure("ERROR", foreground=ModernTheme.ERROR, background=ModernTheme.ERROR_BG, font=('Consolas', 9, 'bold'))
        self.log_text.tag_configure("WARNING", foreground=ModernTheme.WARNING)
        self.log_text.tag_configure("SUCCESS", foreground=ModernTheme.SUCCESS)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=6)
        
        # Botão Iniciar Coleta
        start_button = ttk.Button(button_frame, 
                                 text="Iniciar Coleta", 
                                 command=self.start_collection,
                                 cursor="hand2")
        start_button.pack(side=tk.LEFT, padx=3)
        
        # Botão Extrair Objeto Específico
        extract_button = ttk.Button(button_frame, 
                                   text="Extrair Objeto Específico", 
                                   command=self.extract_specific_object,
                                   cursor="hand2")
        extract_button.pack(side=tk.LEFT, padx=3)
        
        # Botão Salvar Configurações
        save_button = ttk.Button(button_frame, 
                                text="Salvar Configurações", 
                                command=self.save_config,
                                cursor="hand2")
        save_button.pack(side=tk.LEFT, padx=3)
        
        # Botão Limpar Log
        clear_button = ttk.Button(button_frame, 
                                 text="Limpar Log", 
                                 command=lambda: self.log_text.delete(1.0, tk.END),
                                 cursor="hand2")
        clear_button.pack(side=tk.LEFT, padx=3)
        
        # Botão Sair
        exit_button = ttk.Button(button_frame, 
                                text="Sair", 
                                command=self.root.quit,
                                cursor="hand2")
        exit_button.pack(side=tk.LEFT, padx=3)
        
        # Rodapé
        footer = ttk.Label(self.root, text="Desenvolvido por Igor Ceranto", font=("Segoe UI", 8), foreground=ModernTheme.SECONDARY, background=ModernTheme.BACKGROUND, anchor="center")
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 16))
        
    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
            
    def log_message(self, message, level="INFO"):
        """Adiciona uma mensagem ao log com formatação colorida"""
        icons = {
            "INFO": "ℹ️ ",
            "ERROR": "✖ ",
            "WARNING": "⚠️ ",
            "SUCCESS": "✔ "
        }
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"{icons.get(level, '')}[{timestamp}] {message}"
        
        self.log_text.insert(tk.END, formatted_message + "\n", level)
        self.log_text.see(tk.END)
        
    def save_config(self):
        config = f"""DB_USER={self.username_var.get()}
DB_PASSWORD={self.password_var.get()}
DB_DSN={self.dsn_var.get()}
DB_SCHEMA={self.schema_var.get()}
"""
        try:
            with open('.env', 'w') as f:
                f.write(config)
            self.log_message("Configurações salvas com sucesso!", "SUCCESS")
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except Exception as e:
            self.log_message(f"Erro ao salvar configurações: {str(e)}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
            
    def start_collection(self):
        # Validar campos
        if not all([self.username_var.get(), self.password_var.get(), 
                   self.dsn_var.get(), self.schema_var.get()]):
            self.log_message("Todos os campos são obrigatórios!", "ERROR")
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
            
        # Limpar log
        self.log_text.delete(1.0, tk.END)
        
        # Iniciar coleta em uma thread separada
        thread = threading.Thread(target=self.collect_schema)
        thread.daemon = True
        thread.start()
        
    def collect_schema(self):
        try:
            # Configurar logging para a interface
            class GUILogHandler(logging.Handler):
                def __init__(self, text_widget, progress_var, progress_label, log_message_func):
                    logging.Handler.__init__(self)
                    self.text_widget = text_widget
                    self.progress_var = progress_var
                    self.progress_label = progress_label
                    self.log_message_func = log_message_func
                    
                def emit(self, record):
                    msg = self.format(record)
                    def append():
                        level = record.levelname
                        self.log_message_func(msg, level)
                        
                        # Atualizar progresso se a mensagem contiver informações de progresso
                        if "Objeto" in msg and "coletado com sucesso" in msg:
                            try:
                                # Extrair nome e tipo do objeto
                                match = re.search(r"Objeto (.+) \((.+)\) coletado com sucesso", msg)
                                if match:
                                    obj_name = match.group(1)
                                    # Atualizar contagem
                                    progress = (self.progress_var.get())
                                    # Extrair contagem do log anterior
                                    # O valor de self.progress_var já está em %
                                    # Buscar a contagem atual e total
                                    processed = int(self.progress_var.get() / 100 * self.total_objects) if hasattr(self, 'total_objects') and self.total_objects else ''
                                    total = self.total_objects if hasattr(self, 'total_objects') else ''
                                    # Atualizar label
                                    self.progress_label.configure(text=f"{progress:.1f}% {processed}/{total} {obj_name}.sql")
                            except Exception as e:
                                pass
                    self.text_widget.after(0, append)
            
            # Configurar logger
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            gui_handler = GUILogHandler(self.log_text, self.progress_var, self.progress_label, self.log_message)
            gui_handler.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(gui_handler)
            
            # Criar e executar o coletor
            colector = SchemaColector()
            colector.output_dir = self.output_dir_var.get()
            
            # Configurar variáveis de ambiente
            os.environ['DB_USER'] = self.username_var.get()
            os.environ['DB_PASSWORD'] = self.password_var.get()
            os.environ['DB_DSN'] = self.dsn_var.get()
            os.environ['DB_SCHEMA'] = self.schema_var.get()
            
            colector.connect()
            colector.collect_objects()
            colector.close()
            
            self.log_message("Coleta concluída com sucesso!", "SUCCESS")
            messagebox.showinfo("Sucesso", "Coleta concluída com sucesso!")
            
        except Exception as e:
            self.log_message(f"Erro durante a coleta: {str(e)}", "ERROR")
            messagebox.showerror("Erro", f"Erro durante a coleta: {str(e)}")
        finally:
            self.progress_var.set(0)
            self.progress_label.configure(text="0%")

    def extract_specific_object(self):
        object_name = self.object_name_var.get().strip()
        if not object_name:
            self.log_message("Informe o nome do objeto para extrair.", "ERROR")
            messagebox.showerror("Erro", "Informe o nome do objeto para extrair.")
            return
        # Limpar log
        self.log_text.delete(1.0, tk.END)
        thread = threading.Thread(target=self._extract_specific_object_thread, args=(object_name,))
        thread.daemon = True
        thread.start()

    def _extract_specific_object_thread(self, object_name):
        try:
            class GUILogHandler(logging.Handler):
                def __init__(self, text_widget, log_message_func):
                    logging.Handler.__init__(self)
                    self.text_widget = text_widget
                    self.log_message_func = log_message_func
                def emit(self, record):
                    msg = self.format(record)
                    def append():
                        level = record.levelname
                        self.log_message_func(msg, level)
                    self.text_widget.after(0, append)
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            gui_handler = GUILogHandler(self.log_text, self.log_message)
            gui_handler.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(gui_handler)
            colector = SchemaColector()
            colector.output_dir = self.output_dir_var.get()
            os.environ['DB_USER'] = self.username_var.get()
            os.environ['DB_PASSWORD'] = self.password_var.get()
            os.environ['DB_DSN'] = self.dsn_var.get()
            os.environ['DB_SCHEMA'] = self.schema_var.get()
            colector.connect()
            # Buscar tipo do objeto
            object_type = self._get_object_type(colector, object_name)
            if not object_type:
                self.log_message(f"Objeto '{object_name}' não encontrado no schema.", "ERROR")
                messagebox.showerror("Erro", f"Objeto '{object_name}' não encontrado no schema.")
                colector.close()
                return
            definition = colector.get_object_definition(object_name, object_type)
            if definition:
                # Remover 'EDITIONABLE'
                definition = re.sub(r'EDITIONABLE\s*', '', definition, flags=re.IGNORECASE)
                schema = os.getenv('DB_SCHEMA')
                obj_name_clean = object_name.lower()
                object_type_clean = object_type.lower()
                # Remove o owner do nome do objeto no DDL (ex: "OWNER"."OBJETO" -> "objeto")
                pattern = rf'"{schema}"\."{object_name}"'
                definition = re.sub(pattern, obj_name_clean, definition, flags=re.IGNORECASE)
                # Remove o owner de todas as referências do tipo "OWNER"."ALGUMA_COISA"
                pattern_all = rf'"{schema}"\."([^"]+)"'
                definition = re.sub(pattern_all, lambda m: m.group(1).lower(), definition, flags=re.IGNORECASE)
                # Remove cláusulas OWNER (ex: OWNER TO ...)
                definition = re.sub(r'OWNER TO \\"?[^;\n]+', '', definition, flags=re.IGNORECASE)
                # Remove aspas duplas dos nomes dos objetos
                definition = re.sub(r'"([^"]+)"', lambda m: m.group(1).lower(), definition)
                # Salvar tudo em lowercase
                definition = definition.lower()
                dir_path = os.path.join(colector.output_dir, object_type_clean)
                os.makedirs(dir_path, exist_ok=True)
                file_path = os.path.join(dir_path, f"{obj_name_clean}.sql")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(definition)
                self.log_message(f"Objeto '{object_name}' ({object_type}) extraído com sucesso!", "SUCCESS")
                messagebox.showinfo("Sucesso", f"Objeto '{object_name}' ({object_type}) extraído com sucesso!")
            else:
                self.log_message(f"Não foi possível extrair o objeto '{object_name}'.", "ERROR")
                messagebox.showerror("Erro", f"Não foi possível extrair o objeto '{object_name}'.")
            colector.close()
        except Exception as e:
            self.log_message(f"Erro ao extrair objeto: {str(e)}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao extrair objeto: {str(e)}")

    def _get_object_type(self, colector, object_name):
        try:
            query = """
            SELECT OBJECT_TYPE FROM ALL_OBJECTS WHERE OWNER = :1 AND OBJECT_NAME = :2
            """
            colector.cursor.execute(query, (os.getenv('DB_SCHEMA'), object_name))
            result = colector.cursor.fetchone()
            if result:
                return result[0]
            return None
        except Exception:
            return None

def main():
    root = tk.Tk()
    app = SchemaColectorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 