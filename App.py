import customtkinter as ctk
import plotly.graph_objects as go
import os
import pandas as pd
import tkinterhtml as tk_html

from io import StringIO
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from glob import glob


class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.geometry("1280x768")
        self.title("Main App Progress")
        
        # Configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Configure a Frame to group buttons in the same grid cell
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0)
        
        self.btn1 = ctk.CTkButton(self.frame, text='Import files', command=self.ImportFiles)
        self.btn1.grid(row=0, column=0, pady=5, padx=5)
        
        self.btn2 = ctk.CTkButton(self.frame, text='View data', command=self.PlotData)
        self.btn2.grid(row=1, column=0, pady=5, padx=5)
        
        self.btn3 = ctk.CTkButton(self.frame, text='Export data', command=self.ExportData)
        self.btn3.grid(row=2, column=0, pady=5, padx=5)
        
        # Create an HtmlFrame for rendering Plotly graphs
        self.plot_frame = tk_html.HtmlFrame(self, horizontal_scrollbar="auto")
        self.plot_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
    
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
        # Conta qtt de arquivos
        # Maior que 1 gera color code e gráficos
        # Igual a 1 só gráficos
        fig = go.Figure()
        
        for file in self.files:
            filepath = os.path.realpath(file) 
            df = pd.read_csv(filepath, sep=r'\s+', names=['x', 'y'])
            
            for col in df.columns:
                df[col] = [float(value) for value in df[col]]
                
                fig.add_trace(
                    go.Scatter(
                        x=df['x'],
                        y=df['y']
                    )
                )
        
        fig.update_layout(showlegend=False)
        
        # Gera o HTML da figura
        html_buffer = StringIO()
        fig.write_html(html_buffer, full_html=False)  # Retorna apenas o corpo do HTML, sem a tag <html>
        html_content = html_buffer.getvalue()

        # Atualiza o conteúdo do HtmlFrame existente
        self.plot_frame.set_content(html_content)
    
    def ExportData(self):
        print('click')


app = App()
app.mainloop()
