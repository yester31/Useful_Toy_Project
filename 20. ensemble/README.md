# Ensemble
- Detectron2 (git commit id 5e38c1...)
- Faster RCNN R101-DC5
- Faster RCNN R101-FPN 
- Faster RCNN X101-FPN 
- COCO 2017 val Dataset
- Recommend to run in Colab


## Algorithms
- NMS : 내림차순 정렬 후, 가장 높은 스코어의 바운딩 박스를 기준으로 IOU 임곗값을 초과하는 바운딩 박스를 제거.


- soft NMS : NMS와 달리, 비교 과정에서 IOU 임곗값을 초과하는 박스를 그냥 제거하는 것이 아니라 스코어 값을 기존 보다 낮게 변경 처리함.


- NMW : 동일한 객체에 대해서 IOU 임곗값을 초과하는 바운딩 박스들의 그룹을 만들고 
각각의 IOU 값과 스코어 값으로 가중치를 만들어 그 그룹을 대표하는 값을 생성(라벨과 스코어는 그룹 중 스코어가 가장 높은 값 사용).


- WBF : 동일한 객체에 대해서 IOU 임곗값을 초과하는 바운딩 박스들의 그룹을 만들고 
모델에 대한 가중치 값이 적용된 스코어 값을 그 그룹에서 가중치로 사용하여 대표하는 값을 생성(라벨은 그룹 중 스코어가 가장 높은 값, 스코어는 평균값 사용).

## Performance Evaluation
- box AP (Average Precision at IoU=0.50:0.95, area=all)

<table border="0"  width="100%">
	<tbody align="center">
		<tr>
			<td>Faster RCNN backbone</td>
            <td>R101-DC5</td>
            <td>R101-FPN</td>
            <td>X101-FPN</td>
		</tr>
		<tr>
			<td>box AP</td>
			<td>40.631</td>
			<td>42.036</td>
			<td>43.047</td>
		</tr>
	</tbody>
</table>


<table border="0"  width="100%">
	<tbody align="center">
		<tr>
			<td>Ensemble Method</td>
            <td>NMS</td>
            <td>soft NMS</td>
            <td>NMW</td>
            <td><strong>WBF</strong></td>
		</tr>
		<tr>
			<td>box AP</td>
			<td>43.9</td>
			<td>44.0</td>
			<td>44.7</td>
			<td><strong>46.0</strong></td>
		</tr>
	</tbody>
</table>

## Description
- 다양한 앙상블 기법들을 실제로 계산을 통해 결과를 추출하였고 그 값들에 대해 비교 평가함.
- 모든 기법들의 결과값은 각 모델의 결과 보다 나은 성능을 보임.
- NMS와 soft-NMS의 경우 가장 높은 스코어를 갖는 바운딩 박스 하나만을 기준으로 겹치는 정도에 따라 나머지 바운딩 박스를 제거하는 방식으로 이루어지지만, 
NMW와 WBF의 경우 여러 바운딩 박스들의 정보를 종합하여 결과를 내기 때문에 더 우수한 것으로 보임.
- 특히, WBF의 경우 앙상블에서 쓰인 딥러닝 모델들의 가중치 값도 사용하기 때문에 NMW 보다 더 많은 정보를 기반으로 처리한다고 할 수 있음. 
그렇기 때문에 더 나은 성능을 나타낸 것으로 보임.


## Reference
- Detectron2 : <https://github.com/facebookresearch/detectron2>
- WBF : <https://arxiv.org/abs/1910.13302>
- soft NMS : <https://arxiv.org/abs/1704.04503>
- NMW : <https://openaccess.thecvf.com/content_ICCV_2017_workshops/papers/w14/Zhou_CAD_Scale_Invariant_ICCV_2017_paper.pdf>
- pycocotools : <https://github.com/cocodataset/cocoapi>
- ensemble-boxes : <https://github.com/ZFTurbo/Weighted-Boxes-Fusion>