import requests
import time
import csv

API_KEY = "INSERT YOUR API_KEY"

PAGE_SIZE = 50
CHAIN = "ethereum"

# Stores retrieved NFTs to all_nfts.csv file.
def store_nfts(nfts, page_nr):
    if page_nr == 1:
        # Open file & write headers
        with open('all_nfts.csv', 'a', encoding='UTF8') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(["chain", "token_id", "metadata", "metadata_url", "file_url", "animation_url",
                        "cached_file_url", "cached_animation_url", "mint_date", "file_information", "updated_date"])
   
    # Open file & write headers
    for nft in nfts:
        with open('all_nfts.csv', 'a', encoding='UTF8') as myfile:
            wr = csv.writer(myfile)
            wr.writerows([[str(nft["chain"]),
                            str(nft["token_id"]),
                            str(nft["metadata"]),
                            nft["metadata_url"],
                            nft["file_url"],
                            nft["animation_url"],
                            nft["cached_file_url"],
                            nft["cached_animation_url"],
                            str(nft["mint_date"]),
                            str(nft["file_information"]),
                            str(nft["updated_date"])]])


def make_request(continuation):
    url = "https://api.nftport.xyz/v0/nfts"

    headers = {
        'Content-Type': "application/json",
        'Authorization': API_KEY
    }

    if continuation:
        querystring = {"chain":CHAIN, "continuation":continuation, "page_size":PAGE_SIZE, "include":"all"}
    else:
        querystring = {"chain":CHAIN, "page_size":PAGE_SIZE, "include":"all"}

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    return response


def get_all_nfts():
    page_nr = 1
    
    # Initial request
    print("Getting NFTs for page " + str(page_nr) + " with a page size of " + str(PAGE_SIZE))
    query_response = make_request(None)

    if query_response["response"] == "OK":
        nfts = query_response["nfts"]
        store_nfts(nfts, page_nr)
        continuation = query_response["continuation"]
        page_nr = page_nr + 1
    else:
        print(query_response["error"])

    # Paging limited to page_nr > 10, remove or increase pages. If removed script stores NFTs until error message or script stopped.
    while not any([page_nr > 10, continuation == "null", continuation == None]):
        time.sleep(1)
        print("Getting NFTs for page " + str(page_nr) + " with a page size of " + str(PAGE_SIZE))

        query_response = make_request(continuation)

        if query_response["response"] == "OK":
            nfts = query_response["nfts"]
            store_nfts(nfts, page_nr)
            continuation = query_response["continuation"]
            page_nr = page_nr + 1
        else:
            print(query_response["error"])

    print("Finished getting NFTs. Total pages: " + str(page_nr-1) + " & total NFTs: " + str((page_nr-1)*PAGE_SIZE))

def main():
    get_all_nfts()

if __name__ == '__main__':
    main()
