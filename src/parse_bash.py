from bs4 import BeautifulSoup
import requests as req


def get_joke():
    resp = req.get("https://bash.im/random")

    soup = BeautifulSoup(resp.text, 'lxml')

    tag = soup.find("div", {'class': 'quote__body'})
    return_str = ""
    for i in range(len(tag.contents)):
        if str(tag.contents[i]) != '<br/>':
            # print(str(tag.contents[i]).lstrip())
            return_str += str(tag.contents[i]).lstrip()

    return return_str


if __name__ == "__main__":
    joke_str = get_joke()
    print(joke_str)

