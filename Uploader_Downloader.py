#import required l3ibraries
from pytube import YouTube
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request
import time
from zipfile import ZipFile
import shutil

#decision
def choice():
    
    choice = input("Would you like to upload or download? ")
    if choice == "upload":
        print("Accessing Github...")
        github()
    elif choice == "download":
        choice_2 = input("Would you like to download \n Images, Videos or Music or Subtitles \n")
        if choice_2 == "videos":
            videos()
        elif choice_2 == "music":
            music()
        elif choice_2 == "images":
            image()
        elif choice_2 == "subtitles":
            subtitles()
            
#Upload -Section
def github():
    
    driver = webdriver.Chrome(executable_path = "E:/project/Downloader/chromedriver")
    try:
        github = driver.get("https://github.com/login")
        user_name = input("Enter your username: ")
        password = input("Enter password: ")
        driver.find_element_by_name("login").send_keys(user_name)
        time.sleep(1)
        driver.find_element_by_name("password").send_keys(password)
        time.sleep(1)
        driver.find_element_by_name("commit").click()
        time.sleep(1)
        if driver.title == "Sign in to GitHub · GitHub":
            print("Your credentials are wrong try again")
        else:
            if driver.title == "GitHub · Where software is built":
                otp = int(input("Enter otp you just recieved: "))
                driver.find_element_by_id("otp").send_keys(otp)
                driver.find_element_by_xpath("//*[@id='login']/div[3]/form/button").click()
            print("You have been successfully logged in")
            time.sleep(5)
            rep = driver.find_element_by_link_text("New")
            time.sleep(1)
            rep.click()
            repository_name = input("Enter a repository name: ")
            time.sleep(1)
            driver.find_element_by_id("repository_name").send_keys(repository_name)
            description_choice = input("Would you like to provide any description to your project: ")
            if description_choice == "yes":
                description = input("Please provide the description below \n")
                driver.find_element_by_id("repository_description").send_keys(description)
            elif description_choice == "no":
                pass
            type = input("Would you like it to be public or private: ")
            if type == "public":
                driver.find_element_by_id("repository_visibility_public").click()
            elif type == "private":
                driver.find_element_by_id("repository_visibility_private").click()
                driver.find_element_by_xpath("//*[@id='new_repository']/div[3]/button").click() 
            time.sleep(3)
            title = user_name+"/"+repository_name
            if driver.title != title:
                print("Repository name has already been taken")
            else:
                driver.find_element_by_link_text("uploading an existing file").click()
                loc = input("Enter Location of the file: ")
                file_name = input("Enter filename: ")
                extention = input("Enter extention of the file: ")
                loc = loc+"\\"+file_name+extention
                if os.path.exists(loc) == True:
                    driver.find_element_by_xpath('//*[@id="upload-manifest-files-input"]').send_keys(loc)
                    time.sleep(10)
                    driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[2]/div/form/button').click()
                    if driver.current_url == "https://github.com/akd0510/Uploader_Downloaderhttps://github.com/akd0510/Uploader_Downloader":
                        print("Your file has been uploaded")
                    else:
                        print("File could not be uploaded try again...")
                else:
                    print("Such file doesn't exists please check again: ")
    except:
        print("We ran into some problem please check your connectivity")
    time.sleep(15)
    driver.close()

#Download -Section
def videos():  
    
    url = input("Enter URL for the video you need to download: ")
    res_videos = input("Enter resolution: ")
    save_path = "C:/Users/Akshay Dileep/Videos"
    videos = YouTube(url)
    streams = videos.streams.all()
    try:
        filter_videos = videos.streams.filter(res = res_videos).first()
        if filter_videos != None:
            print("Downloading video...")
            filter_videos.download(save_path)
            print("Downloaded")
            os.startfile(save_path)
        else:
            print("The requested resolution for the video isn't available would you like to try again:")
    except:
        choice = input("Error occored probably due to internet connection, would you like to try again: ")
        if choice == "yes":
            choice()
        else:
            print("")    

