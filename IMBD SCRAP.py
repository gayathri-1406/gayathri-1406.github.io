import requests
from bs4 import BeautifulSoup

category=['Action',
'Adventure',
'Animation',
'Biography',
'Comedy',
'Crime',
'Documentary',
'Drama',
'Family',
'Fantasy',
'Film-Noir',
'History',
'Horror',
'Music',
'Musical',
'Romance',
'Sci-Fi',
'Short',
'Sport',
'Thriller',
'War',
'Western']

genre=[]
runtime=[]
certificate=[]
rating=[]
stars=[]
description=[]
votes=[]
director=[]
movie=[]
k=0
tmp=0
n=0
chk=['',1]
url='https://www.imdb.com/search/title/?genres='+category[k]

while True:
    # try:
    page=requests.get(url)
    # print(page)
    # url2='https://www.imdb.com/search/title/?genres=action&start=51&ref_=adv_nxt'
    # page2=requests.get(url2)
    # print(page2)
    dat=BeautifulSoup(page.content,"html.parser")
    
    all1=dat.findAll('div',{'class':'lister-item mode-advanced'})
    
    chk.append(all1)

    for i in all1:
        tmp=tmp+1
        print(category[k],tmp,i.find('img')['alt'])
        # url3='https://www.imdb.com/'+i.findAll('a')[1]['href']
        # page3=requests.get(url3)
        # print(i.find('div',{'class','lister-item-content'}))
        movie.append(i.find('img')['alt'])
        try:
            genre.append(i.find('span',{'class','genre'}).text[1:])
        except:
            genre.append('')
        try:
            runtime.append(i.find('span',{'class','runtime'}).text)
        except:
            runtime.append('')
        try:
            certificate.append(i.find('span',{'class','certificate'}).text)
        except:
            certificate.append('')
            
        try:    
            rating.append(i.find('strong').text)
        except:
            rating.append('')
        
        try:
            description.append(i.findAll('p',{'class','text-muted'})[1].text[1:])
        except:
            description.append('')

        try:
            idx=i.find('p',{'class',''}).text.split('\n').index('    Stars:')
            stars.append(i.find('p',{'class',''}).text.split('\n')[idx+1:])
        except:
            try:
                idx=i.find('p',{'class',''}).text.split('\n').index('    Star:')
                stars.append(i.find('p',{'class',''}).text.split('\n')[idx+1:])
            except:
                stars.append('')
        try:
            votes.append(i.find('p',{'class','sort-num_votes-visible'}).findAll('span')[-1].text)
        except:
            votes.append('')
        try:
            i.find('p',{'class',''}).text.split('\n').index('    Director:')
            director.append(i.find('p',{'class',''}).text.split('\n')[2:idx-1])
        except:
            director.append('')
    n=n+50
    print(n)
    url='https://www.imdb.com/search/title/?genres='+category[k]+'&start='+str(n)+'&ref_=adv_nxt'
    
    if chk[-1]==chk[-2] and chk[-2]==chk[-3]:
        n=0
        k=k+1
        url='https://www.imdb.com/search/title/?genres='+category[k]
        chk=['',1]
    if k>21:
        break
    # except:
    #     break
    # break
#%%
import pandas as pd
df=pd.DataFrame()
df['movie']=movie
df['genre']=genre
df['runtime']=runtime
df['certificate']=certificate
df['rating']=rating
df['stars']=stars
df['description']=description
df['votes']=votes
df['director']=director

df.to_csv(r'C:\Users\Sort\Desktop\IMBD.csv')
#%%

dic1={}
l1=["date","age"]
w=[[1,2],
[34,90],
["g","o"],
["Q","Y"]]

