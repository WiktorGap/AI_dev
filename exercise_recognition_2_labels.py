from fastai.vision.all import *
import pandas as pd
import os
from sklearn.metrics import f1_score



path = Path('dataset')
df = pd.read_csv(path / 'labels.csv')
df['labels'] = df['labels'].str.split(' ')


assert df['labels'].apply(len).eq(2).all(), "Każdy przykład musi mieć dokładnie 2 etykiety!"

def get_x(row): return path / row['filename']
def get_y(row): return row['labels']


mean = tensor([0.4583, 0.4312, 0.4219])
std = tensor([0.3187, 0.3049, 0.3014])


dblock = DataBlock(
    blocks=(ImageBlock, MultiCategoryBlock),
    get_x=get_x,
    get_y=get_y,
    splitter=RandomSplitter(seed=42),
    item_tfms=Resize(460),
    batch_tfms=[*aug_transforms(size=224), Normalize.from_stats(mean, std)]
)


dls = dblock.dataloaders(df, bs=32)

model = resnet50  
learn = vision_learner(dls, model, loss_func=BCEWithLogitsLossFlat(), metrics=accuracy_multi)


learn.fine_tune(12, base_lr=3e-3)


preds, targs = learn.tta()
pred_labels = (preds > 0.5).int()
f1 = f1_score(targs, pred_labels, average='samples')
print(f"F1 score (dla wielu etykiet): {f1:.4f}")

learn.export('gym_model.pkl')
