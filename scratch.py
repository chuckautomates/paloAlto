import device
import base
from importlib import reload
from xml.etree import ElementTree as ET

fw1Data = {'username': 'admin', 'password': 'boops', 'basePath': '192.168.1.222', 'sslVerify': False}


fw1 = device.DeviceController(**fw1Data)
fw1.deviceSaveBackup()
response = fw1.deviceExportBackup()

responseId = fw1.deviceDownloadContentUpdate()

boop = fw1.deviceJobStatus(responseId)

boop = fw1.deviceDownloadLatestContentUpdate()


boop = fw1.deviceJobStatus(28)



fw1 = base.Base(**fw1Data)

headers = fw1.headers()

print(headers)

fw1.generate_token(False)






tree = ET.XML(boop.text)
ET.dump(tree)
jobId = tree[0][1].text
