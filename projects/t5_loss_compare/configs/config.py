from libai.config import LazyCall, get_config

from libai.scheduler import WarmupMultiStepLR

from .t5_dataset import dataloader, tokenization

model = get_config("./common/models/t5.py").pretrain_model
graph = get_config("./common/models/graph.py").graph
train = get_config("./common/train.py").train
optim = get_config("./common/optim.py").optim

train.eval_iter = 10


# Set all dropout to 0.
model.cfg.hidden_dropout_prob = 0.0
model.cfg.attention_probs_dropout_prob = 0.0
model.cfg.embedding_dropout_prob = 0.0

# Set matched model arguments
model.cfg.hidden_layers = 6
model.cfg.hidden_size = 384
model.cfg.intermediate_size = 1536
model.cfg.num_attention_heads = 12
model.cfg.max_position_embeddings = 512

train.train_iter = 1000
train.micro_batch_size = 16
train.train_micro_batch_size = 16
train.log_period = 1
train.warmup_ratio = 0.00

# graph.enabled = False


# Set a constant lr scheduler after warmup
optim.lr = 0.0001
train.scheduler = LazyCall(WarmupMultiStepLR)(warmup_factor=0.1, warmup_iter=0, milestones=[0.99])


for ds in dataloader.train.dataset:
    ds.max_num_samples = train.train_iter * train.micro_batch_size