import requests
import time
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from urllib.request import urlopen as uReq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import logging
import pymongo
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service(executable_path=r'/Users/ankitbodar/Software/chromedriver_mac64/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

application = Flask(__name__) # initializing a flask app
app=application

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template('index.html')

@app.route('/channle',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            url = "https://www.youtube.com/@" + searchString +'/videos'
            driver.get(url)
            time.sleep(5) 
            video_page = driver.page_source.encode('utf-8')
            driver.quit() 

            soup = bs(video_page, 'html.parser')
            video_containers = soup.find_all('div', {'id': 'dismissible'})

            videos=[]
            for container in video_containers[:5]:
                video_url=''
                thumbnail_url=''
                title=''
                views=''
                upload_time=''
                    # Extract the video URL
                try:
                    video_url = 'https://www.youtube.com'+container.find('a',{'class':'yt-simple-endpoint inline-block style-scope ytd-thumbnail'})['href']
                    if len(video_url)==0:
                        video_url='NA'
                except:
                    logging.info("video_url")
                
                # Extract the thumbnail URL
                try:
                    thumbnail_url = container.a.find('img',{'alt': ''})['src']
                    if thumbnail_url=='':
                        thumbnail_url='NA'
                
                except:
                    logging.info("thumbnail_url")
                # Extract the video title
                try:
                    title = container.find('a', {'class': 'yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media'})['title']
                    if len(title)==0:
                        title='NA'
                except:
                    logging.info("title")
                # Extract the view count
                try:
                    views = container.find('span', {'class': 'inline-metadata-item style-scope ytd-video-meta-block'}).text.strip()
                    if len(views)==0:
                        views='NA'
                except:
                    logging.info("views")
                # Extract the upload time
                try:
                    for ut in container.find_all('span', {'class': 'inline-metadata-item style-scope ytd-video-meta-block'})[1:]:
                        upload_time=ut.text.strip()
                    if len(upload_time)==0:
                        upload_time='NA'
                except Exception as e:
                            logging.info(e)
                
                
                video = {
                    'Video URL': video_url,
                    'Thumbnail URL': thumbnail_url,
                    'Title': title,
                    'Views': views,
                    'Upload Time': upload_time
                }
            
                videos.append(video)
            client=pymongo.MongoClient("mongodb+srv://ankitbodar001:17931793@cluster0.z8vs20i.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
            db=client['youtube_scrap']
            review_col=db['youtube_scrap_data']
            review_col.insert_many(videos)
            return render_template('results.html', reviews=videos[0:(len(videos)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
	#app.run(debug=True)
