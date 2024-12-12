import customtkinter as ctk
import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog as fd

sns.set_theme()

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.geometry("1280x768")
        self.title("Main App Progress")
        
        # Configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Configure each frame for each widget group
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0)

        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row = 0, column = 1, rowspan = 2)
        
        # Configure widgets
        self.btn1 = ctk.CTkButton(self.main_frame, text='Import files', command=self.ImportFiles)
        self.btn1.grid(row=0, column=0, pady=5, padx=5)
        
        self.btn2 = ctk.CTkButton(self.main_frame, text='View data', command=self.PlotData)
        self.btn2.grid(row=1, column=0, pady=5, padx=5)
        
        self.btn3 = ctk.CTkButton(self.main_frame, text='Export data', command=self.ExportData)
        self.btn3.grid(row=2, column=0, pady=5, padx=5)
        
        # Import files placeholder
        self.files = []
        
        # Default axes titles
        self._xlabel = "Wavedata (arb. u.)"
        self._ylabel = "CCD Counts (arb. u.)"

    @property
    def XAxis_Title(self):
        """Obtém o título do eixo X."""
        return self._xlabel

    @XAxis_Title.setter
    def XAxis_Title(self, value):
        """Define o título do eixo X."""
        self._xlabel = value

    @property
    def YAxis_Title(self):
        """Obtém o título do eixo Y."""
        return self._ylabel

    @YAxis_Title.setter
    def YAxis_Title(self, value):
        """Define o título do eixo Y."""
        self._ylabel = value

    def ImportFiles(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        self.files = fd.askopenfilenames(
            title='Open a file',
            filetypes=filetypes
        )

    def PlotData(self):
               
        if not self.files:
            self.ImportFiles()

        # Cria a figura do Matplotlib
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax_line = self.fig.add_subplot(111)  # Subplot para o gráfico de linha

        self.df_full = pd.DataFrame({})

        for file in self.files:
            filepath = os.path.realpath(file)

            # Lê o arquivo e aplica conversão para números
            df = pd.read_csv(filepath, sep=r'\s+', names=['x', 'y'])
            df = df.apply(pd.to_numeric, errors='coerce').dropna()

            # Adiciona dados ao gráfico de linha
            self.ax_line.plot(df['x'], df['y'])

            # Concatena dados no DataFrame completo
            self.df_full = pd.concat([self.df_full, df], axis = 1, ignore_index=True)
        
        
        # Configurações do gráfico de linha
        self.ax_line.set_xlabel(self.XAxis_Title)
        self.ax_line.set_ylabel(self.YAxis_Title)
        
        # Ajusta o layout e adiciona a figura ao Tkinter
        self.fig.tight_layout()

        # Limpa o antigo gráfico antes de desenhar o novo
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)
        
        # Cria um mini-frame para agrupar os botões de crop
        crop_box = ctk.CTkFrame(self.plot_frame)
        crop_box.grid(row=1)
        
        x_crop_label = ctk.CTkLabel(crop_box, text = 'x range',fg_color="transparent")
        x_crop_label.grid(row=0, column = 0, columnspan = 2)

        self.min_x_entry = ctk.CTkEntry(crop_box, placeholder_text="Min x")
        self.min_x_entry.grid(row=1,column = 0)
        
        self.max_x_entry = ctk.CTkEntry(crop_box, placeholder_text="Max x")
        self.max_x_entry.grid(row=1,column = 1)
        
        self.y_crop_label = ctk.CTkLabel(crop_box, text = 'y range',fg_color="transparent")
        self.y_crop_label.grid(row=0, column = 2, columnspan = 2)

        self.min_y_entry = ctk.CTkEntry(crop_box, placeholder_text="Min y")
        self.min_y_entry.grid(row=1,column = 2)
        
        self.max_y_entry = ctk.CTkEntry(crop_box, placeholder_text="Max y")
        self.max_y_entry.grid(row=1,column = 3)
        
        crop_btn = ctk.CTkButton(master = crop_box, text="Crop graph", command=self.Crop)
        crop_btn.grid(row=2, columnspan = 4)
    
    def Crop(self):
        
        def validate_entry(inp):
            try:
                float(inp)
            except:
                return None
            return float(inp)
        
        restart_x = self.df_full.iloc[:,0].values
        restart_y = self.df_full.iloc[:,1:]
        
        self.x_min = validate_entry(self.min_x_entry.get()) or min(restart_x)
        self.x_max = validate_entry(self.max_x_entry.get()) or max(restart_x)
        self.y_min = validate_entry(self.min_y_entry.get()) or min(restart_y.min())
        self.y_max = validate_entry(self.max_y_entry.get()) or max(restart_y.max())

        # Atualiza os limites dos eixos
        self.ax_line.set_xlim(self.x_min, self.x_max)
        self.ax_line.set_ylim(self.y_min, self.y_max)

        # Redesenha o gráfico
        self.canvas.draw()

    def ExportData(self):
        return None

app = App()
app.mainloop()
