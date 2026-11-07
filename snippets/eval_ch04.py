# 摘自 scripts/eval_ch04.py 第 44-54 行
# 仅用于面试核验，不是完整文件

STRATEGIES = ["vector", "bm25", "hybrid", "hybrid_rerank"]
GRADED_BUCKETS = ["A_policy", "B_model", "C_colloquial", "E_multi"]  # 可作答桶
STRATEGY_LABEL = {"vector": "纯向量", "bm25": "纯 BM25", "hybrid": "混合",
                  "hybrid_rerank": "混合 + 重排"}
BUCKET_LABEL = {"A_policy": "政策类", "B_model": "型号类",
                "C_colloquial": "口语类", "E_multi": "跨文档类", "overall": "总体"}
SKIP_GEN = "--skip-gen" in sys.argv   # 只跑确定性两段(裁判上游不可用时)
K = 10                 # 检索深度:喂给生成段与证据覆盖度的条数,跟线上 rerank_top_k 对齐
RECALL_K = 5           # 召回率的截断位:一道题需要的证据要在前五条里凑齐
