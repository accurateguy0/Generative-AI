import torch
import torch.nn as nn
import torch.nn.functional as F

class MedNet(nn.Module):
    def __init__(self, in_channels, num_classes):
        super(MedNet, self).__init__()
        
        # Warstwa 1
        # Używamy 16 filtrów, aby znaleźć proste rzeczy ( krawędzie, kropki )
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2) # Obraz staje się 14x14
        )
        
        # Warstwa 2: Bardziej złożone kształty
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2) # Obraz staje się 7x7
        )

        # Warstwa 3: Konkretne skomplikowane kształty
        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128), # normalizacja
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)) # Spłaszcza do rozmiaru 1x1
        )
        
        # Fully Connected Layer: The "Decision Maker"
        self.fc = nn.Sequential(
            nn.Linear(128, 128), # Standardowa warstwa neuronowa. Bierze 128 cech obrazka i próbuje znaleźć najbardziej prawdopodobny typ komórki
            nn.ReLU(),
            nn.Dropout(0.5), # pomaga zapobiec overfitting
            nn.Linear(128, num_classes) 
        )

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = x.view(x.size(0), -1) # spłaszczenie dla warstwy liniowej
        x = self.fc(x)
        return x

# Test modelu poprzez sztuczny obrazek Batch size 1, 3 color channels (RGB), 28x28 size
if __name__ == "__main__":
    model = MedNet(in_channels=3, num_classes=8)
    test_input = torch.randn(1, 3, 28, 28)
    test_output = model(test_input)
    print(f"Output shape: {test_output.shape}") # Powinno wyjść [1, 8]
