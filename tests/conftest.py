import os
import pytest
from selenium import webdriver
import subprocess
import socket
import requests
import time

DRIVERS = os.path.expanduser("~\\Downloads\\drivers")
path_to_opencart_yml = os.path.expanduser("~\\proj\\opencart\\")
path_to_selenoid = os.path.expanduser("~\\proj\\selenoid\\")
# port vars for exec with docker
cart_port = 8081
php_admin_port = 8888


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", choices=["chrome", "firefox", "opera"])
    parser.addoption("--url", action="store", default="")
    parser.addoption("--selenoid_ip", action="store", default=None)
    parser.addoption("--bversion", action="store", default=None)
    parser.addoption("--vnc", action="store_true", default=True)
    parser.addoption("--selenoid_logs", action="store_true", default=False)
    parser.addoption("--videos", action="store_true", default=False)


@pytest.fixture(scope="session")
def url(request):
    def clear_containers():
        subprocess.run("FOR /f \"tokens=*\" %i IN ('docker ps -q') DO docker stop %i", shell=True)
        subprocess.run("docker container prune -f & docker volume prune -f & docker network prune -f", shell=True)

    request.addfinalizer(clear_containers)

    if request.config.getoption("--url"):
        return request.config.getoption("--url")
    else:
        host_ip = socket.gethostbyname(socket.gethostname())
        os.environ['OPENCART_PORT'] = str(cart_port)
        os.environ['PHPADMIN_PORT'] = str(php_admin_port)
        os.environ['LOCAL_IP'] = str(host_ip)
        subprocess.run(f"cd {path_to_opencart_yml} & docker-compose up -d", shell=True)
        opencart_url = f"http://{host_ip}:{cart_port}/"

        # wait when docker finally loading
        for i in range(30):
            try:
                requests.get(opencart_url).status_code == 200
                return opencart_url
            except requests.ConnectionError:
                time.sleep(1)
        raise EnvironmentError("Что-то случилось с докером. Не могу подключиться!")


@pytest.fixture(scope="session")
def selenoid_handler(request):
    _browser = request.config.getoption("--browser")
    bversion = request.config.getoption("--bversion")
    selenoid_ip = request.config.getoption("--selenoid_ip")
    vnc = request.config.getoption("--vnc")
    sel_logs = request.config.getoption("--selenoid_logs")
    videos = request.config.getoption("--videos")
    if selenoid_ip:
        subprocess.run(f"cd {path_to_selenoid} & cm selenoid start --args \"-limit=12\" & cm selenoid-ui start",
                       shell=True)
        # get available versions for browser in docker
        list_avail_bvers = subprocess.getoutput(f"docker images --format {{{{.Tag}}}} selenoid/{_browser}").split('\n')
        if bversion and bversion not in list_avail_bvers:
            raise ValueError(
                f"{bversion} версия не найдена для браузера {_browser}. Доступны следующие версии: {list_avail_bvers} ")
        if not bversion:
            # если параметром не передана версия браузера - берем последнюю
            bversion = list_avail_bvers[0]
        return {"vnc": vnc, "sel_logs": sel_logs, "videos": videos, "selenoid_ip": selenoid_ip, "bversion": bversion}
    else:
        return None


@pytest.fixture
def browser(request, selenoid_handler):
    _browser = request.config.getoption("--browser")

    if selenoid_handler:
        caps = {
            "browserName": _browser,
            "browserVersion": selenoid_handler["bversion"],
            "screenResolution": "1280x1024",
            "name": "selenoid test run",
            "selenoid:options": {
                "sessionTimeout": "20s",
                "enableVNC": selenoid_handler["vnc"],
                "enableVideo": selenoid_handler["videos"],
                "enableLog": selenoid_handler["sel_logs"]
            }
        }
        driver = webdriver.Remote(
            command_executor=f"http://{selenoid_handler['selenoid_ip']}:4444/wd/hub",
            desired_capabilities=caps
        )
    else:
        if _browser == "chrome":
            driver = webdriver.Chrome(executable_path=f"{DRIVERS}\\chromedriver.exe")
        elif _browser == "opera":
            driver = webdriver.Opera(executable_path=f"{DRIVERS}\\operadriver.exe")
        elif _browser == "firefox":
            driver = webdriver.Firefox(executable_path=f"{DRIVERS}\\geckodriver.exe")
        request.addfinalizer(driver.quit)
    return driver
