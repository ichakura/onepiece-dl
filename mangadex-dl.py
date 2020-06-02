

import cloudscraper
import time, os, sys, re, json, html, re, time, datetime
global value
try:
	a = sys.argv[1]

except IndexError:
	a = ""
try:
	b = sys.argv[2]
except IndexError:
	b = ""


def folder_organization():
    import os
    import zipfile
    import re
    import shutil




    os.chdir("C:\\Users\\rahul\\Documents\\mangadex-dl\\download\One Piece")





    def zip(src, dst):
        zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
        abs_src = os.path.abspath(src)
        for dirname, subdirs, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                print('zipping %s as %s' % (os.path.join(dirname, filename),
                                            arcname))
                zf.write(absname, arcname)
        zf.close()

           
        
    def move():
        for file in sourcefiles:
            if file.endswith('.cbr'):
                f = open("./cbrs/cbrlist.txt", "a")
                f.write(file)
                f.write('\n')
                f.close()
                shutil.move(os.path.join(sourcepath,file), os.path.join(destinationpath,file))
                  
    a = []
    not_empty = []
    dirs = [x[0] for x in os.walk(".")]

    for i in dirs:
        regex = "\d{3}"
      
        b = re.findall(regex, i)
        a.append(b)
    abc = [x for x in a if x]
                


    sourcepath='.'
    sourcefiles = os.listdir(sourcepath)
    destinationpath = './cbrs'

    first_num = min(abc)
    tmpnumone = abc.index(first_num)
    first_num = abc[tmpnumone]
    first_num = int(first_num[0])



    second_num = max(abc)
    tmpnumtwo = abc.index(second_num)
    second_num = abc[tmpnumtwo]
    second_num = int(second_num[0])
    second_num = second_num + 1

    def change_name(num):
        global source
        global name
        name = ""
        cname = ""
        nitoryu = ".\\c" + num + " [Nitoryu]"
        null = ".\\c" + num + " [Null]"
        tor = os.path.isdir(nitoryu)
        ull = os.path.isdir(null)
        if tor == False:
        
            if ull == True:
                name = null
        else:
            name = nitoryu
        source = name
        
    def moved(source):
        destination = ".\\converted"
        shutil.move(source, destination, copy_function = shutil.copytree)
        
    r = range(first_num, second_num)
    for n in r:
        num = str(n)

        with open("./cbrs/cbrlist.txt") as f:
            if num in f.read():
                print("already there")
                continue
                
                
        change_name(num)
        zip(name, num)
     
        for root, dirs, files in os.walk("."): #this finds the zip files
                for file in files:
                    if file.endswith(".zip"):
                         a = os.path.join(root, file)
                         
        base = os.path.splitext(a)[0]
        os.rename(a, base + '.cbr')#changing the extension
        print("Renamed.")
        
        moved(source)
        print("Moved to 'done' folder.")
    sourcepath='.'
    sourcefiles = os.listdir(sourcepath)
    destinationpath = './cbrs'    
        
    move()

    print("Done~")



