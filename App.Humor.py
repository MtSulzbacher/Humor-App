import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Usa o diretório do script

    return os.path.join(base_path, relative_path)

# Caminho para a imagem usando a função resource_path
img_path = resource_path("images/angry.png")


# Conteúdo de analysis.py
def generate_report(period='diário'):
    db_path = resource_path('mood_tracker.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verifica se a tabela existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mood_log';")
    if not cursor.fetchone():
        print("A tabela 'mood_log' não existe. Por favor, registre algum humor primeiro.")
        return
    
    df = pd.read_sql_query("SELECT * FROM mood_log", conn)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    if period == 'diário':
        df_grouped = df.groupby(['date', 'mood']).size().unstack(fill_value=0)
    elif period == 'semanal':
        df['week'] = df['timestamp'].dt.isocalendar().week
        df_grouped = df.groupby(['week', 'mood']).size().unstack(fill_value=0)
    elif period == 'mensal':
        df['month'] = df['timestamp'].dt.month
        df_grouped = df.groupby(['month', 'mood']).size().unstack(fill_value=0)
    else:
        raise ValueError(f"Período inválido: {period}")

    if df_grouped.empty:
        print("Não há dados suficientes para gerar o relatório.")
        return

    df_grouped = df_grouped.reset_index().melt(id_vars='date' if period == 'diário' else ('week' if period == 'semanal' else 'month'), 
        var_name='Humor', 
        value_name='Entradas de Humor')

    # Mapeamento dos nomes dos humores para português
    mood_mapping = {
        'angry': 'Bravo',
        'cry': 'Triste',
        'neutral': 'Neutro',
        'happy': 'Alegre',
        'very_happy': 'Feliz'
    }
    df_grouped['Humor'] = df_grouped['Humor'].map(mood_mapping)

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # Paleta de cores baseada na imagem fornecida
    palette = {
        'Bravo': '#ff0000',  # Vermelho
        'Triste': '#ff7f00',  # Laranja
        'Neutro': '#ffff00',  # Amarelo
        'Alegre': '#7fff00',  # Verde claro
        'Feliz': '#00ff00'  # Verde
    }

    ax = sns.barplot(data=df_grouped, x='date' if period == 'diário' else ('week' if period == 'semanal' else 'month'), 
            y='Entradas de Humor', hue='Humor', palette=palette)

    plt.title(f'Relatório de Humor ({period.capitalize()})')
    plt.xlabel('Período')
    plt.ylabel('Entradas de Humor')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Conteúdo de database.py
class Database:
    def __init__(self, db_name='mood_tracker.db'):
        self.db_name = resource_path(db_name)
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def insert_mood(self, mood):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO mood_log (mood) VALUES (?)', (mood,))
        self.conn.commit()

    def fetch_moods(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM mood_log')
        rows = cursor.fetchall()
        return rows

    def reset_data(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM mood_log')
        self.conn.commit()

# Conteúdo de mood_tracker.py
class MoodTracker:
    def __init__(self):
        self.database = Database()

    def log_mood(self, mood):
        self.database.insert_mood(mood)

    def generate_report(self, period='diário'):
        generate_report(period)

    def reset_data(self):
        self.database.reset_data()

# Conteúdo de mood_ui.py
class MoodTrackerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove a barra de título
        self.root.configure(bg='white')  # Fundo branco por padrão
        self.current_theme = 'white'

        self.mood_tracker = MoodTracker()

        self.offset_x = 0
        self.offset_y = 0
        self.root.bind("<Button-1>", self.click_win)
        self.root.bind("<B1-Motion>", self.drag_win)

        self.create_widgets()

        # Ajuste do tamanho da janela para ficar rente aos emojis e botões
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.root.geometry(f"{width}x{height}")

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg=self.current_theme)
        self.frame.pack(pady=10)

        self.moods = ['angry', 'cry', 'neutral', 'happy', 'very_happy']
        self.mood_buttons = []
        for mood in self.moods:
            img_path = resource_path(f"{mood}.png")
            img = Image.open(img_path)
            img = img.resize((30, 30), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            button = tk.Button(self.frame, image=photo, command=lambda m=mood: self.log_and_update(m), borderwidth=0, bg=self.current_theme, activebackground=self.current_theme)
            button.image = photo  # Keep a reference to avoid garbage collection
            button.pack(side=tk.LEFT, padx=2)
            self.mood_buttons.append(button)

        self.button_frame = tk.Frame(self.root, bg=self.current_theme)
        self.button_frame.pack(pady=5)

        self.theme_button = tk.Button(self.button_frame, text="Tema", command=self.toggle_theme, borderwidth=0, bg=self.current_theme, fg='black', activebackground=self.current_theme)
        self.theme_button.pack(side=tk.LEFT, padx=5)

        self.report_button = tk.Button(self.button_frame, text="Relatório", command=self.open_report_window, borderwidth=0, bg=self.current_theme, fg='black', activebackground=self.current_theme)
        self.report_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Sair", command=self.root.destroy, borderwidth=0, bg=self.current_theme, fg='black', activebackground=self.current_theme)
        self.exit_button.pack(side=tk.LEFT, padx=5)

    def toggle_theme(self):
        if self.current_theme == 'white':
            self.current_theme = 'black'
            fg_color = 'white'
        else:
            self.current_theme = 'white'
            fg_color = 'black'

        self.root.configure(bg=self.current_theme)
        self.frame.configure(bg=self.current_theme)
        self.button_frame.configure(bg=self.current_theme)
        
        for button in self.mood_buttons:
            button.configure(bg=self.current_theme, activebackground=self.current_theme)
        
        self.theme_button.configure(bg=self.current_theme, fg=fg_color, activebackground=self.current_theme)
        self.report_button.configure(bg=self.current_theme, fg=fg_color, activebackground=self.current_theme)
        self.exit_button.configure(bg=self.current_theme, fg=fg_color, activebackground=self.current_theme)

    def log_and_update(self, mood):
        self.mood_tracker.log_mood(mood)

    def open_report_window(self):
        self.report_window = tk.Toplevel(self.root)
        self.report_window.title("Relatório de Humor")
        self.report_window.configure(bg='white')  # Sempre branco
        self.report_window.geometry("200x150")  # Tamanho ajustado

        tk.Label(self.report_window, text="Selecionar Período:", bg='white').pack(pady=5)
        self.period_var = tk.StringVar(value='diário')
        period_options = ['diário', 'semanal', 'mensal']
        self.period_menu = ttk.Combobox(self.report_window, textvariable=self.period_var, values=period_options, state='readonly')
        self.period_menu.pack(pady=5)

        self.generate_button = tk.Button(self.report_window, text="Gerar Relatório", command=self.generate_report, borderwidth=0, bg='white')
        self.generate_button.pack(pady=5)

        self.reset_button = tk.Button(self.report_window, text="Resetar Dados", command=self.reset_data, borderwidth=0, bg='white')
        self.reset_button.pack(pady=5)

    def generate_report(self):
        period = self.period_var.get()
        self.mood_tracker.generate_report(period)

    def reset_data(self):
        self.mood_tracker.reset_data()

    def click_win(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def drag_win(self, event):
        x = self.root.winfo_pointerx() - self.offset_x
        y = self.root.winfo_pointery() - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def run(self):
        self.root.mainloop()

# Conteúdo de main.py ajustado
def main():
    app = MoodTrackerUI()
    app.run()

if __name__ == "__main__":
    main()
