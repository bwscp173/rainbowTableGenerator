import json
import hashlib
import os
import time

def getChoice(options: list[str]) -> int:
    """given a list of options, the user will give the index
    of the option that they want to select"""
    running = True
    toDisplay=""
    for i in range(len(options)):
        toDisplay += f"\n{i+1}) {options[i]}"
    while running:
        print(f"\nwhich hashing algorithm should be used: {toDisplay}")

        try:
            choice = int(input(">> "))
            if choice == -55:
                exit(-55)
            if choice > len(options) or choice < 1:
                raise Exception(f"invalid option: must be between {len(options)}-1")
            return choice
        except Exception as e:
            print(e)
            print("type -55 to quit")

options = [
    "hashlib.sha1",
    "hashlib.sha224",
    "hashlib.sha256",
    "hashlib.sha384",
    "hashlib.sha512",
    "hashlib.sha3_256",
    "hashlib.sha3_224",
    "hashlib.sha3_384",
    "hashlib.sha3_512",
    "hashlib.md5"
]

def readFromFile(fileName:str) -> list[str]:
    contense = []

    if not os.path.isfile(fileName):
        raise Exception("invalid file: file given does not exist")

    with open(fileName,"r", errors="ignore") as f:
        contense = f.read().split("\n")

    return contense

def computeRainbowTable(wordlist: list[str], option: int, salt:str="", appendSalt:bool=True) -> dict[str:str]:
    """
    appendSalt can be true for appending, and false for prepending"""
    rainbowTable={}
    theHash:hashlib.HASH

    for i in range(len(wordlist)):
        match option:
            case 1:
                theHash = hashlib.sha1()
            case 2:
                theHash = hashlib.sha224()
            case 3:
                theHash = hashlib.sha256()
            case 4:
                theHash = hashlib.sha384()
            case 5:
                theHash = hashlib.sha512()
            case 6:
                theHash = hashlib.md5()
            case 7:
                theHash = hashlib.sha3_224()
            case 8:
                theHash = hashlib.sha3_384()
            case 9:
                theHash = hashlib.sha3_512()
            case 10:
                theHash = hashlib.md5()
            case _:
                raise Exception("invalid option given")

        if appendSalt:
            toHash = (wordlist[i] + salt).strip()
        else:
            toHash = (salt + wordlist[i]).strip()

        theHash.update(toHash.encode())
        rainbowTable[theHash.hexdigest()] = wordlist[i]

    return rainbowTable
        
def writeRainbowTable(fileName:str, rainbowTable:dict) -> None:
    """writes the rainbowTable to the given fileName"""
    with open(fileName,"w") as f:
        f.write(json.dumps(rainbowTable,indent=4))

def save_x_lines(fileName:str, lines:int) -> list[str]:
    """inefficient as hell, i just needed to save x many lines from rockyou
    the file it saves to is hardcoded"""
    a = readFromFile(fileName)[:lines]
    with open("10mil.txt","w") as f:
        f.write('\n'.join(a))

def lookUpHash(fileName:str, hash:str) -> str:
    """reads from the json file and finds the hash, returns the value"""
    if not os.path.isfile(fileName):
        raise Exception("invalid file: file given does not exist")
    
    with open(fileName) as json_file:
        rainbowTable = json.load(json_file)

    return rainbowTable[hash]

def lookUpHashes(fileName:str, hashes:list[str]) -> str:
    """reads from the json file and finds the hash, returns the value"""
    if not os.path.isfile(fileName):
        raise Exception("invalid file: file given does not exist")
    
    time1 = time.time()
    with open(fileName) as json_file:
        rainbowTable = json.load(json_file)
    time2 = time.time()
    print("time to load is:" , time2-time1)

    return [rainbowTable[hash] for hash in hashes]

if __name__ == "__main__":

    hashChoice:int = getChoice(options)
    wordList = readFromFile("1mil.txt")
    time1 = time.time()
    hashes = computeRainbowTable(wordList,hashChoice)
    time2 = time.time()
    print("time to calc: " + str(time2 - time1))


    time1 = time.time()
    writeRainbowTable("results.json",hashes)
    time2 = time.time()
    print("time to write: " + str(time2 - time1))

    input("pausing")

    time1 = time.time()
    #where resultsSmoll.json are md5 keys
    print("password is: ", lookUpHashes("resultsSmoll.json",["263fec58861449aacc1c328a4aff64aff4c62df4a2d50b3f207fa89b6e242c9aa778e7a8baeffef85b6ca6d2e7dc16ff0a760d59c13c238f6bcdc32f8ce9cc62","547e4dcff44f953e4aef595d0562af9f8394c6b6b1f6f1678d29806cfb6659e973785dc2054cbac9f1ffdc7ddb8e4bdd02a3760d05346a567cc7f8dce8c74709","690437692d902cfd23005bda16631d83644899e78dc0a489da6dca3cb9f9c0cdcd9dd533bc59102dc90155223df777672328c9149354de239f48c58f0a1d44a6"]))  # some random hash near the end of the file
    time2 = time.time()


    # time1 = time.time()
    # print("password is: ", lookUpHashes("results.json",["5df96e9d8177d088819c2483a1470ddc","443521dab57488e8601a27945d13b330","6a2f64db9fe58b0cc075b9e865a66857","bab42885007b841dc35c99b11a8e8e57","d348760015ff852d6535a111701bf953"]))  # some random hash near the end of the file
    # time2 = time.time()
    # print("total time searching + loading: " + str(time2 - time1))

    # time1 = time.time()
    # print("password is: ", lookUpHashes("results.json",["5df96e9d8177d088819c2483a1470ddc"]))  # some random hash near the end of the file
    # time2 = time.time()
    # print("total time searching + loading: " + str(time2 - time1))