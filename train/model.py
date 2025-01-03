import torch
import torch.functional as F

class CIFARPredictor(torch.nn.Module):
    def __init__(self):
        super().__init__()
        # in_dim = 3, 3, 21
        self.predictor = torch.nn.Sequential(
            torch.nn.Conv2d(12, 6, 3, padding=2),
            torch.nn.ReLU(True),
            torch.nn.Dropout(0.5),
            torch.nn.Flatten(),
            torch.nn.Linear(150, 64),
            torch.nn.ReLU(True),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(True),
            torch.nn.Linear(32, 10),
        )

    def forward(self, x):
        return F.softmax(self.predictor(x), dim=1)