import numpy as np

class DataProcessor:
       
    def validate_entry(self, inp):
        try:
            return float(inp)
        except ValueError:
            return None
    
    def UpdateCanvas(self):
        
        self.ax_color.clear()
        self.ax_integrated.clear()
        
        self.FalseColorPlot()
        self.CalculateIntegral()
        
        self.ax_color.set_xlabel('Wavedata (arb. u.)')
        self.ax_color.set_ylabel('Custom variable (arb. u.)')
        
        self.ax_integrated.set_xlabel('Custom variable (arb. u.)')
        self.ax_integrated.set_ylabel('Integrated counts (arb. u.)')
        
        # Redesenha o grafico
        self.canvas.draw()
    
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
        
        if len(self.tags) == 0:
            self.tags = None
            
        self.UpdateCanvas()
        
        self.RenderDataFrame()
            
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
        
        self.UpdateCanvas()
        
        self.RenderDataFrame()