def normal():

	A_VERSION = "V0.2.2"

	def pad_filename(str):
		digits = re.compile('(\\d+)')
		pos = digits.search(str)
		if pos:
			return str[1:pos.start()] + pos.group(1).zfill(3) + str[pos.end():]
		else:
			return str

	def float_conversion(x):
		try:
			x = float(x)
		except ValueError: # empty string for oneshot
			x = 0
		return x

	def zpad(num):
		if "." in num:
			parts = num.split('.')
			return "{}.{}".format(parts[0].zfill(3), parts[1])
		else:
			return num.zfill(3)

	def dl(manga_id, lang_code, tld="org"):
		# grab manga info json from api
		scraper = cloudscraper.create_scraper()
		try:
			r = scraper.get("https://mangadex.{}/api/manga/{}/".format(tld, manga_id))
			manga = json.loads(r.text)
		except (json.decoder.JSONDecodeError, ValueError) as err:
			print("CloudFlare error: {}".format(err))
			exit(1)

		try:
			title = manga["manga"]["title"]
		except:
			print("Please enter a MangaDex manga (not chapter) URL.")
			exit(1)
		print("\nTitle: {}".format(html.unescape(title)))

		# check available chapters
		chapters = []

		if "chapter" in manga:
			print("Chapter found in language you requested")
		else:
			print("Chapter not found in the language you requested.")
			exit(1)

		for chap in manga["chapter"]:
			if manga["chapter"][str(chap)]["lang_code"] == lang_code:
				chapters.append(manga["chapter"][str(chap)]["chapter"])
		chapters.sort(key=float_conversion) # sort numerically by chapter #

		chapters_revised = ["Oneshot" if x == "" else x for x in chapters]
		print("Available chapters:")
		print(" " + ', '.join(map(str, chapters_revised)))

		# i/o for chapters to download
		requested_chapters = []
		chap_list = input("\nEnter chapter(s) to download: ").strip()
		chap_list = [s for s in chap_list.split(',')]
		for s in chap_list:
			if "-" in s:
				split = s.split('-')
				lower_bound = split[0]
				upper_bound = split[1]
				try:
					lower_bound_i = chapters.index(lower_bound)
				except ValueError:
					print("Chapter {} does not exist. Skipping {}.".format(lower_bound, s))
					continue # go to next iteration of loop
				try:
					upper_bound_i = chapters.index(upper_bound)
				except ValueError:
					print("Chapter {} does not exist. Skipping {}.".format(upper_bound, s))
					continue
				s = chapters[lower_bound_i:upper_bound_i+1]
			else:
				try:
					s = [chapters[chapters.index(s)]]
				except ValueError:
					print("Chapter {} does not exist. Skipping.".format(s))
					continue
			requested_chapters.extend(s)

		# find out which are availble to dl
		chaps_to_dl = []
		for chapter_id in manga["chapter"]:
			try:
				chapter_num = str(float(manga["chapter"][str(chapter_id)]["chapter"])).replace(".0","")
			except:
				pass # Oneshot
			chapter_group = manga["chapter"][chapter_id]["group_name"]
			if chapter_num in requested_chapters and manga["chapter"][chapter_id]["lang_code"] == lang_code:
				chaps_to_dl.append((str(chapter_num), chapter_id, chapter_group))
		chaps_to_dl.sort()

		if len(chaps_to_dl) == 0:
			print("No chapters available to download!")
			exit(0)

		# get chapter(s) json
		print()
		for chapter_id in chaps_to_dl:
			print("Downloading chapter {}...".format(chapter_id[0]))
			r = scraper.get("https://mangadex.{}/api/chapter/{}/".format(tld, chapter_id[1]))
			chapter = json.loads(r.text)

			# get url list
			images = []
			server = chapter["server"]
			if "mangadex.{}".format(tld) not in server:
				server = "https://mangadex.{}{}".format(tld, server)
			hashcode = chapter["hash"]
			for page in chapter["page_array"]:
				images.append("{}{}/{}".format(server, hashcode, page))

			# download images
			groupname = chapter_id[2].replace("/","-")
			for url in images:
				filename = os.path.basename(url)
				dest_folder = os.path.join(os.getcwd(), "download", title, "c{} [{}]".format(zpad(chapter_id[0]), groupname))
				if not os.path.exists(dest_folder):
					os.makedirs(dest_folder)
				dest_filename = pad_filename(filename)
				outfile = os.path.join(dest_folder, dest_filename)

				r = scraper.get(url)
				if r.status_code == 200:
					with open(outfile, 'wb') as f:
						f.write(r.content)
				else:
					print("Encountered Error {} when downloading.".format(e.code))

				print(" Downloaded page {}.".format(re.sub("\\D", "", filename)))
				time.sleep(1)

		print("Done!")

	if __name__ == "__main__":
		print("mangadex-dl v{}".format(A_VERSION))

		lang_code = 'gb'
		url = ""
		while url == "":
			url = "https://mangadex.org/title/39/one-piece".strip()
		try:
			manga_id = re.search("[0-9]+", url).group(0)
			split_url = url.split("/")
			for segment in split_url:
				if "mangadex" in segment:
					url = segment.split('.')
			dl(manga_id, lang_code,  url[1])
		except:
			print("Error with URL.")


'''
========================================================================================================================
========================================================================================================================
========================================================================================================================
========================================================================================================================
'''


