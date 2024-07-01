import torch 
import torch.nn as nn
import numpy as np

class Perceptron(nn.Module):
    def __init__(self, input_size, output_size, epoch, batch_size, lr):
        super().__init__()
        self.epoch = epoch
        self.batch_size = batch_size
        self.lin = nn.Linear(input_size, output_size, dtype=torch.float64)
        self.optimizer = torch.optim.Adam(self.lin.parameters(), lr)
        self.loss_f = nn.MSELoss()
        
    def forward(self, X):
        pred = self.lin(X)
        return torch.softmax(pred, dim=1)
    
    def fit(self, X: torch.Tensor, Y: torch.Tensor):
        N = X.shape[0]
        X = X.type(torch.float64)
        
        for i in range(self.epoch):
            indices = torch.randperm(N)
            X, Y = X[indices], Y[indices]
            for j in range(0, N - self.batch_size, self.batch_size):
                X_batch, Y_batch = X[j:j+self.batch_size], Y[j:j+self.batch_size]
                self.lin.zero_grad()
                Y_pred = self(X_batch)
                loss = self.loss_f(Y_pred, Y_batch)
                loss.backward()
                self.optimizer.step()
                  
    def predict(self, X):
        X = X.type(torch.float64)
        pred = self(X)
        return torch.argmax(pred, dim=1)
    
    def get_w(self):
        return torch.cat([param.reshape((-1,)) for param in self.lin.parameters()])
    
class Ansamble:
    def __init__(self, model, input_size, output_size, models_num, train_size, epoch, batch_size, lr):
        self.output_size = output_size
        self.train_size = train_size
        self.models_num = models_num
        self.models = [model(input_size, output_size, epoch, batch_size, lr) for _ in range(models_num)]
    
    def fit(self, X: torch.Tensor, Y: torch.Tensor):
        N = X.shape[0]
        n = int(self.train_size * N)
        for model in self.models:
            indices = torch.randperm(N)
            model.fit(X[indices[:n]], Y[indices[:n]])
                        
    def predict(self, X):
        X = X.type(torch.float64)
        answers = torch.zeros((X.shape[0], self.output_size))
        for model in self.models:
            pred = model(X)
            answers += pred
        answers = torch.argmax(answers, dim=1)
        return answers

    
    