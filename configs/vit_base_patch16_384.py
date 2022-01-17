from libai.config import LazyCall
from libai.scheduler import WarmupCosineLR
from .common.models.vit import vit_model as model
from .common.train import train
from .common.optim import optim


from libai.models import VisionTransformerGraph

# ViT-Base-Patch16-384 model config
model.cfg.img_size = 384

# Refine optimizer cfg for vit model
optim.lr = 5e-4
optim.weight_decay = 1e-8

# Set scheduler cfg for vit model
scheduler = LazyCall(WarmupCosineLR)(
    max_iters=10000,
    warmup_iters=1000,
    warmup_factor = 0.001,
    alpha = 0.01
)

# Set pipeline layers for paralleleism
train.dist.pipeline_num_layers = model.cfg.num_layers

# Refine train cfg for vit model
train.warmup_epochs = 20
train.epochs = 300
train.micro_batch_size = 128

# Set fp16 ON
train.amp.enabled = True

# fmt: off
graph = dict(
    # options for graph or eager mode
    enabled=True,
    train_graph=LazyCall(VisionTransformerGraph)(
        fp16=train.amp.enabled,
        is_train=True,
    ),
    eval_graph=LazyCall(VisionTransformerGraph)(
        fp16=train.amp.enabled, 
        is_train=False,),
    debug = False,
)
# fmt: on