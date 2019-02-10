from clipper_admin import ClipperConnection, DockerContainerManager

clipper_conn = ClipperConnection(DockerContainerManager())

clipper_conn.start_clipper()



clipper_conn.register_application(name="hello-from-gonnect", input_type="doubles", default_output="-1.0", slo_micros=100000)


print(clipper_conn.get_all_apps())

import requests, json, numpy as np
headers = {"Content-type": "application/json"}
requests.post("http://localhost:1337/hello-from-gonnect/predict", headers=headers, data=json.dumps({"input": list(np.random.random(10))})).json()


clipper_conn.stop_all()