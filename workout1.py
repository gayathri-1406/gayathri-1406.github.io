import cv2
import numpy as np
from PIL import ImageGrab
from time import sleep  
from selenium import webdriver
from math import cos
from shapely.geometry import Polygon,Point

def Clean_browser1():
    # /html/body/div[3]/div/div[5]/div[1]/div/div[9]/div/div[2]/div[1]/div/div[2]
    sleep(2)
    def clear(lnk):
        elm=browser1.find_element_by_xpath(lnk)
        browser1.execute_script("arguments[0].style.display = 'none';", elm)
        sleep(0.5)
    clear('/html/body/div[3]/div/div[5]/div[1]/div/div[9]/div')
    clear('/html/body/div[3]/div/div[5]/div[1]/div/div[4]')
    clear('/html/body/div[3]/div/div[5]/div[1]/div/div[5]/div/div[1]/div[1]')
    clear('/html/body/div[3]/div/div[2]/div')
    clear('/html/body/div[3]/div/div[3]')
    clear('/html/body/div[3]/div/div[5]/div[3]/div')


Shps=[['11.022352090911742,76.95901236473289'],['11.005404016440474,76.95587903467384'],['11.029061168526834,76.9603576058374'],['11.026475883653783,76.94348960583743']]
browser1= webdriver.Chrome()
sleep(2)
browser1.maximize_window()
browser1.get('https://accounts.google.com/v3/signin/identifier?dsh=S1325409553%3A1681205161927729&ifkv=AQMjQ7R5Zgxdk-6JuNWQfLEQhvgG4bJEC6r2157Tlus-dutP6SpOShR221KSm9uAxR59MB9yGhA-HQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
sleep(3)

user_nme=browser1.find_elements_by_xpath('/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input')
user_nme[0].send_keys('gayathri.r@brandidea.ai')
sleep(1)

nxt_bt=browser1.find_elements_by_xpath('/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span')
nxt_bt[0].click()
sleep(2)
pwd=browser1.find_elements_by_xpath('/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
pwd[0].send_keys('Brand@2021')
sleep(1)
log_bt=browser1.find_elements_by_xpath('/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span')
log_bt[0].click()
sleep(5)
for k in Shps:
    browser1.get('https://www.google.com/maps/d/edit?mid=1HvDGOqpknZXon3cArWwh6mz8qR2XX-Y&ll='+k[0]+'&z=19')
    sleep(2)
    Clean_browser1()
    mine=browser1.current_url
    Pol=[]
    P1=[]
    static_ther=0.000002623
    center=eval(mine.split('=')[2][:-2].replace('%2C',','))
    # center=eval(k[0])
    
    lat = center[0]
    lon = center[1]
    Pi=3.14
    R=6378137
    dn = 50.7   #Lon
    de = -198.4  #Lat
    dLat = dn/R
    dLon = de/(R*cos(Pi*lat/180))
    latO = lat + dLat * 180/Pi
    lonO = lon + dLon * 180/Pi   
    tpp=[latO,lonO]
    rng=[[[8, 5, 140],[32, 32, 160]],[[15,125,185],[25,155,210]]]
    for u in rng:
        sleep(3)
    
        img1 = ImageGrab.grab()
        img= np.array(img1,np.uint8)
        
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(img, -1, kernel)
    
        im_hsv = cv2.cvtColor(sharpened, cv2.COLOR_BGR2HSV)
        
        sleep(4)
    
        imgContour = img
        lower1=np.array(u[0],np.uint8)#gmap-Residential
        upper1=np.array(u[1],np.uint8)#gmap-Residential

        mask1 = cv2.inRange(im_hsv, lower1,upper1)

        mask1= cv2.cvtColor(mask1, cv2.IMREAD_GRAYSCALE)

        threshold1 = 0
        threshold2 = 250
        kernel = np.ones((1,1))
        imgBlur1 = cv2.GaussianBlur(mask1, (0,0),1.0)

    
        imgCanny1 = cv2.Canny(imgBlur1,threshold1,threshold2,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

    
        imgDil1 = cv2.dilate(imgCanny1, kernel, iterations=3)
    
        contours1, hierarchy1 = cv2.findContours(imgDil1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        try:hierarchy1 = hierarchy1[0] 
        except: pass

        print("I Came Here to get contors")
        typ1='Residential'
        typ2='Shop'
        typ3='Corporate Office'
        for component in zip(contours1, hierarchy1):
            # print("Resident")
            currentHierarchy = component[1]
            if currentHierarchy[2] < 0:
                cnt1 = component[0]
            elif currentHierarchy[3] < 0:
                continue
            M1 = cv2.moments(cnt1)

            area = cv2.contourArea(cnt1)
            
            # approx = cv2.approxPolyDP(cnt1, 0.09 * cv2.arcLength(cnt1, True), True)
            approx=cnt1
            if area > 100:
                pp=[]
                for k in approx:
                    # print(k[0][0])
                    # k[0][0]=1080-k[0][0]
                    lat1=tpp[0]
                    lon1=tpp[1]
    
                    Pi=3.14
                    R=6378137
    
                    ln_dis=k[0][1]*0.2661
                    lt_dis=k[0][0]*0.2661
    
                    dn =  -ln_dis #Lon
                    de =  lt_dis #Lat
                    dLat = dn/R
                    dLon = de/(R*cos(Pi*lat1/180))
                    latO = lat1 + dLat * 180/Pi
                    lonO = lon1 + dLon * 180/Pi
                    # print(latO,lonO)
                    pp.append([latO,lonO][::-1])
                    try:
                        Pol1=Polygon(pp)
                        # pp.append(Pol1)
                        # Pnt1=Point(center)
                        # if Pol1.contains(Pnt1)!=False:
                        #     print(Pol1.contains(Pnt1))
                    except:
                        pass
                Pol.append(Pol1)
                P1.append(pp)
                # print('This is Pol',Pol)
    import geopandas as gpd
    d = {'geometry': Pol}
    gdf = gpd.GeoDataFrame(d)
    Pnt1=Point(center[::-1])
    polygon_index = gdf.distance(Pnt1).sort_values().index[0]
    print(gdf.loc[polygon_index])
    break
# #%%
# from shapely.geometry import Point, Polygon
# import geopandas as gpd
# d = {'geometry': [Polygon([(0, 0), (1, 1), (1, 0)]), Polygon([(3, 3), (4, 3), (4, 4)])]}
# gdf = gpd.GeoDataFrame(d)
# red_point = Point(1,2)
# polygon_index = gdf.distance(red_point).sort_values().index[0]
# gdf.loc[polygon_index]


# list(gdf.loc[polygon_index][0].exterior.coords)