def mod():
	

	A_VERSION = "Mangadex DL Modded by Rahul V0.2.3"

	def pad_filename(str):
		digits = re.compile('(\\d+)')
		pos = digits.search(str)
		if pos:
			return str[1:pos.start()] + pos.group(1).zfill(3) + str[pos.end():]
		else:
			return str

	def float_conversion(x):
		try:
			x = float(x)
		except ValueError: # empty string for oneshot
			x = 0
		return x

	def zpad(num):
		if "." in num:
			parts = num.split('.')
			return "{}.{}".format(parts[0].zfill(3), parts[1])
		else:
			return num.zfill(3)
	
		

	def dl(manga_id, lang_code, lowest_num, tld="org"):
		# grab manga info json from api
		scraper = cloudscraper.create_scraper()
		try:
			r = scraper.get("https://mangadex.{}/api/manga/{}/".format(tld, manga_id))
			manga = json.loads(r.text)
		except (json.decoder.JSONDecodeError, ValueError) as err:
			print("CloudFlare error: {}".format(err))
			exit(1)

		try:
			title = manga["manga"]["title"]
		except:
			print("Please enter a MangaDex manga (not chapter) URL.")
			exit(1)
		print("\nTitle: {}".format(html.unescape(title)))

		# check available chapters
		chapters = []

		if "chapter" in manga:
			print("Chapter found in language you requested")
		else:
			print("Chapter not found in the language you requested.")
			exit(1)

		for chap in manga["chapter"]:
			if manga["chapter"][str(chap)]["lang_code"] == lang_code:
				chapters.append(manga["chapter"][str(chap)]["chapter"])
		chapters.sort(key=float_conversion) # sort numerically by chapter #

		chapters_revised = ["Oneshot" if x == "" else x for x in chapters]
		print("Available chapters:")
		print(" " + ', '.join(map(str, chapters_revised)))

		# i/o for chapters to download

		requested_chapters = []
		chap_list = input("\nEnter chapter to download to: ").strip()
		chap_list = [s for s in chap_list.split(',')]
		for s in chap_list:
			s = s.strip() 
			if "-" not in s:
				s =  s + "-"
			if "-" in s:
				split = s.split('-')
				lower_bound = lowest_num
				upper_bound = split[0]
				try:
					lower_bound_i = chapters.index(lower_bound)
				except ValueError:
					print("Chapter {} does not exist. Skipping {}.".format(lower_bound, s))
					continue # go to next iteration of loop
				try:
					upper_bound_i = chapters.index(upper_bound)
				except ValueError:
					print("Chapter {} does not exist. Skipping {}.".format(upper_bound, s))
					continue
				s = chapters[lower_bound_i:upper_bound_i+1]
			else:
				try:
					s = [chapters[chapters.index(s)]]
				except ValueError:
					print("Chapter {} does not exist. Skipping.".format(s))
					continue
			requested_chapters.extend(s)

		# find out which are availble to dl
		chaps_to_dl = []
		for chapter_id in manga["chapter"]:
			try:
				chapter_num = str(float(manga["chapter"][str(chapter_id)]["chapter"])).replace(".0","")
			except:
				pass # Oneshot
			chapter_group = manga["chapter"][chapter_id]["group_name"]
			if chapter_num in requested_chapters and manga["chapter"][chapter_id]["lang_code"] == lang_code:
				chaps_to_dl.append((str(chapter_num), chapter_id, chapter_group))
		chaps_to_dl.sort()

		if len(chaps_to_dl) == 0:
			print("No chapters available to download!")
			exit(0)

		# get chapter(s) json
		
		for chapter_id in chaps_to_dl:
			print("Downloading chapter {}...".format(chapter_id[0]))
			r = scraper.get("https://mangadex.{}/api/chapter/{}/".format(tld, chapter_id[1]))
			chapter = json.loads(r.text)

			# get url list
			images = []
			server = chapter["server"]
			if "mangadex.{}".format(tld) not in server:
				server = "https://mangadex.{}{}".format(tld, server)
			hashcode = chapter["hash"]
			for page in chapter["page_array"]:
				images.append("{}{}/{}".format(server, hashcode, page))

			# download images
			groupname = chapter_id[2].replace("/","-")
			for url in images:
				filename = os.path.basename(url)
				dest_folder = os.path.join(os.getcwd(), "download", title, "c{} [{}]".format(zpad(chapter_id[0]), groupname))
				if not os.path.exists(dest_folder):
					os.makedirs(dest_folder)
				dest_filename = pad_filename(filename)
				outfile = os.path.join(dest_folder, dest_filename)

				r = scraper.get(url)
				if r.status_code == 200:
					with open(outfile, 'wb') as f:
						f.write(r.content)
				else:
					print("Encountered Error {} when downloading.".format(e.code))

				print(" Downloaded page {}.".format(re.sub("\\D", "", filename)))
				time.sleep(1)

		print("Done!")

	if __name__ == "__main__":
		print("mangadex-dl v{}".format(A_VERSION))
		lines = []
		reg = "\|*.cbr\|*"
		with open(".\\download\\One Piece\\cbrs\\cbrlist.txt") as f:
			content = f.readlines()
		content = [x.strip() for x in content] 
		content = max(content)
		content = int(re.sub(reg, "", content))
		value = str(content)
		content = str(content + 1)
		
		print("Last chapter you got: " + value)
		
		
		lang_code = "gb"
		
		url = ""

		while url == "":
			url = "https://mangadex.org/title/39/one-piece".strip()
		try:
			manga_id = re.search("[0-9]+", url).group(0)
			split_url = url.split("/")
			for segment in split_url:
				if "mangadex" in segment:
					url = segment.split('.')
			dl(manga_id, lang_code, content, url[1])
		except:
			print("Error with URL.")


start = time.time()
if a == "n":
	print("Booting normal version of mangadex-dl")
	normal()
if a == "f":
    folder_organization()
if a == "":
	print("Booting custom version of mangadex-dl")
	mod()

folder_organization()
end = time.time()
print(start, end)
sec = end - start
sec = str(datetime.timedelta(seconds=sec))
print(sec)
