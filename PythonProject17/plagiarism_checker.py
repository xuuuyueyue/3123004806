import sys
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import datetime


class PlagiarismChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def preprocess_text(self, text):
        """预处理文本：去除标点符号，分词"""
        # 去除标点符号
        text = re.sub(r'[^\w\s]', '', text)
        # 使用jieba分词
        words = jieba.cut(text)
        return ' '.join(words)

    def read_file(self, file_path):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"错误：文件 {file_path} 不存在")
            sys.exit(1)
        except Exception as e:
            print(f"读取文件时出错：{e}")
            sys.exit(1)

    def calculate_similarity(self, original_text, copied_text):
        """计算文本相似度"""
        # 预处理文本
        original_processed = self.preprocess_text(original_text)
        copied_processed = self.preprocess_text(copied_text)

        # 创建TF-IDF向量
        tfidf_matrix = self.vectorizer.fit_transform([original_processed, copied_processed])

        # 计算余弦相似度
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return similarity[0][0]

    def check_plagiarism(self, original_path, copied_path, output_path):
        """主函数：检查抄袭"""
        # 读取文件
        original_text = self.read_file(original_path)
        copied_text = self.read_file(copied_path)

        # 计算相似度
        similarity = self.calculate_similarity(original_text, copied_text)

        # 获取当前时间
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 输出结果到文件（追加模式）
        try:
            with open(output_path, 'a', encoding='utf-8') as f:  # 改为 'a' 模式（追加）
                # 写入分隔线和时间戳
                f.write(f"\n{'=' * 50}\n")
                f.write(f"查重时间：{current_time}\n")
                f.write(f"原文文件：{original_path}\n")
                f.write(f"对比文件：{copied_path}\n")
                f.write(f"重复率：{similarity:.2%}\n")
                f.write(f"相似度分数：{similarity:.4f}\n")

            print(f"查重完成！重复率：{similarity:.2%}")
            print(f"结果已追加保存到：{output_path}")
        except Exception as e:
            print(f"写入输出文件时出错：{e}")
            sys.exit(1)


def main():
    # 检查命令行参数
    if len(sys.argv) != 4:
        print("用法: python plagiarism_checker.py <原文文件路径> <抄袭版文件路径> <输出文件路径>")
        print("示例: python plagiarism_checker.py orig.txt copied.txt result.txt")
        sys.exit(1)

    # 获取命令行参数
    original_path = sys.argv[1]
    copied_path = sys.argv[2]
    output_path = sys.argv[3]

    # 创建查重器并执行查重
    checker = PlagiarismChecker()
    checker.check_plagiarism(original_path, copied_path, output_path)


if __name__ == "__main__":
    main()