import requests

def add_file_to_ipfs(file_path):
    url = "http://127.0.0.1:5001/api/v0/add"
    with open("test.txt", "rb") as file:
        files = {"file":file}
        response = requests.post(url, files=files)

        if response.status_code == 200: 
            try: 
                cid = response.json()["Hash"]
                print(f"File uploaded to IPFS. CID: {cid}")
                return cid
            except:
                print("Error parsing the JSON response.")
                print("Response text:", response.txt)
                return None
        else:
            print("Error uploading file.")
            print("Status Code:", response.status_code)
            print("Response text:", response.text)
            return None
        
file_path = "test.txt"
add_file_to_ipfs(file_path)

def save_cid_to_file(cid):
    with open("cid_storage.txt", "a")as file:
        file.write(f"{cid}\n")

cid = add_file_to_ipfs(file_path)

if cid:
    save_cid_to_file(cid)
    print(f"CID {cid} saved to file.")
else:
    print("No CID to save.")


