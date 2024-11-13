"""fedlc: A Flower Baseline."""

import torch

from flwr.client import ClientApp, NumPyClient
from flwr.common import Context
from fedlc.dataset import load_data
from fedlc.model import get_weights, set_weights, test, train, initialize_model


class FlowerClient(NumPyClient):
    """A class defining the client."""

    def __init__(self, net, trainloader, valloader, local_epochs, learning_rate):
        self.net = net
        self.trainloader = trainloader
        self.valloader = valloader
        self.local_epochs = local_epochs
        self.learning_rate = learning_rate
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.net.to(self.device)

    def fit(self, parameters, config):
        """Traim model using this client's data."""
        set_weights(self.net, parameters)
        train_loss = train(
            self.net,
            self.trainloader,
            self.local_epochs,
            self.device,
            self.learning_rate
        )
        return (
            get_weights(self.net),
            len(self.trainloader.dataset),
            {"train_loss": train_loss},
        )

    def evaluate(self, parameters, config):
        """Evaluate model using this client's data."""
        set_weights(self.net, parameters)
        loss, accuracy = test(self.net, self.valloader, self.device)
        return loss, len(self.valloader.dataset), {"accuracy": accuracy}


def client_fn(context: Context):
    """Construct a Client that will be run in a ClientApp."""
    # Load model and data
    
    # 3 channels and 10 classes for CIFAR-10
    net = initialize_model("resnet18", channels=3, num_classes=10)

    print(f"context in client: ", context)

    batch_size = int(context.run_config["batch-size"])
    local_epochs = int(context.run_config["local-epochs"])
    learning_rate = int(context.run_config["learning-rate"])

    partition_id = int(context.node_config["partition-id"])
    num_partitions = int(context.node_config["num-partitions"])
    trainloader, valloader = load_data(partition_id, num_partitions, batch_size)

    # Return Client instance
    return FlowerClient(net, trainloader, valloader, local_epochs, learning_rate).to_client()


# Flower ClientApp
app = ClientApp(client_fn)
