import requests
import time
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool


def get_num(thread_name):

    print(thread_name, "***启动-->")

    url = "http://api.fxhyd.cn/UserInterface.aspx"
    project = "11610"  # 西瓜11610 猫眼11075
    token = "003276475a7f625c4020a89ddc5021fb805433c6"

    params_getmobile = {
        "action": "getmobile",
        "token": token,
        "itemid": project,
        "excludeno": "170|171",
    }

    while True:
        while True:
            try:
                r = requests.get(url, params=params_getmobile, timeout=10)
                break
            except Exception as e:
                print(e)
                pass

        content = r.text

        if "success|" in content:
            number = content.replace("success|", "")
            print("获得号码：", number)
            break
        else:
            print("获得号码失败：", content)
            pass

    flag = None

    params_getsms = {
        "action": "getsms",
        "token": token,
        "itemid": project,
        "mobile": number,
        "release": "1",
    }

    i = 1
    while i<=12:

        while True:
            try:
                r = requests.get(url, params=params_getsms, timeout=10)
                break
            except Exception as e:
                print(e)
                pass

        content = r.text
        # print("第%d次请求->" % i)
        if content == "3001":
            # print("短信尚未到达, 代码:", content)
            i += 1
            time.sleep(5)
        elif "success|" in content:
            flag = number
            print("短信接收成功:", number, content)
            break
        else:
            print("短信请求异常:", content)
            break

    params_release = {
        "action": "release",
        "token": token,
        "itemid": project,
        "mobile": number,
        "release": "1",
    }

    while True:
        try:
            r = requests.get(url, params=params_release, timeout=10)
            print(r.text, "释放！")
            break
        except Exception as e:
            print(e)
            pass

    return flag


if __name__ == '__main__':

    while True:
        aysn_num = 5

        thread_names = [i for i in range(1, aysn_num+1)]
        pool = ThreadPool(aysn_num)
        lis = pool.map(get_num, thread_names)
        pool.close()
        pool.join()
        if len(set(lis)) != 1:
            break
