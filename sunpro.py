import urllib.request
from PIL import Image
import io
import os, glob
"""
# open a connection to a URL using urllib
webUrl  = urllib.request.urlopen('https://sdo.gsfc.nasa.gov/assets/img/browse/2021/07/12/20210712_000000_512_HMIIF.jpg')

#get the result code and print it
print ("result code: " + str(webUrl.getcode()))

# read the data from the URL and print it
data = webUrl.read()

"""




def get_sun_from_date(datetime: str, upload_folder: str) -> str:

    date, hour = datetime.split('_')
    year, month, day = date.split('/')

    hmib_file =  f'{year}{month}{day}_{hour}0000_512_HMIB.jpg'
    hmiif_file = f'{year}{month}{day}_{hour}0000_512_HMIIF.jpg'

    hmib_url = f'{year}/{month}/{day}/{year}{month}{day}_{hour}0000_512_HMIB.jpg'
    hmiif_url = f'{year}/{month}/{day}/{year}{month}{day}_{hour}0000_512_HMIIF.jpg'

    sdo_base_url = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'

    # record HMIB pic
    with urllib.request.urlopen(sdo_base_url + hmib_url) as url:
        with open(upload_folder + '/' + hmib_file, 'wb') as f:
            f.write(url.read())


    with urllib.request.urlopen(sdo_base_url + hmiif_url) as url:
        with open(upload_folder + '/' + hmiif_file, 'wb') as f:
            f.write(url.read())

    #img = Image.open('static/uploads/' + hmib_file)
    #img.show()

    #img = Image.open('static/uploads/' + hmiif_file)
    #img.show()

    return upload_folder + '/' + hmib_file , upload_folder + '/' + hmiif_file







"""
from PIL import Image
import urllib.request

URL = 'http://www.w3schools.com/css/trolltunga.jpg'

with urllib.request.urlopen(URL) as url:
    with open('temp.jpg', 'wb') as f:
        f.write(url.read())

img = Image.open('temp.jpg')

img.show()
"""

#list

#https://sdo.gsfc.nasa.gov/assets/img/browse/2021/07/12/20210712_000000_512_HMIIF.jpg

"""
#00 H 00 M 00 S
20210712_000000_512_HMIIF.jpg
20210712_000000_512_HMIB.jpg
20210712_000317_512_1700.jpg  
20210712_000411_512_304211171.jpg 
20210712_000610_512_0171.jpg 

# 3H0
20210712_030000_512_HMIIF.jpg
20210712_030000_512_HMIB.jpg            



#4H00
20210712_040000_512_HMIIF.jpg    
20210712_040000_512_HMIB.jpg    


#5H00
20210712_050000_512_HMIIF.jpg 
20210712_050000_512_HMIB.jpg    


#6H15
  20210712_061500_512_HMIIF.jpg  
  20210712_061500_512_HMIB.jpg    
   

#7H00
     20210712_070000_512_HMIIF.jpg  
     20210712_070000_512_HMIB.jpg  
     

#8H00
      20210712_080000_512_HMIIF.jpg  
      20210712_080000_512_HMIB.jpg   



#9H00
     20210712_090000_512_HMIIF.jpg   
     20210712_090000_512_HMIB.jpg  

    20210612_090010_512_0171.jpg 


#10H00
      20210712_100000_512_HMIIF.jpg  
      20210712_100000_512_HMIB.jpg  

#11H
   20210712_110000_512_HMIIF.jpg     
   20210712_110000_512_HMIB.jpg     

#12H
 20210712_120000_512_HMIIF.jpg    
 20210712_120000_512_HMIB.jpg   


#13H
      20210712_130000_512_HMIIF.jpg   
      20210712_130000_512_HMIB.jpg    

#14H
      20210712_140000_512_HMIIF.jpg
       20210712_140000_512_HMIB.jpg      



#15H
  20210712_150000_512_HMIIF.jpg   
   20210712_150000_512_HMIB.jpg    


  #16H
        20210712_160000_512_HMIIF.jpg
         20210712_160000_512_HMIB.jpg      

#17H
   20210712_170000_512_HMIIF.jpg 
    20210712_170000_512_HMIB.jpg            

#18H
      20210712_180000_512_HMIIF.jpg   
       20210712_180000_512_HMIB.jpg     


#19H
20210712_190000_512_HMIIF.jpg   
 20210712_190000_512_HMIB.jpg    

#20H
      20210612_200000_512_HMIIF.jpg   
       20210712_200000_512_HMIB.jpg     

#21h
      20210612_210000_512_HMIIF.jpg  
       20210712_210000_512_HMIB.jpg    
#22H
     20210612_220000_512_HMIIF.jpg
      20210712_220000_512_HMIB.jpg      

#23
    20210612_230000_512_HMIIF.jpg 
    20210712_230000_512_HMIB.jpg   
"""




