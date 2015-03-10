import glitch
import subprocess
import tumblr
import pytumblr
import datetime
import twitter

def make_gif(filename, paths, duration=10):
    subprocess.call(['convert', '-delay', '20', '-loop', '0'] + paths + [filename])

def get_caption(titles):
    # Have the beginning of the captions start with the day's date
    date = datetime.datetime.now()
    date_string = date.strftime("%m-%d-%Y")
    caption = date_string + '\n'
    for title in titles:
        caption += title + '\n'
    return caption

tumblr.search_party()

# ##YOUR NEW NUMBER##
# search_num = tumblr.top_hit_num
# # divide by 5,000,000 to normalize the range from [0,5000000] to [0,1]
# # multiply by 5 to increase the range from [0,5]
# glitch_num = ((search_num / 5000000) * 5)

glitcher = glitch.Glitch()

frames = []
#glitched_image = tumblr.searchTerm
total_mentions = 5

for i in range(0, total_mentions):
    glitched_image = glitcher.trigger(tumblr.searchTerm + '.jpg', "random")
    print glitched_image
    frames.append(tumblr.searchTerm + '.jpg')

make_gif("mygif.gif", frames)

# make_gif("mygif.gif", ["ken/ken-109-glitched.jpg", "ken/ken-118-glitched.jpg", "ken/ken-121-glitched.jpg"])

ouath_data = open("oauth.txt")

# get all keys
keys = ouath_data.read()
keys_decoded = keys.decode("utf-8-sig")
keys = keys_decoded.encode("utf-8")
keys = keys.rstrip().split('\n')


client = pytumblr.TumblrRestClient(
  keys[0],
  keys[1],
  keys[2],  
  keys[3]
)

tweet = twitter.get_random_tweet().encode('utf-8') 
caption = get_caption(tumblr.get_titles()) + "\n" + tweet 
# post photo to tumblr
client.create_video("anarchyarchive", state="published", caption = caption, data = "mygif.gif" )
