from app.tasks import collect_zentrade_data

def test_collect_zentrade_data():
    result = collect_zentrade_data()
    assert result is None  # 작업이 성공적으로 완료되었는지 확인