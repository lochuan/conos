import time
import random
from hashlib import sha1
import hmac
import base64
import binascii

def cos_multi_signature():
	appid="1253694121"
	bucket="conos"
	secret_id="AKIDPiKsNkZX2Ws20mEktzzoSxjRxPL55z98"
	secret_key="3jGg6MQURDoMjuQvPgqtomhQ2SgjaG2l"
	expired=str(int(time.time()) + 60)
	onceExpired="0"
	rdm=str(random.randrange(1000,9999999999))
	current=str(int(time.time()))

	multi_effect_string = 'a='+appid+'&b='+bucket+'&k='+secret_id+'&e='+expired+'&t='+current+'&r='+rdm+'&f='
	multi_effect_string_utf = multi_effect_string.encode('ascii')
	sha1_hmac = hmac.new(bytes(secret_key, 'ascii'), multi_effect_string_utf, sha1)
	hmac_digest = sha1_hmac.hexdigest()
	hmac_digest = binascii.unhexlify(hmac_digest)
	sign_hex = hmac_digest + multi_effect_string_utf
	sign = base64.b64encode(sign_hex)
	sign = sign.decode('ascii')
	return sign

def cos_single_signature(filename):
	appid="1253694121"
	bucket="conos"
	secret_id="AKIDPiKsNkZX2Ws20mEktzzoSxjRxPL55z98"
	secret_key="3jGg6MQURDoMjuQvPgqtomhQ2SgjaG2l"
	expired=str(int(time.time()) + 60)
	onceExpired="0"
	rdm=str(random.randrange(1000,9999999999))
	current=str(int(time.time()))

	single_effect_string = 'a='+appid+'&b='+bucket+'&k='+secret_id+'&e='+onceExpired+'&t='+current+'&r='+rdm+'&f='+filename
	single_effect_string_utf = single_effect_string.encode('ascii')
	sha1_hmac = hmac.new(bytes(secret_key, 'ascii'), single_effect_string_utf, sha1)
	hmac_digest = sha1_hmac.hexdigest()
	hmac_digest = binascii.unhexlify(hmac_digest)
	sign_hex = hmac_digest + single_effect_string_utf
	sign = base64.b64encode(sign_hex)
	sign = sign.decode('ascii')
	return sign
