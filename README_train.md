# model_training.sh

微调bge模型，即model_training.sh的解读

- [model\_training.sh](#model_trainingsh)
  - [1. Installation](#1-installation)
  - [2. Data format](#2-data-format)
  - [3. Train](#3-train)
## 1. Installation

- **with pip**

```shell
pip install -U FlagEmbedding[finetune]
```

## 2. Data format

Train data should be a json file, where each line is a dict like this:

```shell
{ "query": str, "pos": List[str], "neg": List[str] }
```

`query` 是查询，`pos` 是正文本列表，`neg` 是负文本列表。 

## 3. Train

torchrun部分的可选参数：
- **`model_name_or_path`**： 用于训练的模型存储路径。
- **`config_name`**： 预训练的配置名称或路径（如果与模型名称不相同）。
- **`tokenizer_name`**： 预训练的标记符号名称或路径（如果与模型名不相同）。
- **`cache_dir`**： 从 s3 下载的预训练模型的存储位置。
- **`trust_remote_code`**： 信任远程代码。
- **`token`**： 访问模型时使用的令牌。
- **`train_data`**： 一个或多个训练数据路径。
- **`cache_path`**： 缓存数据的存储位置。
- **`train_group_size`**： 训练时每批次每组数据大小
- **`query_max_len`**： 经过标记化后的最大输入序列总长度。 长度超过此值的序列将被截断。
- **`passage_max_len`**： 经过标记化后的最大输入序列总长度。 长度超过此值的序列将被截断。
- **`pad_to_multiple_of`**： 如果设置，将把序列填充为所提供值的倍数。
- **`max_example_num_per_dataset`**： 每个数据集的最大示例数。
- **`query_instruction_for_retrieval`**： 查询嵌入指令。
- **`query_instruction_format`**： 查询指令的格式。
- **`knowledge_distillation`**： 当 `pos_scores： List[float]` 和 `neg_scores： List[float]` 包含在训练数据里时，使用知识蒸馏。
- **`passage_instruction_for_retrieval`**： 文档嵌入指令。
- **`passage_instruction_format`**： 文档指令的格式。
- **`shuffle_ratio`**： 文本的洗牌比例。
- **`same_dataset_within_batch`**： 同一批次中的所有样本来自同一个数据集。
- **`small_threshold`**： 小数据集的阈值。 同一目录下的所有小数据集将合并为一个数据集。
- **`drop_threshold`**： 放弃合并后的小数据集的阈值。 如果合并后的小数据集中的示例数量少于此阈值，则会被丢弃。
- **`negatives_cross_device`**： 跨设备共享负样本。
- **`temperature`**： 用于相似性评分的温度。
- **`fix_position_embedding`**： 冻结位置嵌入的参数。
- **`sentence_pooling_method`**： 池化方法。 可用选项：cls、mean、last_token。 默认值：cls。
- **`normalize_embeddings`**： 是否规范化嵌入。
- **`sub_batch_size`**： 训练的子批次大小。
- **`kd_loss_type`**： 知识提炼的损失类型。 可用选项：kl_div、m3_kd_loss。 默认值：kl_div。

```shell
torchrun --nproc_per_node 8 \
	-m FlagEmbedding.finetune.embedder.encoder_only.base \
	--model_name_or_path BAAI/bge-large-en-v1.5 \
    --output_dir ./test_encoder_only_base_bge-large-en-v1.5 \
    --train_data ./example_data/retrieval \
    --overwrite_output_dir \
    --trust_remote_code \
    --num_train_epochs 2 \
    --train_group_size 8 \
    --per_device_train_batch_size 2 \
    --learning_rate 1e-5 \
    --query_max_len 512 \
    --passage_max_len 512 \
    --query_instruction_for_retrieval '为这个问题生成嵌入表示来检索文章: ' \
    --query_instruction_format '{}{}' \
    --query_instruction_for_retrieval '为这个文章生成嵌入表示来供问题检索: ' 
    --query_instruction_format '{}{}' \
    --knowledge_distillation False \
    --fp16 \
    --cache_dir ./cache/model \
    --cache_path ./cache/data \
    --dataloader_drop_last True \
    --warmup_ratio 0.1 \
    --gradient_checkpointing \
    --deepspeed ../ds_stage0.json \
    --logging_steps 1 \
    --save_steps 1000 \
    --negatives_cross_device \
    --temperature 0.02 \
    --sentence_pooling_method cls \
    --normalize_embeddings True \
    --kd_loss_type kl_div
```
