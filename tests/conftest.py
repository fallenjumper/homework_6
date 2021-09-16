import os
import pytest
from selenium import webdriver
import subprocess
import socket
import requests
import time

DRIVERS = os.path.expanduser("~\\Downloads\\drivers")
path_to_opencart_yml = os.path.expanduser("~\\proj\\opencart\\")
# port vars for exec with docker
cart_port = 8081
php_admin_port = 8888


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", choices=["chrome", "firefox", "opera"])
    parser.addoption("--url", action="store", default="")


@pytest.fixture(scope="session")
def url(request):
    def clear_containers():
        subprocess.run("FOR /f \"tokens=*\" %i IN ('docker ps -q') DO docker stop %i", shell=True)
        subprocess.run("docker container prune -f & docker volume prune -f & docker network prune -f", shell=True)

    if request.config.getoption("--url"):
        return request.config.getoption("--url")
    else:
        host_ip = socket.gethostbyname(socket.gethostname())
        os.environ['OPENCART_PORT'] = str(cart_port)
        os.environ['PHPADMIN_PORT'] = str(php_admin_port)
        os.environ['LOCAL_IP'] = str(host_ip)
        subprocess.run(f"cd {path_to_opencart_yml} & docker-compose up -d", shell=True)
        opencart_url = f"http://{host_ip}:{cart_port}/"
        request.addfinalizer(clear_containers)
        # wait when docker finally loading
        for i in range(30):
            try:
                requests.get(opencart_url).status_code == 200
                return opencart_url
            except requests.ConnectionError:
                time.sleep(1)
        raise EnvironmentError("Что-то случилось с докером. Не могу подключиться!")


@pytest.fixture
def browser(request):
    _browser = request.config.getoption("--browser")

    if _browser == "chrome":
        driver = webdriver.Chrome(executable_path=f"{DRIVERS}\\chromedriver.exe")
    elif _browser == "opera":
        driver = webdriver.Opera(executable_path=f"{DRIVERS}\\operadriver.exe")
    elif _browser == "firefox":
        driver = webdriver.Firefox(executable_path=f"{DRIVERS}\\geckodriver.exe")

    request.addfinalizer(driver.quit)
    return driver