#result = Fido.search(a.Time('2021/07/11', '2021/07/11'),
#                     a.Instrument.hmi, a.Physobs.los_magnetic_field)

"""
result = Fido.search(a.Time('2021/07/12', '2021/07/12'), a.Instrument.lyra, a.Level.two) 

print(result)  
downloaded_files = Fido.fetch(result)  

hmi_map = sunpy.map.Map(downloaded_files)
fig = plt.figure()
hmi_map.plot()

plt.show()
"""






#tst = a.Time('2012/3/4', '2012/3/6')
#a.Instrument.lyra

#print(tst)

#print(a.Instrument)



#test1

#jsoc series
#print(a.jsoc.Series)

#test2
#result = Fido.search(a.Time('2021/6/12', '2021/6/12'), a.Instrument.aia)
#print(result)

#results = Fido.search(a.Time("2021/6/12 15:00", "2021/6/12 16:00"), a.Instrument.aia)  
#print(results)

#downloaded_files = Fido.fetch(results)  



#result = Fido.search(a.Time('2020/06/13 13:47', '2020/06/13 13:48'),
#                     a.Instrument.aia)
                     #a.Wavelength(171*u.angstrom))
#print(result)

#results = Fido.search(a.Time("2021/07/12 15:05", "2021/07/12 15:10"), a.Instrument.aia | a.Instrument.hmi)  
#print(results)  



#print(aia)


"""
result = Fido.search(a.Time('2021/06/13 13:31', '2021/06/13 13:32'),
                     a.Instrument.hmi, a.Physobs.los_magnetic_field)

print(result)

jsoc_result = result[0]
print(jsoc_result.show('T_REC', 'CROTA2'))


downloaded_file = Fido.fetch(result)
print(downloaded_file)

hmi_map = sunpy.map.Map(downloaded_file[0])
fig = plt.figure()
hmi_map.plot()

plt.show()


hmi_rotated = hmi_map.rotate(order=3)
hmi_rotated.plot()

plt.show()
"""


#res = Fido.search(a.Time('2021/06/13 13:40', '2021/06/13 14:00'), a.Instrument.aia, a.Wavelength(171*u.angstrom))  

#print(res)
#files = Fido.fetch(res[:, 0])

#downloaded_files = Fido.fetch(result)





#result = Fido.search(a.Time('2021/06/12 10:00', '2021/06/12 15:00'),
#                     a.Instrument.aia,
#                     a.Wavelength(171*u.angstrom) | a.Wavelength(94*u.angstrom))
#print(result)


# Affichage
#map = sunpy.map.Map(downloaded_files[2])
#fig = plt.figure(figsize=(16,9))
#map.plot()
#plt.show()

#---------- IMAGE GENERIQUE -------------#
"""
smap = sunpy.map.Map(AIA_171_IMAGE)

figure = plt.figure(frameon=False)
ax = plt.axes([0, 0, 1, 1])
# Disable the axis
ax.set_axis_off()

# Plot the map. Since are not interested in the exact map coordinates, we can
# simply use :meth:`~matplotlib.Axes.imshow`.
norm = smap.plot_settings['norm']
norm.vmin, norm.vmax = np.percentile(smap.data, [1, 99.9])
ax.imshow(smap.data,
          norm=norm,
          cmap=smap.plot_settings['cmap'])
          

plt.show()"""