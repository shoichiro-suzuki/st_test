# 罠DBから罠をカウントし、罠IDを割り振る
from azure_.cosmosdb import search_container_by_query

trap_db = [
    {
        "trap_id": 1,
        "trap_name": "花の村ソーラーの道",
        "trap_lat": 34.600521,
        "trap_lon": 137.121363,
        "trap_type": "箱罠",
        "trap_status": "active",
        "trap_count": 1,
    },
    {
        "trap_id": 2,
        "trap_name": "花の村駐車場横",
        "trap_lat": 34.600521,
        "trap_lon": 137.121363,
        "trap_type": "くくり罠",
        "trap_status": "active",
        "trap_count": 3,
    },
]


def count_trap():
    # 登録罠数をカウントする
    database_name = "02_Documents"
    container_name = "study"
    query = "SELECT VALUE COUNT(1) FROM c"
    parameters = []
    res = search_container_by_query(
        database_name,
        container_name,
        query,
        parameters,
    )
    count = res[0] if res else 0
    return count
