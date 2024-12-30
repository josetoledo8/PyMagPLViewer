import struct
import numpy as np
import plotly.graph_objects as go
import math
import os
import pandas as pd

class read_spe:
    
    def __init__(self, filename):
        self._filename = filename
        
    
    def get_from_bytes(self, byte_data, format, offset):
        calcsize = struct.calcsize(format)
        return struct.unpack(format, byte_data[offset:offset+calcsize])[0]


    def getDataInformation(self):
        file = open(self._filename, "rb")
        bytes = file.read()

        SPEVersion = round(self.get_from_bytes(bytes, "f", 1992), 1)

        datatype = self.get_from_bytes(bytes, "h", 108)
        frame_width = self.get_from_bytes(bytes, "H", 42)
        frame_height = self.get_from_bytes(bytes, "H", 656)
        num_frames = self.get_from_bytes(bytes, "i", 1446)
        to_np_type = [np.float32, np.int32, np.int16, np.uint16, None, np.float64, np.uint8, None, np.uint32]
        np_type = to_np_type[datatype]
        itemsize = np.dtype(np_type).itemsize
        XMLOffset = self.get_from_bytes(bytes, "64Q", 678)

        Count = frame_width * frame_height

        if SPEVersion < 3:
            
            Version = SPEVersion
            Frame = num_frames
            Width = frame_width
            Height = frame_height
            Laser = self.get_from_bytes(bytes, "d", 3311)
            LocalDate = self.get_from_bytes(bytes, "16s", 20)
            LocalDate = LocalDate.decode("utf-8", "ignore")
           
            LocalTime = self.get_from_bytes(bytes, "6s", 172)
            LocalTime = LocalTime.decode("utf-8", "ignore")
            Time = LocalTime[:2] + ":" + LocalTime[2:4] + ":" + LocalTime[4:]
            UTCTime = self.get_from_bytes(bytes, "6s", 179)
            UTCTime = UTCTime.decode("utf-8", "ignore")
            ExpTime = self.get_from_bytes(bytes, "f", 10)
            CWL = self.get_from_bytes(bytes, "f", 72)
            Grating = self.get_from_bytes(bytes, "32f", 650)
            BG = self.get_from_bytes(bytes, "i", 150)
            XStartNM = self.get_from_bytes(bytes, "d", 3183)
            XStopNM = self.get_from_bytes(bytes, "d", 3199)

            PXSize = (XStopNM-XStartNM)/(Count-1)
            Wavedata = []
            WavedataRound = []
            j = 0
            while j < Count:
                val = XStartNM + (j * PXSize)
                Wavedata.append(val)
                WavedataRound.append(round(val, 2))
                j += 1

        self.SPE_Infos = f'''
Loaded file: {self._filename.split('//')[-1].split('.SPE')[0]}
SPE Version: {Version}
Laser wavelength: {Laser}
Exposure time (s): {ExpTime}
Grating: {Grating} l/mm
Background correction: {False if BG == 0 else True}
'''
        return np_type, itemsize, Count, Version, Frame, Width, Height, Laser, ExpTime, CWL, Grating, BG, Wavedata, WavedataRound

    def getSpectra(self):

        np_type, itemsize, Count, Version, Frame, Width, Height, Laser, ExpTime, CWL, Grating, BG, Wavedata, WavedataRound = self.getDataInformation()

        Frame = int(Frame)
        Itemsize = int(itemsize)
        Count = int(Count)

        spectra = []
        spectra.append(WavedataRound)

        with open(self._filename, 'rb') as file:
            bytes = file.read()

            Px = int(math.sqrt(int(Frame)))
            for i in range(0, Frame):
                offset = 4100 + i*Count*Itemsize
                data = np.frombuffer(bytes, dtype=np_type, count=Count, offset=offset)

                spectra.append(data)

        self.spectra_df = pd.DataFrame(spectra).transpose()
        self.spectra_df.columns = ['wavedata'] + [f'spec_{i}' for i in range(1, len(self.spectra_df.columns), 1)]
        
        self._start = min(self.spectra_df['wavedata'])
        self._final = max(self.spectra_df['wavedata'])
        
        self._start_reset = round(min(self.spectra_df['wavedata']), 2)
        self._final_reset = round(max(self.spectra_df['wavedata']), 2)
        self.spectra_df_reset = self.spectra_df.copy()
        
        return self.spectra_df
       

    def getMappingCoordinates(self):

        num_scanned_lines = int(np.sqrt(len(self.spectra_df.columns) - 1)) # The 1 subtraction is to throw away the Energy/Wavelength column
        
        self.x_line = [i for i in range(num_scanned_lines)]
        self.y_line = self.x_line
        
        pixel_coordinates = []
        for x in self.x_line:
            for y in self.y_line:
                pixel_coordinates.append(f'x={x} y={y}')

        self.spectra_df.columns = ['wavedata'] + pixel_coordinates