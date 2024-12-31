import customtkinter as ctk
import matplotlib.gridspec as gridspec
import seaborn as sns

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .data_import import DataImporter
from .data_visualizer import DataVisualizer
from .data_processing import DataProcessor

sns.set_theme(style="darkgrid")

class App(ctk.CTk, DataImporter, DataVisualizer, DataProcessor):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.geometry()
        self.title("Photoluminescence Data Visualizer")

        self.FrameMain()
        self.FrameGraphs()
        self.FrameCrop()
        self.FrameTags()
        self.FrameDataTable()
    
    def ClearFrame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def FrameMain(self):

        # Configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(
            row=0, column=0, padx=2, pady=2, stick='ns')

        # Distribui uniformemente os miniframes de importacao e exportacao
        self.main_frame.grid_columnconfigure((0,1), weight=1)

        self.MiniFrameImportOptions()
        self.MiniFrameExportOptions()

    def MiniFrameImportOptions(self):

        # Set the frame for import options
        import_frame = ctk.CTkFrame(self.main_frame)
        import_frame.grid(
            row=0, column=0, columnspan = 1, pady=5, padx=5, sticky='we')

        # Colunas 0 e 1 com mesmo peso
        import_frame.grid_columnconfigure(0, weight=1)

        # Import button
        ctk.CTkButton(
            import_frame, text='Import data', command=self.PlotData).grid(
                row=0, column=0, columnspan = 1, pady=5, padx=5, sticky='NSWE')

        # Set column separator elements
        self.import_separator = ctk.StringVar(value="Tab/space")
        ctk.CTkLabel(
            import_frame, text='Column separator', 
            fg_color="transparent"
        ).grid(
            row=1, column=0, columnspan = 1, pady=5, padx=5, sticky = 'w')

        ctk.CTkComboBox(
            import_frame, values=['Tab/space', ',', ';'], 
            variable=self.import_separator
        ).grid(
            row=2, column=0, columnspan = 1, pady=5, padx=5, sticky = 'we')

    def MiniFrameExportOptions(self):

        export_frame = ctk.CTkFrame(self.main_frame)
        export_frame.grid(row=0, column = 1, columnspan=1, pady=5, padx=5, stick='we')
        
        export_frame.columnconfigure(0, weight=1)
                
        # Export button
        ctk.CTkButton(export_frame, text='Export data', command=self.ExportData).grid(
            row=0, column = 0, columnspan=1, pady=5, padx=5, sticky='WE')

        # Set export image elements
        # Recebe self para ser acessado em ExportData
        self.export_image = ctk.StringVar(value="No")

        ctk.CTkLabel(
            export_frame, text='Export image', 
            fg_color="transparent"
        ).grid(
            row=1, column = 0, columnspan=1, pady=5, padx=5, sticky = 'w')

        ctk.CTkComboBox(
            export_frame, values=['No', 'Yes'], 
            variable=self.export_image
        ).grid(
            row=2, column = 0, columnspan=1, pady=5, padx=5, sticky = 'we')

    def FrameGraphs(self):

        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=1, padx=2, pady=2, stick='ns')

        # Cria a figura do Matplotlib
        self.fig = Figure(figsize=(10, 6), dpi=100)

        # Configurar o GridSpec
        # 2 linhas e 2 colunas, com ajuste de proporções
        gs = gridspec.GridSpec(2, 2, height_ratios=[1, 0.75])

        self.ax_line = self.fig.add_subplot(gs[0, 0])
        self.ax_color = self.fig.add_subplot(gs[0, 1])
        self.ax_integrated = self.fig.add_subplot(gs[1, :])

        # Nome dos eixos
        self.ax_line.set_xlabel('Wavedata (arb. u.)')
        self.ax_line.set_ylabel('CCD Counts (arb. u.)')

        self.ax_color.set_xlabel('Wavedata (arb. u.)')
        self.ax_color.set_ylabel('Custom variable (arb. u.)')

        self.ax_integrated.set_xlabel('Custom variable (arb. u.)')
        self.ax_integrated.set_ylabel('Integrated counts (normalized)')

        # Ajusta o layout e adiciona a figura ao Tkinter
        self.fig.tight_layout(pad=1.1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

    def FrameCrop(self):

        # Cria um mini-frame para agrupar os botões de crop
        crop_box = ctk.CTkFrame(self.plot_frame, fg_color="transparent")
        crop_box.grid(row=1, pady=5)

        # Configura entries para cortar o eixo-x
        x_crop_label = ctk.CTkLabel(
            crop_box, text='X Range', fg_color="transparent")
        x_crop_label.grid(row=0, column=0, columnspan=2)

        self.min_x_entry = ctk.CTkEntry(crop_box, placeholder_text="Min x")
        self.min_x_entry.grid(row=1, column=0)

        self.max_x_entry = ctk.CTkEntry(crop_box, placeholder_text="Max x")
        self.max_x_entry.grid(row=1, column=1)

        # Configura entries para cortar o eixo-y
        self.y_crop_label = ctk.CTkLabel(
            crop_box, text='CCD Counts Range', fg_color="transparent")
        self.y_crop_label.grid(row=0, column=2, columnspan=2)

        self.min_y_entry = ctk.CTkEntry(
            crop_box, placeholder_text="Min counts")
        self.min_y_entry.grid(row=1, column=2)

        self.max_y_entry = ctk.CTkEntry(
            crop_box, placeholder_text="Max counts")
        self.max_y_entry.grid(row=1, column=3)

        # Define o Crop Button
        crop_btn = ctk.CTkButton(
            master=crop_box, text="Crop graph", command=self.Crop)
        crop_btn.grid(row=2, columnspan=4, pady=5)

    def FrameTags(self):
        self.tag_frame = ctk.CTkFrame(self.main_frame)
        self.tag_frame.grid(row=4, column=0, columnspan=4, sticky='NSWE')

        self.tag_frame_label = ctk.CTkLabel(
            self.tag_frame, text='Custom variable (Field, Angle, Time, etc)', fg_color="transparent")
        self.tag_frame_label.grid(
            row=0, pady=5, padx=5, columnspan=3, sticky='WE')

        self.tag_frame_label1 = ctk.CTkLabel(
            self.tag_frame, text='Initial value', fg_color="transparent")
        self.tag_frame_label1.grid(row=1, column=0, pady=5, padx=5)

        self.tag_frame_label2 = ctk.CTkLabel(
            self.tag_frame, text='Final value', fg_color="transparent")
        self.tag_frame_label2.grid(row=1, column=1, pady=5, padx=5)

        self.tag_frame_label3 = ctk.CTkLabel(
            self.tag_frame, text='Step value', fg_color="transparent")
        self.tag_frame_label3.grid(row=1, column=2, pady=5, padx=5)

        # Place entries using a loop
        self.init_entries = []
        self.final_entries = []
        self.step_entries = []

        for i in range(1, 4):
            init_entry = ctk.CTkEntry(self.tag_frame)
            init_entry.grid(row=i + 1, column=0, padx=5, pady=5)
            self.init_entries.append(init_entry)

            final_entry = ctk.CTkEntry(self.tag_frame)
            final_entry.grid(row=i + 1, column=1, padx=5, pady=5)
            self.final_entries.append(final_entry)

            step_entry = ctk.CTkEntry(self.tag_frame)
            step_entry.grid(row=i + 1, column=2, padx=5, pady=5)
            self.step_entries.append(step_entry)

        # Set confirm button
        tag_btn = ctk.CTkButton(master=self.tag_frame,
                                text="Apply tags", command=self.ApplyTags)
        tag_btn.grid(row=i+2, columnspan=3)
        
        self.next_empty_row = i + 3

    def FrameDataTable(self):
        # Criar um frame vazio para renderizar o DataFrame quando os dados forem importados
        self.table_frame = ctk.CTkFrame(self.tag_frame)
        self.table_frame.grid(
            row=self.next_empty_row, 
            column=0, 
            columnspan=4, 
            sticky='NSWE',
            pady=5
        )
        
        # Configurar a grade para centralizar o rótulo
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Rótulo centralizado
        ctk.CTkLabel(
            self.table_frame, 
            text='Data preview', 
            fg_color="transparent", 
            anchor="center",  # Centraliza o texto no rótulo
            font=("Arial", 14, "bold")  # Ajuste opcional para destaque
        ).grid(
            column=0,
            row=0,
            columnspan=1,  # Garante que o rótulo ocupe o espaço da tabela
            sticky='WE',
            pady=10
        )
        
        try:
            self.RenderDataFrame()
        except:
            pass

        
    def RenderDataFrame(self):
                
        preview_rows = 5
        preview_cols = 10
        preview = self.df_full.iloc[0:preview_rows, 0:preview_cols]
        
        if self.tags:
            preview.columns = ['Wavedata'] + list(self.tags)[0:preview_cols-1]
        
        self.ClearFrame(self.table_frame)
        
        # Renderizar cabeçalhos com cor de fundo diferente
        for col_index, col_name in enumerate(preview.columns):
            label = ctk.CTkLabel(
                self.table_frame, 
                text=col_name, 
                font=("Arial", 12, "bold"), 
                fg_color="#46799c",  # Cor de fundo do cabeçalho
                text_color="white",  # Cor do texto
                corner_radius = 3
            )
            label.grid(row=1, column=col_index, padx=0, pady=5, sticky="nsew")
        
        # Renderizar linhas do DataFrame com bordas em torno das células
        for row_index, row in enumerate(preview.values):
            for col_index, cell_value in enumerate(row):
                label = ctk.CTkLabel(
                    self.table_frame, 
                    text=str(cell_value), 
                    font=("Arial", 10)
                )
                label.grid(row=row_index + 2, column=col_index, padx=1, pady=1, sticky="nsew")
        
        # Ajustar proporção das colunas para preencher espaço dinamicamente
        for col_index in range(preview.shape[1]):
            self.table_frame.grid_columnconfigure(col_index, weight=1)