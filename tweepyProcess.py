import tweepy
import json
import csv
import os
import requests
import openpyxl
import time
import datetime
import main
import circlePostion as circlePosition

consumer_key = 'EWZEu7RBUhJ4nfy9fawZ1tTWc'
consumer_secret = 'hlyr7GPr4F1969wY5XEGutrXj00DHEbgO50ZiEKjOMFQJd7H4V'


#twitter認証
def authTwitter(consumer_key, consumer_secret, access_token_key, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    return tweepy.API(auth,wait_on_rate_limit=True)

#csvがすでに存在していればリセット
def resetDirectory():
    if(os.path.exists('lists_tweets.csv')):
        os.remove('lists_tweets.csv')

def getList(consumer_key, consumer_secret, access_token_key, access_token_secret):
    api=authTwitter(consumer_key, consumer_secret, access_token_key, access_token_secret)
    ress = api.lists_all()
    return ress

def getMember(consumer_key, consumer_secret, access_token_key, access_token_secret, listIndex):
    #認証
    api=authTwitter(consumer_key, consumer_secret, access_token_key, access_token_secret)
    ress = api.lists_all()
    res=ress[listIndex]
    return res.member_count

#検索メソッド
def searchTweet(consumer_key, consumer_secret, access_token_key, access_token_secret, list_index, searchDate, isFolder, csvOption, progress, dir):
    #認証
    api=authTwitter(consumer_key, consumer_secret, access_token_key, access_token_secret)
    ress = api.lists_all()
    i=0
    member_count=1
    res=ress[list_index]
    name=res.name
    ids=res.id
    slug=res.slug
    print(name)
    print(ids)
    print(slug)
    print()


    csvPath = dir + '/tweet_list.csv'
    if csvOption[0]:
        with open(csvPath,'a',encoding="utf_8_sig")as f:
            writer = csv.writer(f)
            array = ['name', 'URL', 'text', 'image_num', 'circle_position']
            csvItem=[]
            s=0
            for t in csvOption[1]:
                if t:
                    csvItem.append(array[s])
                print(csvItem)
                s=s+1
            writer.writerow(csvItem)
        f.close

    #リストメンバー取得
    members=tweepy.Cursor(api.list_members,slug=slug,owner_screen_name=api.me().screen_name).items()
    for member in members:
        name=member.name
        name=circlePosition.remove_emoji(name)
        progress.moveProgress(member_count, name)
        name=name.replace('*','')
        name=name.replace('.','')
        name=name.replace('/','')
        #名前表示
        print()
        print('==================================================')
        print(name+'  '+str(member_count)+'/'+str(res.member_count))
        print('==================================================')
        member_count+=1
        i=i+1
        #ツイート取得　ツイートに「お品書き」が含まれている、かつ画像が添付されているもの
        for tweet in tweepy.Cursor(api.user_timeline,id=member.id, since_id=1189931802908954625).items():
            if ('お品書き' in tweet.text or 'おしながき' in tweet.text or 'お' in tweet.text) and not('RT' in tweet.text) :
                if(searchDate > tweet.created_at):
                    break
                #print(tweet)
                if 'media' in tweet.entities:
                    for k in tweet.entities['media']:
                        j=1
                        url = k['media_url']
                        tweetURL='https://twitter.com/'+tweet.user.screen_name + '/status/' + str(tweet.id)
                        #画像を取得
                        if isFolder[0]:
                            response=requests.get(url,stream=True)
                            if response.status_code==200:
                                if isFolder[1]:
                                    os.makedirs(dir + '/' +name,exist_ok=True)
                                    path=dir + '/' +name+'/oshinagaki'+str(i)+'-'+str(j)+'.jpg'
                                else:
                                    path=dir + '/' +name+str(i)+'-'+str(j)+'.jpg'
                                    #ファイル書き込み
                                with open(path,'wb') as file:
                                    file.write(response.content)
                                file.close
                        #サークル一取得
                        position = ''.join(circlePosition.circlePosition(name))
                        if csvOption[0]:
                            with open(csvPath,'a',encoding="utf_8_sig")as f:
                                writer = csv.writer(f)
                                array = [name,tweetURL,tweet.text,path,position]
                                csvItem=[]
                                s=0
                                for t in csvOption[1]:
                                    if t:
                                        csvItem.append(array[s])
                                    s=s+1
                                writer.writerow(csvItem)
                                print(csvItem)
                            f.close
                        j=j+1
                break