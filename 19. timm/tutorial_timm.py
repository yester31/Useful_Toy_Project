import timm
import torch
from pprint import pprint

# timm 에서 제공 하는 모델 zoo 리스트
model_names = timm.list_models(pretrained=True)
pprint(model_names)

# feature extractor 로 사용 하기
model = timm.create_model('efficientnetv2_rw_s',features_only=True,  pretrained=True)
model.eval()
print(model)

print(f'Feature channels: {model.feature_info.channels()}')
o = model(torch.randn(2, 3, 224, 224))
for x in o:
  print(x.shape)


