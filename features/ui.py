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
            row=0, column=0, padx=2, pady=2, sticky = 'n')

        # Distribui uniformemente os miniframes de importacao e exportacao
        self.main_frame.grid_columnconfigure((0,1), weight=1)

        self.MiniFrameImportOptions()
        self.MiniFrameExportOptions()

    def MiniFrameImportOptions(self):

        # Set the frame for import options
        import_frame = ctk.CTkFrame(self.main_frame)
        import_frame.grid(
            row=0, column=0, columnspan = 1, pady=5, padx=5, sticky ='we')

        # Colunas 0 e 1 com mesmo peso
        import_frame.grid_columnconfigure(0, weight=1)

        # Import button
        ctk.CTkButton(
            import_frame, text='Import data', command=self.PlotData).grid(
                row=0, column=0, columnspan = 1, pady=5, padx=5, sticky ='NSWE')

        # Set column separator elements
        self.import_separator = ctk.StringVar(value="Tab/space")
        ctk.CTkLabel(
            import_frame, text='Column separator', 
            fg_color="transparent"
        ).grid(
            row=1, column=0, columnspan = 1, pady=0, padx=5, sticky = 'w')

        ctk.CTkComboBox(
            import_frame, values=['Tab/space', ',', ';'], 
            variable=self.import_separator
        ).grid(
            row=2, column=0, columnspan = 1, pady=0, padx=5, sticky = 'we')

    def MiniFrameExportOptions(self):

        export_frame = ctk.CTkFrame(self.main_frame)
        export_frame.grid(row=0, column = 1, columnspan=1, pady=5, padx=5, stick='we')
        
        export_frame.columnconfigure(0, weight=1)
                
        # Export button
        ctk.CTkButton(export_frame, text='Export data', command=self.ExportData).grid(
            row=0, column = 0, columnspan=1, pady=5, padx=5, sticky ='WE')

        # Set export image elements
        # Recebe self para ser acessado em ExportData
        self.export_image = ctk.StringVar(value="No")

        ctk.CTkLabel(
            export_frame, text='Export image', 
            fg_color="transparent"
        ).grid(
            row=1, column = 0, columnspan=1, pady=0, padx=5, sticky = 'w')

        ctk.CTkComboBox(
            export_frame, values=['No', 'Yes'], 
            variable=self.export_image
        ).grid(
            row=2, column = 0, columnspan=1, pady=0, padx=5, sticky = 'we')

    def FrameGraphs(self):

        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=1, padx=2, pady=2, stick='n')

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

        # Cria um container principal com um fundo distinto
        crop_container = ctk.CTkFrame(
            self.plot_frame, 
            corner_radius=10, 
            fg_color="transparent", 
            border_color="#565b5e", 
            border_width=2  # Define a largura da borda
        )
        crop_container.grid(row=1, pady=10, padx=10, sticky ='we')  # Define padding para destacar o bisel
        crop_container.grid_columnconfigure(0, weight=1)

        # Cria um mini-frame para agrupar os botões de crop dentro do container
        crop_box = ctk.CTkFrame(crop_container, fg_color="transparent")
        crop_box.grid(row=0, padx=10, pady=10, sticky ='we')

        crop_box.grid_columnconfigure((0, 1, 2, 3, 4, 5,6), weight=1)

        # Configura entries para cortar o eixo-x
        x_crop_label = ctk.CTkLabel(crop_box, text='X Range', fg_color="transparent")
        x_crop_label.grid(row=0, column=0, columnspan=2)

        self.min_x_entry = ctk.CTkEntry(crop_box, placeholder_text="Min x")
        self.min_x_entry.grid(row=1, column=0)

        self.max_x_entry = ctk.CTkEntry(crop_box, placeholder_text="Max x")
        self.max_x_entry.grid(row=1, column=1)

        # Espaçador entre X e CCD
        spacer = ctk.CTkLabel(crop_box, text='', fg_color="transparent")
        spacer.grid(row=1, column=2, padx=10)

        # Configura entries para cortar o eixo-y
        self.y_crop_label = ctk.CTkLabel(crop_box, text='CCD Counts Range', fg_color="transparent")
        self.y_crop_label.grid(row=0, column=3, columnspan=2)

        self.min_y_entry = ctk.CTkEntry(crop_box, placeholder_text="Min counts")
        self.min_y_entry.grid(row=1, column=3)

        self.max_y_entry = ctk.CTkEntry(crop_box, placeholder_text="Max counts")
        self.max_y_entry.grid(row=1, column=4)

        # Espaçador entre CCD e botao
        spacer = ctk.CTkLabel(crop_box, text='', fg_color="transparent")
        spacer.grid(row=1, column=5, padx=10)

        # Define o Crop Button
        crop_btn = ctk.CTkButton(
            master=crop_box, text="Update axes",
            corner_radius=5,
            command=self.Crop)
        crop_btn.grid(row=0, rowspan=2, column=6, padx=5, pady=5, sticky ='nswe')


    def FrameTags(self):
        
        self.tag_frame = ctk.CTkFrame(self.main_frame)
        self.tag_frame.grid(row=4, column=0, columnspan=4, sticky ='NSWE')

        ctk.CTkLabel(
            self.tag_frame, text='Custom variable (Field, Angle, Time, etc)', 
            fg_color="transparent"
        ).grid(
            row=0, pady=5, padx=5, 
            columnspan=3, sticky ='WE'
        )

        ctk.CTkLabel(
            self.tag_frame, text='Initial value', fg_color="transparent"
        ).grid(row=1, column=0, pady=5, padx=5)

        ctk.CTkLabel(
            self.tag_frame, text='Final value', fg_color="transparent"
        ).grid(row=1, column=1, pady=5, padx=5)

        ctk.CTkLabel(
            self.tag_frame, text='Step value', fg_color="transparent"
        ).grid(row=1, column=2, pady=5, padx=5)

        # Place entries using a loop
        self.init_entries = []
        self.final_entries = []
        self.step_entries = []

        # Garante que self.num_tags seja inicializado            
        self.num_tags = getattr(self, 'num_tags', 3)

        # Cria entradas dinamicamente
        for i in range(1, self.num_tags + 1):
            init_entry = ctk.CTkEntry(self.tag_frame)
            init_entry.grid(row=i + 1, column=0, padx=5, pady=5)
            self.init_entries.append(init_entry)

            final_entry = ctk.CTkEntry(self.tag_frame)
            final_entry.grid(row=i + 1, column=1, padx=5, pady=5)
            self.final_entries.append(final_entry)

            step_entry = ctk.CTkEntry(self.tag_frame)
            step_entry.grid(row=i + 1, column=2, padx=5, pady=5)
            self.step_entries.append(step_entry)

        # ComboBox para selecionar o número de tags
        num_tags_var = ctk.IntVar(value=self.num_tags)

        def update_num_tags(new_value):
            self.num_tags = int(new_value)
            self.FrameTags()  # Atualiza o frame com o novo número de tags
            self.FrameDataTable()

        ctk.CTkLabel(
            master=self.tag_frame,
            text='Custom variable intervals: ', 
            fg_color="transparent"
        ).grid(
            row=self.num_tags + 2, column = 0,  columnspan = 2, sticky = 'we', pady = 5
        )

        ctk.CTkComboBox(
            master=self.tag_frame,
            values=[str(i) for i in range(1, 11)],
            command=update_num_tags,
            variable=num_tags_var
        ).grid(row=self.num_tags + 2, column=2, pady=5)

        # Botão de confirmação
        tag_btn = ctk.CTkButton(
            master=self.tag_frame, text="Apply tags", command=self.ApplyTags)
        tag_btn.grid(row=self.num_tags + 3, columnspan=3, sticky='we', pady=5)

        # Atualiza o próximo índice vazio
        self.next_empty_row = self.num_tags + 4

    def FrameDataTable(self):
        # Criar um frame vazio para renderizar o DataFrame quando os dados forem importados
        self.table_frame = ctk.CTkFrame(self.tag_frame, fg_color="transparent")
        self.table_frame.grid(
            row=self.next_empty_row, 
            column=0, 
            columnspan=4, 
            sticky ='NWE',
            pady=5
        )
                
        try:
            self.RenderDataFrame()
        except:
            pass

    def RenderDataFrame(self):
        preview_rows = 5
        preview_cols = 11

        if self.x_max or self.x_min:
            df = self.df_full[self.df_full.iloc[:, 0].between(self.x_min, self.x_max)]
        else:
            df = self.df_full

        # Obter as primeiras e últimas linhas do DataFrame
        first_preview = df.iloc[0:preview_rows, 0:preview_cols]
        last_preview = df.iloc[-preview_rows:, 0:preview_cols]

        # Configurar os cabeçalhos
        if self.tags:
            columns = ['Wavedata'] + list(self.tags)[0:preview_cols-1]
        else:
            columns = self.df_full.columns[:preview_cols]

        first_preview.columns = columns
        last_preview.columns = columns

        # Limpar frame antes de renderizar nova tabela
        self.ClearFrame(self.table_frame)

        # Adicionar título acima da tabela
        title_label = ctk.CTkLabel(
            self.table_frame,
            text="Preview of imported data",
            font=("Arial", 12),
            fg_color="transparent",  # Fundo transparente
            text_color="white"       # Cor do texto
        )
        title_label.grid(row=0, column=0, columnspan=preview_cols, pady=(5, 2), sticky ="nsew")

        # Renderizar cabeçalhos com cor de fundo diferente
        for col_index, col_name in enumerate(columns):
            label = ctk.CTkLabel(
                self.table_frame, 
                text=col_name, 
                font=("Arial", 12), 
                fg_color="#565b5e",  # Cor de fundo do cabeçalho
                text_color="white",  # Cor do texto            
            )
            label.grid(row=1, column=col_index, padx=0, pady=8, sticky ="nsew")

        # Renderizar as primeiras linhas
        current_row = 2
        for row_index, row in enumerate(first_preview.values):
            for col_index, cell_value in enumerate(row):
                label = ctk.CTkLabel(
                    self.table_frame, 
                    text=str(cell_value), 
                    font=("Arial", 10)
                )
                label.grid(row=current_row, column=col_index, padx=1, pady=1, sticky ="nsew")
            current_row += 1

        # Adicionar reticências centralizadas
        for col_index in range(preview_cols):
            label = ctk.CTkLabel(
                self.table_frame, 
                text="..." if col_index == preview_cols // 2 else "",
                font=("Arial", 12, "italic")
            )
            label.grid(row=current_row, column=col_index, padx=1, pady=1, sticky ="nsew")
        current_row += 1

        # Renderizar as últimas linhas
        for row_index, row in enumerate(last_preview.values):
            for col_index, cell_value in enumerate(row):
                label = ctk.CTkLabel(
                    self.table_frame, 
                    text=str(cell_value), 
                    font=("Arial", 10)
                )
                label.grid(row=current_row, column=col_index, padx=1, pady=1, sticky ="nsew")
            current_row += 1

        # Ajustar proporção das colunas para preencher espaço dinamicamente
        for col_index in range(preview_cols):
            self.table_frame.grid_columnconfigure(col_index, weight=1)