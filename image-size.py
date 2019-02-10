import base64
import json
import requests

raw_bytes = open('imgs/clipper-logo.png', "rb").read()
raw_bytes[:10]

encoded_bytes = base64.b64encode(raw_bytes)
print(type(encoded_bytes))
encoded_bytes[:10]

encoded_string = encoded_bytes.decode()
print(type(encoded_string))
encoded_string[:10]

def query(addr, filename):
    print('addr:' + addr)
    url = "http://%s/image-example/predict" % addr
    print('url:' + url)
    req_json = json.dumps({
        "input":
        base64.b64encode(open(filename, "rb").read()).decode() # bytes to unicode
    })
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, headers=headers, data=req_json)
    print('output:')
    print(r.json())


def image_size(imgs):
    """
    Input:
    - imgs : (np.ndarray) of shape (n, d). n is the number of data in this batch
             d is the length of the bytes as numpy int8 array.
    Output:
    - sizes : List[Tuple(int, int),...]
    """
    import base64
    import io
    import os
    import PIL.Image
    import tempfile

    num_imgs = len(imgs)
    sizes = []
    for i in range(num_imgs):
        # Create a temp file to write to
        tmp = tempfile.NamedTemporaryFile('wb', delete=False, suffix='.png')
        tmp.write(io.BytesIO(imgs[i]).getvalue())
        tmp.close()

        # Use PIL to read in the file and compute size
        size = PIL.Image.open(tmp.name, 'r').size

        # Remove the temp file
        os.unlink(tmp.name)

        sizes.append(size)
    return sizes


from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.deployers import python as python_deployer

clipper_conn = ClipperConnection(DockerContainerManager())
clipper_conn.start_clipper()


python_deployer.create_endpoint(
    clipper_conn=clipper_conn,
    name="image-size",
    input_type="bytes",
    func=image_size,
    pkgs_to_install=['pillow']
)

print('clipper_conn.get_query_addr()' + clipper_conn.get_query_addr())

# To test
# query(clipper_conn.get_query_addr(), 'imgs/clipper-logo.png')



