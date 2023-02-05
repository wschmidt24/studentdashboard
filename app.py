from flask import Flask, render_template, request, redirect
from time import sleep
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime


def get_data(nuid, passworddd):
    headless_option = Options()
    headless_option.add_argument("--headless")
    headless_option.add_argument("--disable-gpu")
    headless_option.add_argument("--no-sandbox")
    headless_option.add_argument("--allow-insecure-localhost")
    browser = webdriver.Chrome(options=headless_option)
    browser.get("https://myred.nebraska.edu")
    while (browser.title != "MyRED | University of Nebraska-Lincoln"):
        if browser.title == "MyRED":
            try:
                browser.switch_to.frame('content')
                browser.find_element(by=By.XPATH, value='//*[@id="login-nuid"]').click()
            except:
                print("MyRED Login Button not found")
        if browser.title == "University of Nebraska & State College Single Sign On":
            username = browser.find_element(by=By.XPATH, value='//*[@id="username"]')
            username.send_keys(nuid)
            password = browser.find_element(by=By.XPATH, value='//*[@id="password"]')
            password.send_keys(passworddd)
            login_button = browser.find_element(by=By.XPATH, value='//*[@id="content-wrap"]/div/section[4]/div/div/form/div/button')
            login_button.click()
        if browser.title == "Universal Prompt":
            os.system('clear')
            try:
                browser.find_element(by=By.XPATH, value='//*[@id="trust-browser-button"]').click()
            except:
                print("Waiting for authenicator...")
                sleep(.5)

    account_balance = None
    due_date = None
    due_now = None
    while (account_balance == None or due_date == None or due_now == None):
        try:
            account_balance_strings = browser.find_element(by=By.XPATH, value='//*[@id="student.hiobx.haccbal"]/div/strong').text.split(' ')
            account_balance = float(account_balance_strings[1])
        except:
            account_balance = None
        try:
            due_date = browser.find_element(by=By.XPATH, value='//*[@id="student.hiobx.hiobxpc"]/div[1]/table/tbody/tr[2]/td').text
        except:
            due_date = None
        try:
            due_now_strings = browser.find_element(by=By.XPATH, value='//*[@id="student.hiobx.hiobxpc"]/div[2]/strong').text.split(' ')
            due_now = float(due_now_strings[1])
        except:
            due_now = None

    while (browser.title != 'Home | University Housing Portal'):
        try:
            browser.get(
                'https://myred.nebraska.edu/psc/myred/NBL/HRMS/s/WEBLIB_NBA_SSO.ISCRIPT1.FieldFormula.IScript_Login?institution=NEUNL&setupid=STARREZUNL')
        except:
            print("Accessing UNL housing...")
            sleep(.1)
    while (browser.title == 'Home | University Housing Portal'):
        try:
            href = browser.find_element(by=By.XPATH, value='/html/body/div[1]/section[1]/div/article/div/div/div/section/div[1]/div[8]/div[2]/div/div/a')
            link = href.get_attribute('href')
            browser.get(link)
        except:
            sleep(.5)
            print("Accecssing meal plan information...")

    meal_swipes_period = None
    dining_dollars = None
    herbies_gc_balance = None
    meal_plan = None
    while (meal_swipes_period == None or dining_dollars == None or herbies_gc_balance == None or meal_plan == None):
        try:
            meal_swipes_period = int(
                browser.find_element(by=By.XPATH, value='/html/body/main/div[2]/form/strong[2]').text)
        except:
            meal_swipes_period = None
        try:
            dining_dollars = float(
                browser.find_element(by=By.XPATH, value='/html/body/main/div[2]/form/strong[5]').text)
        except:
            dining_dollars = None
        try:
            herbies_gc_balance = float(
                browser.find_element(by=By.XPATH, value='/html/body/main/div[2]/form/strong[6]').text)
        except:
            herbies_gc_balance = None
        try:
            meal_plan = browser.find_element(by=By.XPATH, value='/html/body/main/div[2]/form/strong[7]').text
        except:
            meal_plan = None

        browser.get("https://canvas.unl.edu/")
        sleep(1)
        username = browser.find_element(by=By.XPATH, value='//*[@id="username"]')
        username.send_keys(nuid)
        password = browser.find_element(by=By.XPATH, value='//*[@id="password"]')
        password.send_keys(passworddd)
        login_button = browser.find_element(by=By.XPATH, value='//*[@id="login-main"]/form/div/button')
        login_button.click()

        while (browser.title != "Dashboard"):
            try:
                browser.find_element(by=By.XPATH, value='//*[@id="trust-browser-button"]').click()
            except:
                sleep(.1)
                if browser.title == "Universal Prompt":
                    os.system('clear')
                    print("Waiting for authenicator...")

        time.sleep(5)
        text_todo = browser.find_element(by=By.CLASS_NAME, value="Sidebar__TodoListContainer").text
        aa = text_todo.split("\n")
        all_text_list_todo = []
        assignments_list = []
        for item in aa:
            all_text_list_todo.append(item)
        for i in range(1, len(all_text_list_todo), 4):
            assignments_list.append(all_text_list_todo[i:i + 3])

        browser.find_element(by=By.XPATH, value='//*[@id="right-side"]/div[3]/a').click()
        time.sleep(6)
        text_classes = browser.find_element(By.TAG_NAME, "body").text
        all_text_classes = text_classes.split("\n")
        list_all_text = []
        all_classes = []
        for item in all_text_classes:
            list_all_text.append(item)

        for x in list_all_text:
            if x[-1] == "%":
                all_classes.append(x)

        current_classes = []

        for x in all_classes:
            if int(x.split()[-2]) == 2023:
                current_classes.append(x)

    return account_balance, due_now, meal_swipes_period, dining_dollars, herbies_gc_balance, current_classes, assignments_list


