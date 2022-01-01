from libai.config import LazyCall
from .common.models.bert import pretrain_model as model
from .common.train import train
from .common.optim import optim, lr_scheduler
from .common.data.nlp_data import data
from libai.models import BertForPretrainingGraph

# Bert-large model config
model.cfg.num_attention_heads = 16
model.cfg.hidden_size = 768
model.cfg.hidden_layers = 8

# Set pipeline layers for paralleleism
train.dist.pipeline_num_layers = model.cfg.hidden_layers

train.micro_batch_size = 16

# Set fp16 ON
train.amp.enabled = True

# fmt: off
graph = dict(
    # options for graph or eager mode
    enabled=True,
    train=LazyCall(BertForPretrainingGraph)(
        fp16=train.amp.enabled,
        is_eval=False,
    ),
    eval=LazyCall(BertForPretrainingGraph)(
        fp16=train.amp.enabled, 
        is_eval=True,),
)
# fmt: on