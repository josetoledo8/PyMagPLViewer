import numpy as np
import mplcyberpunk

class DataVisualizer:
    
    def PlotData(self):
        
        self.ImportFiles()
                
        self.LineGraph()
        
        self.FalseColorPlot()
        
        self.CalculateIntegral()
        
        self.canvas.draw()
        
    def LineGraph(self):
                
        xdata = self.df_full.iloc[:, 0]
        
        for col in self.df_full.columns[1:]:
            self.ax_line.plot(xdata, self.df_full[col])
            
                
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
            cmap='coolwarm',
            vmin=self.y_min or np.min(z),
            vmax=self.y_max or np.max(z)
        )

        self.ax_color.set_xlim(self.x_min, self.x_max)
        
    def CalculateIntegral(self):

        integrals = []

        x_min = self.x_min if self.x_min is not None else self.df_full[self.df_full.columns[0]].min(
        )
        x_max = self.x_max if self.x_max is not None else self.df_full[self.df_full.columns[0]].max(
        )

        filtered_df = self.df_full[
            (self.df_full[self.df_full.columns[0]] >= x_min) &
            (self.df_full[self.df_full.columns[0]] <= x_max)
        ]

        x = filtered_df[filtered_df.columns[0]].values
        
        for col in filtered_df.columns[1:]:
            y = filtered_df[col].values
            integral = np.trapz(np.abs(y), x=x)
            
            integrals.append(integral)

        vertical_axis = self.tags or filtered_df.columns[1:]
                
        self.ax_integrated.plot(vertical_axis, integrals, linestyle='dashed', marker = 'o')
        
        mplcyberpunk.make_lines_glow(self.ax_integrated)
        mplcyberpunk.add_gradient_fill(self.ax_integrated, alpha_gradientglow=0.5)