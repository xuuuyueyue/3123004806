# 更新 README.md 添加使用说明：
'''
# 文本查重系统

基于TF-IDF和余弦相似度的中文文本查重工具

## 功能特点
- 中文分词处理
- TF-IDF特征提取
- 余弦相似度计算
- 文件读写支持
- 结果输出到文件
- 追加模式记录历史

## 使用方法

```bash
# 基础用法
python plagiarism_checker.py original.txt copied.txt

# 输出结果到文件
python plagiarism_checker.py original.txt copied.txt result.txt
