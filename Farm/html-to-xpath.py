from bs4 import BeautifulSoup, Comment
import requests
import re

def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0,parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)



if __name__ == '__main__':
    r = requests.get("https://python123.io/ws/demo.html")
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.prettify())

    print('打印a标签: \n', soup.find_all('a'))
    print('---------------------------')


    print('打印a和b的标签: \n', soup.find_all(['a','b']))
    print('---------------------------')

    print('打印出b开头的标签')
    for tag in soup.find_all(re.compile("b")):
        print(tag.name)
    print('---------------------------')

    print('打印带有属性值course的p标签 \n', soup.find_all('p', 'course'))
    print('---------------------------')

    print('打印指定字符串,id="link1')
    kv = {'id': 'link1'}
    print(soup.find_all(**kv))
    print('---------------------------')

    # 是否对子孙节点进行搜索
    kv = {'recursive': 'False'}
    print('打印a标签,但是不对子孙节点进行搜索: \n', soup.find_all('a', **kv))
    print('---------------------------')

    kv = {'string': 'Basic Python'}
    print('打印标签直接的字符串，需要准确匹配: \n', soup.find_all(**kv))
    print('---------------------------')
