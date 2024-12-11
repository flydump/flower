---
title: FedRS: Federated Learning with Restricted Softmax for LabelDistribution Non-IID Data
url: https://www.lamda.nju.edu.cn/lixc/papers/FedRS-KDD2021-Lixc.pdf
labels: [data heterogeneity, image classification] 
dataset: [cifar10] 
---

# FedRS: Federated Learning with Restricted Softmax for Label Distribution Non-IID Data

> [!NOTE]
> If you use this baseline in your work, please remember to cite the original authors of the paper as well as the Flower paper.

**Paper:** https://www.lamda.nju.edu.cn/lixc/papers/FedRS-KDD2021-Lixc.pdf

**Authors:** Xin-Chun Li, De-Chuan Zhan

**Abstract:** Federated Learning (FL) aims to generate a global shared model via collaborating decentralized clients with privacy considerations. Unlike standard distributed optimization, FL takes multiple optimization steps on local clients and then aggregates the model updates via a parameter server. Although this significantly reduces communication costs, the non-iid property across heterogeneous devices could make the local update diverge a lot, posing a fundamental challenge to aggregation. In this paper, we focus on a special kind of non-iid scene, i.e., label distribution skew, where each client can only access a partial set of the whole class set. Considering top layers of neural networks are more task-specific, we advocate that the last classification layer is more vulnerable to the shift of label distribution. Hence, we in-depth study the classifier layer and point out that the standard softmax will encounter several problems caused by missing classes. As an alternative, we propose “Restricted Softmax" to limit the update of missing classes’ weights during the local procedure. Our proposed FedRS is very easy to implement with only a few lines of code. We investigate our methods on both public datasets and a real-world service awareness application. Abundant experimental results verify the superiorities of our methods.

## About this baseline

**What’s implemented:** Performance comparison between `FedAvg`, `FedRS (alpha=0.5)` and `FedRS (alpha=0.9)` on VGG model and CIFAR10 with avg 5 classes per client (`Table 5` of paper)

The reproduced results are not exactly same as Table 5, although they do show that FedRS performs better than both FedAvg and FedProx under label skew.

**Datasets:** CIFAR10

**Hardware Setup:** The paper samples 10 clients for 1000 rounds. GPU is recommended. The results below were obtained on a machine with 1x NVIDIA L4 Tensor Core GPU, with 16 vCPUs and 64GB of RAM.

**Contributors:** [@flydump](https://github.com/flydump)

## Experimental Setup

**Task:** Image classification

**Model:** A 9-layer VGG model with 9,225,600 parameters and without batch norm. 

**Dataset:** The implementation is only for the CIFAR-10 dataset currently. Data is partitioned using [ShardPartitioner](https://flower.ai/docs/datasets/ref-api/flwr_datasets.partitioner.ShardPartitioner.html) which sorts the dataset by labels and creates shards, and randomly allocates shards to each client (the number of which depends on the `num-shards-per-partition` arg)

The paper uses a slightly different partitioning scheme, where samples for each class is divided into equal number of partitions, and allocate N shards (across all classes) to each client, such that each client has 5 classes on average.

**Training Hyperparameters:** Table below shows the **default** training hyperparams for the experiments. Values are from the original paper where provided (e.g. learning rate, momentum, weight decay)

| Description | Default Value |
| ----------- | ----- |
| strategy | fedavg |
| scaling factor for missing classes (alpha) | 0.9 |
| fraction fit | 0.1 |
| local epochs | 2 |
| learning rate | 0.03 |
| momentum | 0.9 |
| weight decay | 5e-4 |
| number of rounds | 1000 |
| batch size | 64 |
| num shards per partition | 5 |
| model | vgg11 |

## Environment Setup


```bash
# Create the virtual environment
pyenv virtualenv 3.10.14 <name-of-your-baseline-env>

# Activate it
pyenv activate <name-of-your-baseline-env>

# Install the baseline
pip install -e .
```

If running with **wandb**:

```
wandb login
```

## Running the Experiments

## Table 5 (Performance comparisons with standard FL algorithms (VGG11))

### Commands for C10-100-5 (CIFAR-10 with 100 clients and 5 shards per client)

|  | Command
| ----------- | ----- | 
| FedAvg (default) | `flwr run .` | 
| FedProx (0.0001)| `flwr run . --run-config "alg='fedprox' proximal-mu=0.0001"` | 
| FedProx (0.001)| `flwr run . --run-config "alg='fedprox' proximal-mu=0.001"` | 
| FedRS ($\alpha$=0.5)| `flwr run . --run-config "alpha=0.5"` | 
| FedRS ($\alpha$=0.9) | `flwr run . --run-config "alpha=0.9"` | 

### Commands for C10-100-2 (CIFAR-10 with 100 clients and 2 shards per client)

|  | Command
| ----------- | ----- | 
| FedAvg (default) | `flwr run . --run-config num-shards-per-partition=2` | 
| FedProx (0.0001)| `flwr run . --run-config "alg='fedprox' proximal-mu=0.0001 num-shards-per-partition=2"` | 
| FedProx (0.001)| `flwr run . --run-config "alg='fedprox' proximal-mu=0.001 num-shards-per-partition=2"` | 
| FedRS ($\alpha$=0.5)| `flwr run . --run-config "alpha=0.5 num-shards-per-partition=2"` | 
| FedRS ($\alpha$=0.9) | `flwr run . --run-config "alpha=0.9 num-shards-per-partition=2"` | 

### Commands for C100-100-20 (CIFAR-100 with 100 clients and 20 shards per client)

|  | Command
| ----------- | ----- | 
| FedAvg (default) | `flwr run . --run-config num-shards-per-partition=20 dataset='cifar100'` | 
| FedProx (0.0001)| `flwr run . --run-config "alg='fedprox' proximal-mu=0.0001 num-shards-per-partition=20 dataset='cifar100'` | 
| FedProx (0.001)| `flwr run . --run-config "alg='fedprox' proximal-mu=0.001 num-shards-per-partition=20 dataset='cifar100'` | 
| FedRS ($\alpha$=0.5)| `flwr run . --run-config "alpha=0.5 num-shards-per-partition=20 dataset='cifar100'` | 
| FedRS ($\alpha$=0.9) | `flwr run . --run-config "alpha=0.9 num-shards-per-partition=20 dataset='cifar100'` | 


After 1000 server steps, the accuracy results are as follows:

|  | C10-100-5 
| ----------- | ----- |
| FedAvg | 0.8 | 
| FedProx (0.0001)| 0.7791 | 
| FedProx (0.001)| 0.7914 | 
| FedRS ($\alpha$=0.5)| 0.8149 | 
| FedRS ($\alpha$=0.9) | 0.8149 | 

![FedAvg](_static/accuracy.png)