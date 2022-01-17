# coding=utf-8
# Copyright 2021 The OneFlow Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

sys.path.append(".")

from libai.config.instantiate import instantiate
from libai.config import LazyConfig
from libai.data.structures import Instance

cfg = LazyConfig.load("./configs/common/data/nlp_data.py")

train_loader, val_loader, test_loader = instantiate(cfg.dataloader.train)
print(len(train_loader), len(val_loader), len(test_loader))
for sample in test_loader:
    assert isinstance(sample, Instance)
    break

test_loader = instantiate(cfg.dataloader.test)
for loader in test_loader:
    print(f"test loader: {len(loader)}")
    for sample in loader:
        assert isinstance(sample, Instance)
        break