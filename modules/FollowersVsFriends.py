from urllib.request import Request, urlopen, URLError
import twitter
import time
import config
import oauth2

# doesnt work if the user is private

if __name__ == '__main__':

    api = twitter.Api(consumer_key=config.consumerKey,
                      consumer_secret=config.consumerSecret,
                      access_token_key=config.accessToken,
                      access_token_secret=config.accessSecret,
                      sleep_on_rate_limit=True
                      )

def following(userName):
        x = []
        try:
            [(x.append(each.screen_name))for each in api.GetFriends(screen_name=userName)]
        except twitter.error.TwitterError:
            print("Error occured.", twitter.error.TwitterError)

        return x
def followers(userName):
        # x = []
        # try:
        #     [x.append(each.screen_name) for each in api.GetFollowers(screen_name = userName)]
        # except twitter.error.TwitterError:
        #         print("Error occured.", twitter.error.TwitterError)
        #
        # return x
        # x = []
        followerNames = []
        cursor = -1
        while True:
            try:
                x =  api.GetFollowersPaged(screen_name = userName, cursor=cursor, count = 200 )
                cursor = x[0] #next cursor for how much data is left to compare
                data = x[2] #all the user(id, username) tuples
                for each in data:
                    followerNames.append(each.screen_name)
            except twitter.error.TwitterError:
                    print("Rate limit exceeded")
            if (cursor == 0):
                break
        return followerNames

def compare(userName):

    followingList = following(userName)
    followersList = followers(userName)

    print ("\n\nthis should be " + userName + " list of following ")
    print (followingList)
    print ("\n\nthis should be " + userName + " list of followers ")
    print(followersList)
    print("\n\n")

    difference = len(followingList) - len(followersList)

    notFollowingList = []

    for each in followingList:
        if each in followersList:
            continue
        else:
            notFollowingList.append(each)

    return (difference, notFollowingList)


def main():

    userName = input("Whats the username you want to compare followers vs following on?")

    result = compare(userName)

    print("\n\n\nYou have", result[0], "less followers than people you follow.\n\n", "People you follow who don't follow you are:", result[1], "\n\n\n")


main()
