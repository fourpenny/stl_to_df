import numpy as np
import pandas as pd
import struct #for reading individual bytes

#Function below based on Alex Crosby's code to read an STL and calculate
#its volume (written in Python 2), found here: https://gist.github.com/acrosby/11180502

def stl_to_df(filename):
    with open(filename, 'rb') as f:
        f.read(80) #reads the header
        nn = f.read(4)
        Numtri = struct.unpack('I', nn)[0]
        record_dtype = np.dtype([
            ('Normals', np.float32, (3)),
            ('Vertex1', np.float32, (3)),
            ('Vertex2', np.float32, (3)),
            ('Vertex3', np.float32, (3)),
            ('atttr', '<i2', (1)),
            ])
        
        data = np.zeros((Numtri), dtype=record_dtype)
    
        for i in range(0, Numtri, 10):
            d = np.fromfile(f, dtype=record_dtype, count=10)
            data[i:i+len(d)] = d
        
        normals = data['Normals']
        v1 = data['Vertex1']
        v2 = data['Vertex2']
        v3 = data['Vertex3']
        points = np.hstack(((v1[:, np.newaxis, :]), (v2[:, np.newaxis, :]), (v3[:, np.newaxis, :]), (normals[:, np.newaxis, :])))
        
        points_df = pd.DataFrame.from_records(points)
        f.close()
        return points_df

new_df = stl_to_df('TOMCOIN.stl')
print(new_df.head())