from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import os
import json

breed_to_image_uri = {
    "PUG": "https://gateway.pinata.cloud/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8",
    "SHIBA_INU": "https://gateway.pinata.cloud/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU",
    "ST_BERNARD": "https://gateway.pinata.cloud/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW",
}

tokenId_to_metadata_uri = {
    0: "https://ipfs.io/ipfs/QmWmvZshhqQWyudm2ZvFcTPTR8B5EkU7GBgcXwJsBY4hEZ?filename=0-SHIBA_INU.json",
    1: "https://ipfs.io/ipfs/QmUCgM3DjUe9urt2EMBX3P9LZbbMSmDCeKr6fJGV8tGEfq?filename=1-ST_BERNARD.json",
    2: "https://ipfs.io/ipfs/QmUCgM3DjUe9urt2EMBX3P9LZbbMSmDCeKr6fJGV8tGEfq?filename=2-ST_BERNARD.json",
    3: "https://ipfs.io/ipfs/QmUCgM3DjUe9urt2EMBX3P9LZbbMSmDCeKr6fJGV8tGEfq?filename=3-ST_BERNARD.json",
    4: "https://ipfs.io/ipfs/QmUCgM3DjUe9urt2EMBX3P9LZbbMSmDCeKr6fJGV8tGEfq?filename=4-ST_BERNARD.json",
    5: "https://ipfs.io/ipfs/QmWmvZshhqQWyudm2ZvFcTPTR8B5EkU7GBgcXwJsBY4hEZ?filename=5-SHIBA_INU.json",
    6: "https://ipfs.io/ipfs/QmZM6R1GiABCikdyVwuEpBRPLQFSuojDEYe29dUT4AcAGw?filename=6-PUG.json",
    7: "https://ipfs.io/ipfs/QmZM6R1GiABCikdyVwuEpBRPLQFSuojDEYe29dUT4AcAGw?filename=7-PUG.json",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite.")
        else:
            print(f"Creating metadata file: {metadata_file_name}.")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs_pinata(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                metadata_uri = upload_to_ipfs_pinata(metadata_file_name)
            metadata_uri = (
                metadata_uri if metadata_uri else tokenId_to_metadata_uri[token_id]
            )


def upload_to_ipfs(filepath):
    # opening image files in python, we need the key "rb" in the .open function,
    # since images are binaries
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # run ipfs daemon before in the command line to start the local hosted server
        # the ipfs_url will be displayed at the end of the output under "WebUI:"
        ipfs_url = "http://127.0.0.1:5001"
        # get the endpoint from https://docs.ipfs.io/reference/http/api/#api-v0-add
        end_point = "/api/v0/add"
        response = requests.post(ipfs_url + end_point, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


def upload_to_ipfs_pinata(filepath):
    PINATA_BASE_URL = "https://api.pinata.cloud/"
    endpoint = "pinning/pinFileToIPFS"
    filename = filepath.split("/")[-1:][0]
    print(filename)
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET_KEY"),
    }

    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        ipfs_hash = response.json()["IpfsHash"]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
