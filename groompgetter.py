from pyquery import PyQuery as q
import re

videoIdPattern = re.compile('\?v=(.{11})')
latest = ""
with open('latest.sav','r') as f:
	latest = f.read()
	f.close()

def getUserUploads(username):
	doc = q("https://www.youtube.com/user/%s/videos" % username)
	vids = doc('#channels-browse-content-grid .yt-lockup-title a[href^="/watch"]')
	vids = vids.map(lambda i, e: {
		'id':videoIdPattern.findall(q(e).attr('href')),
		'title':q(e).attr('title')
	})

	for v in vids:
		if len(v['id']) and v['title']:
			if v['id'][0]==latest:
				break
			notifyVideo(v['id'][0],v['title'])

	f = open('latest.sav','w')
	f.write(vids[0]['id'][0])
	f.close()

def notifyVideo(videoId,videoName):
	print("New video! {0} (http://youtu.be/{1})".format(videoName,videoId))

getUserUploads(input("Enter username: "))