import numpy as np
import torch
from torch.utils.data import Dataset
import matplotlib.pyplot as plt

class Sample_1(Dataset):
    def __init__(self, N, r, noise):
        self.N = 2*N
        bl_x1 = np.random.normal(0, noise*r/4, N)
        bl_x2 = np.random.normal(0, noise*r/4, N)
        bl = np.hstack((bl_x1.reshape(N,1), bl_x2.reshape(N,1)))
        
        t = np.random.uniform(0, 2*np.pi, N)
        r_x1 = r * np.cos(t) + np.random.normal(0, noise*r/10, N)
        r_x2 = r * np.sin(t) + np.random.normal(0, noise*r/10, N)
        red = np.hstack((r_x1.reshape(N,1), r_x2.reshape(N,1)))
        
        self.x = torch.from_numpy(np.vstack((bl, red)))
        bl_y = np.ones(shape=(N,1))
        r_y = np.zeros(shape=(N,1))  
        self.y = torch.from_numpy(np.vstack((bl_y, r_y)))
    
    def __len__(self):
        return self.N
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]
    
    def __getall__(self):
        return self.x, self.y
    
class Sample_2(Dataset):
    def __init__(self, N, side, noise):
        self.N = 2*N
        sigm = noise*side / 25
        
        bl_x1 = np.random.uniform(0, side, N) + np.random.normal(0, sigm, N)
        bl_x2 = np.random.uniform(0, side, N) + np.random.normal(0, sigm, N)
        bl_x1[:int(N/2)] = -bl_x1[:int(N/2)]
        bl_x2[:int(N/2)] = -bl_x2[:int(N/2)]
        bl = np.hstack((bl_x1.reshape(N,1), bl_x2.reshape(N,1)))
        
        t = np.random.uniform(0, 2*np.pi, N)
        r_x1 = np.random.uniform(0, side, N) + np.random.normal(0, sigm, N)
        r_x2 = np.random.uniform(0, side, N) + np.random.normal(0, sigm, N)
        r_x1[:int(N/2)] = -r_x1[:int(N/2)]
        r_x2[int(N/2):] = -r_x2[int(N/2):]
        red = np.hstack((r_x1.reshape(N,1), r_x2.reshape(N,1)))
        
        self.x = torch.from_numpy(np.vstack((bl, red)))
        bl_y = np.ones(shape=(N,1))
        r_y = np.zeros(shape=(N,1))  
        self.y = torch.from_numpy(np.vstack((bl_y, r_y)))
    
    def __len__(self):
        return self.N
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]
    
    def __getall__(self):
        return self.x, self.y
    
class Sample_3(Dataset):
    def __init__(self, N, center, noise):
        self.N = 2*N
        sigm = noise * center / 1.5 
        
        bl_x1 = np.random.normal(center, sigm, N)
        bl_x2 = np.random.normal(center, sigm, N)
        bl = np.hstack((bl_x1.reshape(N,1), bl_x2.reshape(N,1)))
        
        t = np.random.uniform(0, 2*np.pi, N)
        r_x1 = np.random.normal(-center, sigm, N)
        r_x2 = np.random.normal(-center, sigm, N)
        red = np.hstack((r_x1.reshape(N,1), r_x2.reshape(N,1)))
        
        self.x = torch.from_numpy(np.vstack((bl, red)))
        bl_y = np.ones(shape=(N,1))
        r_y = np.zeros(shape=(N,1))  
        self.y = torch.from_numpy(np.vstack((bl_y, r_y)))
    
    def __len__(self):
        return self.N
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]
    
    def __getall__(self):
        return self.x, self.y
    
class Sample_4(Dataset):
    def __init__(self, N, spiral_len, noise):
        self.N = 2*N
        t = np.random.uniform(0, spiral_len, N)
        sigm = noise * 0.3
        
        bl_x1 = t * np.cos(t) + np.random.uniform(-sigm, sigm, N)
        bl_x2 = t * np.sin(t) + np.random.uniform(-sigm, sigm, N)
        bl = np.hstack((bl_x1.reshape(N,1), bl_x2.reshape(N,1)))
        
        r_x1 = t * -np.cos(t) + np.random.uniform(-sigm, sigm, N)
        r_x2 = t * -np.sin(t) + np.random.uniform(-sigm, sigm, N)
        red = np.hstack((r_x1.reshape(N,1), r_x2.reshape(N,1)))
        
        self.x = torch.from_numpy(np.vstack((bl, red)))
        bl_y = np.ones(shape=(N,1))
        r_y = np.zeros(shape=(N,1))  
        self.y = torch.from_numpy(np.vstack((bl_y, r_y)))
    
    def __len__(self):
        return self.N
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]
    
    def __getall__(self):
        return self.x, self.y
    
def draw_sample(XY):
    with torch.no_grad():
        X, Y = XY.__getall__()
        x_min, x_max = torch.min(X[:,0]), torch.max(X[:,0])
        y_min, y_max = torch.min(X[:,1]), torch.max(X[:,1])
        plt.ylim(1.2*y_min, 1.2*y_max)
        plt.scatter(X.numpy()[:,0], X.numpy()[:,1], c=Y.numpy())