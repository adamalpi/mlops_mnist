from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

EXPERIMENTS_LOCATION = "fashion_mnist_experiment"
MODEL_NAME_CONVENTION = "model.pth"

# constant for classes
classes = (
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle Boot",
)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class Model:
    """Classifier wrapper for torch models."""

    def __init__(self, experiment_name: str, root_dir: str = "."):
        """Model constructor.

        Args:
            experiment_name: name of experiment (refer to csv column
                -> Experiment Name)
            root_dir: root directory where to find the models
        """
        self.experiment_name = experiment_name
        self.root_dir = Path(root_dir)

        if not self.root_dir.exists():
            raise FileNotFoundError(
                f"Root directory does not exist. Abs path: {str(self.root_dir.absolute())}"
            )

        self.model_path = (
                    self.root_dir / EXPERIMENTS_LOCATION / self.experiment_name / MODEL_NAME_CONVENTION
                )
        self.model = None
        self.load()

    def load(self):
        """Loads serialized model into memory.

        Raises:
            FileNotFoundError: if model file does not exist. Model file name is configured 
        """
    
        if not self.model_path.exists():
            raise FileNotFoundError("Experiment does not exist.")

        self.model = Net()
        self.model.load_state_dict(torch.load(self.model_path))

    def inference(self, image):
        """Runs model prediction.

        Args:
            image (PIL.Image) as input for the model
        """
        transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
        )
        x = transform(image)[0].unsqueeze(0).unsqueeze(0)
        pred = self.model(x)
        idx = torch.argmax(pred).cpu().detach().numpy()

        return classes[idx]
