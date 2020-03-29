from adpocket import AdPocket

client = AdPocket(email="user@example.com", password="password", adid="00000000-0000-0000-0000-000000000000")

resp = client.redeemTrueMoney("09XXXXXXXX", 1000)
print(resp["ret_msg"])
