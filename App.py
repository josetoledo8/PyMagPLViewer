import customtkinter as ctk
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog as fd

sns.set_theme()


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.geometry("1280x768")
        self.title("Main App Progress")

        # Configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Configure each frame for each widget group
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0)

        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=1)

        # Configure widgets
        self.btn2 = ctk.CTkButton(
            self.main_frame, text='Load data', command=self.PlotData)
        self.btn2.grid(row=0, column=0, pady=5, padx=5)

        self.btn3 = ctk.CTkButton(
            self.main_frame, text='Export data', command=self.ExportData)
        self.btn3.grid(row=3, column=0, pady=5, padx=5)

        # Import files placeholder
        self.files = []

        # Default axes titles
        self.x_label = "Wavedata (arb. u.)"
        self.y_label = "CCD Counts (arb. u.)"

        self.x_min = self.x_max = self.y_min = self.y_max = None

    def ImportFiles(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        self.files = fd.askopenfilenames(
            title='Open a file',
            filetypes=filetypes
        )

        self.GetSpectraTags()

    def PlotData(self):

        self.ImportFiles()

        # Reset any applied tags
        self.tags = None

        # Cria a figura do Matplotlib
        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.ax_line = self.fig.add_subplot(121)
        self.ax_color = self.fig.add_subplot(122)

        self.df_full = pd.DataFrame({})

        for file in self.files:
            filepath = os.path.realpath(file)

            # Lê o arquivo e aplica conversão para números
            df = pd.read_csv(filepath, sep=r'\s+', names=['x', 'y'])
            df = df.apply(pd.to_numeric, errors='coerce').dropna()

            # Adiciona dados ao gráfico de linha
            self.ax_line.plot(df['x'], df['y'])

            # Concatena dados no DataFrame completo
            self.df_full = pd.concat(
                [self.df_full, df], axis=1, ignore_index=True)

        # Elimina as duplicatas da coluna 'x' geradas pelo processo de concatenação lateral
        self.df_full = self.df_full.T.drop_duplicates().T

        # Gera o False Color Plot com os dados dos graficos de linha
        self.FalseColorPlot()

        # Configurações do gráfico de linha
        self.ax_line.set_xlabel(self.x_label)
        self.ax_line.set_ylabel(self.y_label)

        # Ajusta o layout e adiciona a figura ao Tkinter
        self.fig.tight_layout()

        # Limpa o antigo gráfico antes de desenhar o novo
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

        # Gera os widgets para manipular os eixos dos gráficos
        self.CropOptions()

    def CropOptions(self):

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

    def GetSpectraTags(self):
        self.tag_frame = ctk.CTkFrame(self.main_frame)
        self.tag_frame.grid(row=4, column=0)

        self.tag_frame_label = ctk.CTkLabel(
            self.tag_frame, text='Variable parameter (Field, Angle, Time, etc)', fg_color="transparent")
        self.tag_frame_label.grid(row=0, pady=5, padx=5, columnspan=3)

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

    def ApplyTags(self):

        # Placeholder for user's tag
        self.tags = []

        for i, f, s in zip(self.init_entries, self.final_entries, self.step_entries):

            i_val = i.get()
            f_val = f.get()
            s_val = s.get()

            entries = list(map(self.validate_entry, [i_val, f_val, s_val]))

            entries = list(filter(lambda value: value is not None, entries))

            if len(entries) == 3:
                self.tags.extend(np.arange(float(i_val), float(
                    f_val) + float(s_val), float(s_val)))

        if len(self.tags) > 1:
            self.FalseColorPlot()

            # Redesenha o grafico
            self.canvas.draw()

    def validate_entry(self, inp):
        try:
            return float(inp)
        except ValueError:
            return None

    def Crop(self):

        # Valida as entradas para os limites
        self.x_min = self.validate_entry(
            self.min_x_entry.get()) or min(self.df_full.iloc[:, 0])
        self.x_max = self.validate_entry(
            self.max_x_entry.get()) or max(self.df_full.iloc[:, 0])
        self.y_min = self.validate_entry(
            self.min_y_entry.get()) or self.df_full.iloc[:, 1:].values.min()
        self.y_max = self.validate_entry(
            self.max_y_entry.get()) or self.df_full.iloc[:, 1:].values.max()

        # Atualiza os limites do gráfico de linha
        self.ax_line.set_xlim(self.x_min, self.x_max)
        self.ax_line.set_ylim(self.y_min, self.y_max)

        self.FalseColorPlot()

        # Redesenha o gráfico
        self.canvas.draw()

    def FalseColorPlot(self):

        x = self.df_full.iloc[:, 0].values  # Wavedata
        y = self.tags or self.df_full.columns[1:].astype(
            float)  # Magnetic field
        z = self.df_full.iloc[:, 1:].values.T  # PL intensity

        X, Y = np.meshgrid(x, y)
        self.ax_color.pcolormesh(
            X,
            Y,
            z,
            cmap='viridis',
            vmin=self.y_min or np.min(z),
            vmax=self.y_max or np.max(z)
        )

        self.ax_color.set_xlim(self.x_min, self.x_max)

    def ExportData(self):
        return None


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
