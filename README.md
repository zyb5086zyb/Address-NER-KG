# pipeline： NER+知识图谱解决地址解析
### 1. NER

使用BI-LSTM+CRF解决

#### ner模型训练

python train_lstm_crf.py

### 2.搭建知识图谱

#### 知识图谱数据处理

python process_data_kg.py

#### 知识图谱构建

python build_addressgraph.py

### 3.NER模型结果

![alt](https://github.com/zyb5086zyb/Address-NER-KG/blob/main/images/ner_result.png)

### KG结果图

![alt](https://github.com/zyb5086zyb/Address-NER-KG/blob/main/images/kg_result.png)

