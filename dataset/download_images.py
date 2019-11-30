from requests_html import HTMLSession
import requests
import os
import argparse
import sys
import json
import time

def main(args):
  #parse arguments
  parser = argparse.ArgumentParser(description='Scrape Google imges')
  parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
  parser.add_argument('-n', '--num_images', default=10, type=int, help='num images to save')
  parser.add_argument('-d', '--directory', default='/Users/gene/Downloads/', type=str, help='save directory')
  args = parser.parse_args()
  query = args.search#raw_input(args.search)
  max_images = args.num_images
  save_directory = args.directory
  
  #Create url to search images
  query= query.split()
  query='+'.join(query)
  url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch&tbs=sur:fc"
  
  session = HTMLSession()
  res = session.get(url)
  
  while not(res.ok):
    time.sleep(1)
    res = session.get(url)
  
  i = 0
  
  print(len(res.html.find('.rg_meta')))
  
  for value in res.html.find('.rg_meta'):
    json_data = json.loads(value.text)
    img = json_data['ou']
    ext = json_data['ity']
    
    if ext == '':
      continue
    
    print(f'Downloading: {img}')
    
    try:
      raw_img = requests.get(img, timeout=10).content
      #store image
      f = open(os.path.join(save_directory, f'img_{i}.{ext}'), 'wb')
      f.write(raw_img)
      f.close()
    except Exception as e:
      print(f"Could not load: {img}")
      print(e)
        
    i += 1
    if i == max_images:
      break;

if __name__ == '__main__':
  from sys import argv
  try:
    main(argv)
  except KeyboardInterrupt:
    pass
    sys.exit()
