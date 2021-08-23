# Copyright The PyTorch Lightning team.
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
import os
import re
from unittest import mock

import pytest
import torch

from flash import Trainer
from flash.core.utilities.imports import _TEXT_AVAILABLE
from flash.text import QuestionAnsweringTask
from flash.text.question_answering.data import QuestionAnsweringPostprocess, QuestionAnsweringPreprocess
from tests.helpers.utils import _SERVE_TESTING, _TEXT_TESTING

# ======== Mock functions ========

SEQUENCE_LENGTH = 384


class DummyDataset(torch.utils.data.Dataset):
    def __getitem__(self, index):
        return {
<<<<<<< HEAD:tests/text/question_answering/test_model.py
            "input_ids": torch.randint(1000, size=(SEQUENCE_LENGTH, )),
            "attention_mask": torch.randint(1, size=(SEQUENCE_LENGTH, )),
            "start_positions": torch.randint(1000, size=(1, )),
            "end_positions": torch.randint(1000, size=(1, )),
=======
            "input_ids": torch.randint(1000, size=(128,)),
            "labels": torch.randint(1000, size=(128,)),
>>>>>>> master:tests/text/seq2seq/question_answering/test_model.py
        }

    def __len__(self) -> int:
        return 100


# ==============================

TEST_BACKBONE = "distilbert-base-uncased"


@pytest.mark.skipif(os.name == "nt", reason="Huggingface timing out on Windows")
@pytest.mark.skipif(not _TEXT_TESTING, reason="text libraries aren't installed.")
def test_init_train(tmpdir):
    model = QuestionAnsweringTask(TEST_BACKBONE)
    train_dl = torch.utils.data.DataLoader(DummyDataset())
    trainer = Trainer(default_root_dir=tmpdir, fast_dev_run=True)
    trainer.fit(model, train_dl)


@pytest.mark.skipif(not _SERVE_TESTING, reason="serve libraries aren't installed.")
@mock.patch("flash._IS_TESTING", True)
def test_serve():
    model = QuestionAnsweringTask(TEST_BACKBONE)
    # TODO: Currently only servable once a preprocess and postprocess have been attached
    model._preprocess = QuestionAnsweringPreprocess(backbone=TEST_BACKBONE)
    model._postprocess = QuestionAnsweringPostprocess()
    model.eval()
    model.serve()


@pytest.mark.skipif(_TEXT_AVAILABLE, reason="text libraries are installed.")
def test_load_from_checkpoint_dependency_error():
    with pytest.raises(ModuleNotFoundError, match=re.escape("'lightning-flash[text]'")):
        QuestionAnsweringTask.load_from_checkpoint("not_a_real_checkpoint.pt")
