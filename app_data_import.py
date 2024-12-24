import pandas as pd
import os
from tkinter import filedialog as fd

class DataImporter:

    def ImportFiles(self):
               
        self.tags = None
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        
        # Limpa os gráficos, caso um re-import seja feito
        self.ax_line.clear()
        self.ax_color.clear()
        self.ax_integrated.clear()
        
        # Nome dos eixos
        self.ax_line.set_xlabel('Wavedata (arb. u.)')
        self.ax_line.set_ylabel('CCD Counts (arb. u.)')
        
        self.ax_color.set_xlabel('Wavedata (arb. u.)')
        self.ax_color.set_ylabel('Custom variable (arb. u.)')
        
        self.ax_integrated.set_xlabel('Custom variable (arb. u.)')
        self.ax_integrated.set_ylabel('Integrated counts (arb. u.)')
        
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        self.files = fd.askopenfilenames(
            title='Open a file',
            filetypes=filetypes
        )
        
        self.df_full = pd.DataFrame({})

        for file in self.files:
            filepath = os.path.realpath(file)

            # Lê o arquivo e aplica conversão para números
            df = pd.read_csv(filepath, sep=r'\s+', names=['x', 'y'])
            df = df.apply(pd.to_numeric, errors='coerce').dropna()

            # Concatena dados no DataFrame completo
            self.df_full = pd.concat(
                [self.df_full, df], axis=1, ignore_index=True)

        # Elimina as duplicatas da coluna 'x' geradas pelo processo de concatenação lateral
        self.df_full = self.df_full.T.drop_duplicates().T
        
    def ExportData(self):
        pass