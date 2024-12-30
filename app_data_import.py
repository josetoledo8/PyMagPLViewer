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
        self.ax_integrated.set_ylabel('Integrated counts (normalized)')
        
        filetypes = (
            ('Text files', '*.txt'),
            ('Comma-separated values', '*.csv'),
            ('Dat files', '*.dat'),
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

            # Lê o arquivo e aplica conversão para números
            sep = self.import_separator.get()
            
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
        
    def ExportData(self):
        
        if self.tags:
            self.df_full.columns = ['wave'] + self.tags
            
        self.df_full.to_csv('exported_data.csv', sep = ' ', index=False)
        
        if self.export_image.get() == 'Yes':
            self.fig.savefig('exported_image.png', dpi = 150)