import pandas as pd
import os
from pandastable import Table
from tkinter import filedialog as fd
from .utils.SPE_Loader import read_spe

class DataImporter:
    
    def SPEImport(self, file):
        spe = read_spe(file)
        df = spe.getSpectra()
        df.columns = ['x'] + [f'y{i}' for i in range(1, len(df.columns))]
        return df

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
        self.ax_integrated.set_ylabel('Integrated counts (normalized)')
        
        filetypes = (
            ('Text files', '*.txt'),
            ('Comma-separated values', '*.csv'),
            ('Dat files', '*.dat'),
            ('SPE files', '*.spe'),
            ('All files', '*.*')
        )

        self.files = fd.askopenfilenames(
            title='Open a file',
            filetypes=filetypes
        )
        
        self.df_full = pd.DataFrame({})

        # Loop para processar os arquivos
        for i, file in enumerate(self.files):
            filepath = os.path.realpath(file)
            extension = os.path.splitext(filepath)[1].lower()
            
            # Lê o arquivo e aplica conversão para números
            sep = self.import_separator.get()
            
            if extension.lower() == '.spe':
                df = self.SPEImport(filepath)
            else:
                df = pd.read_csv(
                    filepath, 
                    sep=r'\s+' if sep == 'Tab/space' else sep, 
                    header=None, 
                    engine='python')
            
            df = df.apply(pd.to_numeric, errors='coerce').dropna()

            df.columns = ['x'] + [f'y{i}' for i in range(1, len(df.columns))]

            if i == 0:
                # Primeira iteração: inicializa self.df_full
                self.df_full = df
            else:
                # Combina os DataFrames usando merge (full join)
                self.df_full = pd.merge(
                    left=self.df_full,
                    right=df,
                    on='x',
                    how='outer'
                )
            # Renomeia as colunas apos o merge para evitar colunas com nomes duplicados
            self.df_full.columns = ['x'] + [i for i in range(1, len(self.df_full.columns))]

        # Elimina as duplicatas da coluna 'x' geradas pelo processo de concatenação lateral
        self.df_full = self.df_full.T.drop_duplicates().T
        
        self.RenderDataFrame()
        
        
    def ExportData(self):
               
        if self.tags:
            self.df_full.columns = ['wavedata'] + self.tags
        else:
            self.df_full.columns = ['wavedata'] + [f'y{i}' for i in range(1, len(self.df_full.columns))]
        
        export_df = self.df_full[(self.df_full['wavedata'] >= self.x_min) & (self.df_full['wavedata'] <= self.x_max)]
            
        export_df.to_csv('exported_data.csv', sep = ' ', index=False)
        
        if self.export_image.get() == 'Yes':
            self.fig.savefig('exported_image.png', dpi = 150)