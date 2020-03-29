from Crypto.Cipher import AES
import requests
import datetime
import hashlib
import random
import json
import uuid

class AdPocket:

	isLogged = False
	headers = {
		"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; LG-US996 Build/NRD90M)"
	}

	def __init__(self, email, password, adid="", udid=""):
		# Note that adid is a shared pref property which is located at /data/data/net.fsnasia.adpocket/shared_prefs/ADPOCKET.xml
		# if both udid and adid are not defined, the module will generate new for each created classes
		# which haven't confirmed to be working with redeemTrueMoney() yet
		#
		self.email = email
		self.password = password

		if udid:
			self.udid = udid
		else:
			if adid:
				self.adid = uuid.UUID(adid)
			else:
				self.adid = uuid.uuid4()
			self.udid = "{0}-{1}".format(hashlib.sha1(str(self.adid).encode()).hexdigest(), self.adid.hex[0] + str(len(str(self.adid))) + self.adid.hex[-1])

		self.login_resp = self._login()

	def _generate_h(self, t):
		secret_padding = "b05bb1122c80a2593362fdec22b14c0c" # Yes, cracked by Noxturnix ;)
		return hashlib.sha256(secret_padding.encode() + t.encode()).hexdigest()

	def _login(self):
		json_data = {
			"id": self.email,
			"pwd": hashlib.sha256(self.password.encode()).hexdigest()
		}
		data = {
			"json": json.dumps(json_data, separators=(",", ":"))
		}
		json_resp = requests.post("http://th-api.fsnasia.net:40404/api/info/get_myinfo", headers=self.headers, data=data).json()
		assert json_resp["ret_cd"] == 0, "Cannot login, invalid credential"
		self.user_cd = json_resp["user_cd"]
		self.total_earn = json_resp["total_earn"]
		self.isLogged = True
		return json_resp

	def redeemTrueMoney(self, phone_number, amount):
		# Not sure if udid can be randomized. if it doesn't (which it's supposed to be), try to create a class with adid defined
		#
		# 10 digits phone number, example: 09XXXXXXXX
		#
		assert amount in [300, 500, 1000], "Invalid amount, possible values are 300, 500, 1000"
		t = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
		json_data = {
			"type": "truemoney",
			"id": self.email,
			"amount": str(amount),
			"point": "3600" if amount == 300 else "5500" if amount == 500 else "10000",
			"phone": phone_number,
			"action_type_cd": str(random.randint(0, 99999)), # kind of stupid but this is actually how the app works
			"ad_cd": str(random.randint(0, 7)), # this too
			"udid": self.udid,
			"t": t,
			"h": self._generate_h(t)
		}
		data = {
			"json": json.dumps(json_data, separators=(",", ":"))
		}
		json_resp = requests.post("http://th-api.fsnasia.net:40404/api/withdrawal/request_withdrawal", headers=self.headers, data=data).json()
		return json_resp

	def getAds(self):
		# REDACTED
		# due to app privacy
		pass

	def interactAd(self):
		# REDACTED
		# due to app privacy
		pass

	def exploitServer(self):
		payload1 = b"h\xfc(\x9a\xa4\xdf9\x00f\xe4\xe6\xb8~\xb2\x9e\xc1"
		payload2 = b"\xacT\xf3\x80\xear>g\x19\x1fX&f+M\x80"
		payload3 = b"\xc5R\xf8U\xf5\x94J\xa4\xe1\xd1q-\xcc\xc9\xca\x04\xf0\xda\x0b%\x8d\xb3\x9c-\xdd;UPJ\xf4\xc6["
		cipher = AES.new(payload1, AES.MODE_CBC, payload2)
		d = cipher.decrypt(payload3)
		d = d[:-d[-1]]
		print(d.decode())