def validate(my_username, my_password):
    headless_option = Options()
    headless_option.add_argument("--headless")
    headless_option.add_argument("--disable-gpu")
    headless_option.add_argument("--no-sandbox")
    headless_option.add_argument("--allow-insecure-localhost")
    browser = webdriver.Chrome(options=headless_option)
    browser.get("https://trueyou.nebraska.edu/")
    browser.find_element(by=By.CSS_SELECTOR, value= 'body > div.off-canvas-content > div.desktop-header.sticky-container > header > div.menu-primary-nav > div > div.columns.small-6.column-right.logged-out > div > div.columns.shrink > a').click()
    browser.find_element(by=By.XPATH, value = '//*[@id="content-wrap"]/div/section[2]/div/div/div[1]/a').click()
    username = browser.find_element(by=By.XPATH, value='//*[@id="username"]')
    username.send_keys(my_username)
    password = browser.find_element(by=By.XPATH, value='//*[@id="password"]')
    password.send_keys(my_password)
    login_button = browser.find_element(by=By.XPATH, value='//*[@id="content-wrap"]/div/section[4]/div/div/form/div/button')
    login_button.click()
    try:
        if browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/section[3]/div/div/div/span').text == 'Invalid credentials.':
            return False
    except:
        if browser.title != 'University of Nebraska & State College Single Sign On':
            return True
        else:
            print("Inconclusive validation")
            return False


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("main.html")


@app.route('/dashboard', methods=['POST'])
def index():
    nuid = request.form['nuid']
    print(nuid)
    password = request.form['password']
    if validate(nuid, password) == False:
        return redirect('/')
    account_balance, due_now, meal_swipes_period, dining_dollars, herbies_gc_balance, current_classes, temp_to_do_list = get_data(nuid, password)
    grades = {} # {class : grade}
    for string in current_classes:
        a = string.split()
        percent = a[-1]
        x = ""
        [x := x + str + " " for str in a[:-1]]
        grades[x] = percent

    today = datetime.date.today()
    future = datetime.date(2023, 5, 10)
    difference = future - today
    per_day = dining_dollars / int(difference.days)
    to_do_list = []
    for x in temp_to_do_list:
        temp = []
        temp.append(x[0:2])
        temp.append(x[-1].split("s"))
        to_do_list.append(temp)
    return render_template("index.html", classes=grades.keys(), grades=grades, to_do=to_do_list[:-1],
                           account_balance=format(account_balance, ".2f"), due_now=format(due_now, ".2f"), meal_swipes_period=meal_swipes_period, dining_dollars=format(dining_dollars, ".2f"), herbies_gc_balance=format(herbies_gc_balance, ".2f"), per_day=format(per_day, ".2f"))


if __name__ == '__main__':
    app.run()
