import requests
from colorama import init,Fore
init(True)
import threading
Lock = threading.Lock()
def Dofilter(link):
    if "/" in link:
        deflink = link
        ssl = link.split("//")[0]
        sitename = link.split("/")[2]
        link = f"{ssl}//{sitename}"
    else:
        link = f"http://{link}"
    try:
        session = requests.Session()
        session.headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44"
        res = session.get(link,headers=session.headers)
        statuscode = res.status_code
        if statuscode==200:
            if "shopify" in res.text:
                with Lock:
                    print(f"{Fore.RED}[SHOPIFY] {link}")
                    f = open("Links[shopify].txt","a")
                    f.write(f"{deflink}\n")
                    f.close()
            else:
                with Lock:
                    print(f"{Fore.LIGHTGREEN_EX}[+] {link}")
                    f = open(f"Links[Non-Shopify].txt","a")
                    f.write(f"{deflink}\n")
                    f.close()
        elif statuscode!=200:
            with Lock:
                    print(f"{Fore.RED}[status code: {statuscode}] {link}")
                    f = open(f"Links[{statuscode}].txt","a")
                    f.write(f"{deflink}\n")
                    f.close()
    except Exception as e:
        with Lock:
            print(f"{Fore.RED}[-] Error -> {link}")
            f = open(f"Links[Errors].txt","a")
            f.write(f"{deflink}\n")
            f.close()

goodlst = []
threadlst = []
f = open("urls.txt").readlines()
for line in f:
    goodlst.append(line.split("\n")[0])

if __name__ == "__main__":
    for link in goodlst:
        thread = threading.Thread(target=Dofilter,args=(link,))
        thread.start()
        threadlst.append(thread)
    for current in threadlst:
        current.join()

    input()
