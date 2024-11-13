"""fedlc: A Flower Baseline."""

from typing import List, Tuple

from flwr.common import Context, Metrics
from flwr.server import ServerApp, ServerAppComponents, ServerConfig
from flwr.server.strategy import FedAvg, FedProx


# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    """Do weighted average of accuracy metric."""
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * float(m["accuracy"]) for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


def server_fn(context: Context):
    """Construct components that set the ServerApp behaviour."""
    # Read from config
    num_rounds = context.run_config["num-server-rounds"]
    fraction_fit = context.run_config["fraction-fit"]
    fraction_evaluate = context.run_config["fraction-evaluate"]
    proximal_mu = context.run_config["proximal-mu"]

    # Define strategy
    if context.run_config["strategy"] == "fedprox":
        strategy = FedProx(
            fraction_fit=float(fraction_fit),
            fraction_evaluate=float(fraction_evaluate),
            evaluate_metrics_aggregation_fn=weighted_average,
            proximal_mu=float(proximal_mu),
        )
    else:
        # default to FedAvg
        strategy = FedAvg(
            fraction_fit=float(fraction_fit),
            fraction_evaluate=float(fraction_evaluate),
            evaluate_metrics_aggregation_fn=weighted_average,
        )
    config = ServerConfig(num_rounds=int(num_rounds))

    return ServerAppComponents(strategy=strategy, config=config)


# Create ServerApp
app = ServerApp(server_fn=server_fn)