def music():
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--test-type")
        options.add_argument('--disable-notifications')
        driver = webdriver.Chrome(executable_path = "E:/project/Downloader/chromedriver", options=options)
    
        song_name = input("Enter song name: ")
        song_name = song_name.title()
        song_name = song_name.replace(" ","-")

        song_request = driver.get("https://mp3paw.com/mp3-download/"+song_name)
        song_query = driver.find_elements_by_class_name("mp3")
        song_details = driver.find_elements_by_tag_name("h3")
        song_duration = driver.find_elements_by_class_name("mp3-duration")
    
    
        play_button_x_path = ["//*[@id='mp3List']/div[1]/div[3]/ul/li[1]/div",
                              "//*[@id='mp3List']/div[2]/div[3]/ul/li[1]/div",
                              "//*[@id='mp3List']/div[3]/div[3]/ul/li[1]/div",
                              "//*[@id='mp3List']/div[4]/div[3]/ul/li[1]/div",
                              "//*[@id='mp3List']/div[5]/div[3]/ul/li[1]/div"]
    
        download_button_x_path = ["//*[@id='mp3List']/div[1]/div[3]/ul/li[3]/div",
                                  "//*[@id='mp3List']/div[2]/div[3]/ul/li[3]/div",
                                  "//*[@id='mp3List']/div[3]/div[3]/ul/li[3]/div",
                                  "//*[@id='mp3List']/div[4]/div[3]/ul/li[3]/div",
                                  "//*[@id='mp3List']/div[5]/div[3]/ul/li[3]/div"]
        if song_query is None:
            print("Your requested song isn't available")
        else:
            for i in range(5):
                print(str(i + 1)+".> ",song_details[i].text)
                print("duration = ",song_duration[i].text,"\n")
            index = int(input("Enter the index number of song you would like to select: "))
            index = index - 1
            choice = input("would you like to play the song or download the song: ")
            if choice == "play":
                driver.find_element_by_xpath(play_button_x_path[index]).click()
                print("Your song is being played... Hope you enjoy!")
            elif choice == "download":
                driver.find_element_by_xpath(download_button_x_path[index]).click()
                handle = driver.window_handles
                driver.switch_to.window(handle[1])
                request = requests.get(driver.current_url)
                html_page = BeautifulSoup(request.content,"html.parser")
                song_quality = html_page.findAll("div", {"class":"rate"})
                song_size = html_page.findAll("div", {"class":"foot"})
                print("Available qualities are: ")
                for i in range(6):
                    print(str(i + 1)+".>",song_quality[i].text)
                    print("size:",song_size[i + 1].text,"\n")
                quality_choice = int(input("Which one would you like to download: "))
                if quality_choice == 1:
                    driver.find_element_by_class_name("btr-320").click()
                elif quality_choice == 2:
                    driver.find_element_by_class_name("btr-256").click()
                elif quality_choice == 3:
                    driver.find_element_by_class_name("btr-192").click()
                elif quality_choice == 4:
                    driver.find_element_by_class_name("btr-128").click()
                elif quality_choice == 5:
                    driver.find_element_by_class_name("btr-64").click()
                elif quality_choice == 6:
                    driver.find_element_by_class_name("btr-32").click()
                name = driver.find_element_by_tag_name("h1").text
                print("Your song will be downloaded")
                time.sleep(120)
                name = name +".mp3"
                name = name.replace("'"," ")
                print(name)
                source = "C:\\Users\\Akshay Dileep\\Downloads\\"+ name
                destination = "E:\Music"
                shutil.move(source,destination)
                destination = destination + "\\" + name
                os.startfile(destination)
                driver.close()
                print("Your song has been downloaded and played")
                
    except:
        print("We ran into some issues please check your connectivity")
    
def image():
    
    url = input("Enter your image link: ")
    name = input("What would you like to name your file: ")
    name = name+".jpg"
    print("Your requested image will be downloaded...")
    try:
        urllib.request.urlretrieve(url,name)
    except:
        print("We ran into some problem while attempting to download please check your internet conncetivity ")
    time.sleep(15)

def subtitles():
    
    driver = webdriver.Chrome(executable_path = "E:/project/Downloader/chromedriver")
    try:
        driver.get("https://yts-subs.com/")
        name = input("Enter movie name: ")
        time.sleep(2)
        driver.find_element_by_id("qSearch").send_keys(name)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="search-movie-form"]/div/div/button').click()
        time.sleep(5)
        details = driver.find_elements_by_class_name("media-body")
        no_of_search_found = len(details)
        driver.delete_all_cookies()
        if no_of_search_found == 0:
            print("The subtitles for the requested movie couldn't be found...")
        else:    
            for i in range(no_of_search_found):
                print(str(i + 1)+".> ",details[i].text,"\n")
            click_link = int(input("Select the index number of which you would like to download: "))
            click_link = click_link - 1
            details[click_link].click()
            time.sleep(5)

#           Algorithm
#           list1 = ["hello","hii there","hello there how are you"]
#           list_2 = []
#           list3 = []
#           for i in list1:
#               list_2 =i.split()
#               for j in list_2:
#                   if j == "are":
#                       list3.append(i)
#           print(list_2)
#           print(list3)
            
            driver.delete_all_cookies()
            subtitles_1 = driver.find_elements_by_class_name("high-rating")
            if subtitles_1 == []:
                print("Sorry the subtiles aren't available")
            else:
                driver.delete_all_cookies()
                subtitles_2 = []
                subtitles_3 = []
                for i in subtitles_1:
                    subtitles_2 = i.text.split()
                    for j in subtitles_2:
                        if j == "English":
                            subtitles_3.append(i)
                print("English subtitles are been displayed: ")
                index = 0
                for english_subtitles in subtitles_3:
                    index = index + 1
                    print(index,".>",english_subtitles.text.strip("English").strip("Download"),"\n")
                choice = int(input("Please select the index value of the subtitle you would like to download: "))
                choice = choice - 1
                subtitles_3[choice].click()
                name = str(driver.current_url)
                name = name.strip("https://yts-subs.com/subtitles/")
                name = "C:\\Users\\Akshay Dileep\\Downloads\\"+name+ ".zip"
                driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[2]/div[4]/a').click()
                time.sleep(10)
                driver.close()
                file = ZipFile(name)
                file.extractall()
                print("Requested subtitles has been downloaded and extracted")
                os.startfile("E:\project\Downloader")
    except:
        print("Check internet connection")
    time.sleep(15)
    driver.close()
choice()