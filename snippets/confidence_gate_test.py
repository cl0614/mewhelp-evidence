# 摘自 tests/graph/test_ch09_confidence_gate.py 第 40-59 行
# 仅用于面试核验，不是完整文件

async def test_low_confidence_blocks_with_source_and_snapshot(stub_retrieval, stub_selfcheck, monkeypatch):
    monkeypatch.setattr("app.config.settings.evidence_confidence_threshold", 0.5)
    stub_retrieval(_mk_hits(0.15, 0.14))          # 弱证据 → 置信度闸拦下
    stub_selfcheck(True)
    out = await nodes.retrieve_knowledge(_state())
    assert out["evidence_strong"] is False
    assert out["fallback_source"] == "retrieval_low_conf"
    assert len(out["retrieved_snapshot"]) == 2    # 走了检索就有快照
    assert out["evidence_confidence"] < 0.5
    assert "confidence_signals" in out["trace"]


async def test_selfcheck_fail_labels_self_check(stub_retrieval, stub_selfcheck, monkeypatch):
    monkeypatch.setattr("app.config.settings.evidence_confidence_threshold", 0.3)
    stub_retrieval(_mk_hits(0.9, 0.3, 0.3))
    stub_selfcheck(False, "缺关键信息")
    out = await nodes.retrieve_knowledge(_state())
    assert out["evidence_strong"] is False
    assert out["fallback_source"] == "self_check"
    assert out["retrieved_snapshot"]              # 自评不过同样有快照
