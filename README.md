# DoubanSpider_notes

一句话介绍：模拟浏览器自动在豆瓣搜索框中输入175本书的ISBN号，打印每本书前几页的读书笔记和用户头像

备注：本地已保存有175本书的书名和ISBN号

语言：Python

软件：Spyder(Python 3.6)

调用的库：

selenium —— selenium 是一套完整的web应用程序测试系统，包含了测试的录制（selenium IDE）,编写及运行（Selenium Remote Control）和测试的并行处理（Selenium Grid）。Selenium的核心Selenium Core基于JsUnit，完全由JavaScript编写，因此可以用于任何支持JavaScript的浏览器上。selenium可以模拟真实浏览器，自动化测试工具，支持多种浏览器，爬虫中主要用来解决JavaScript渲染问题。

BeautifulSoup —— BeautifulSoup是Python的一个库，最主要的功能就是从网页爬取我们需要的数据。BeautifulSoup将html解析为对象进行处理，全部页面转变为字典或者数组，相对于正则表达式的方式，可以大大简化处理过程。

urllib —— Urllib库是Python中的一个功能强大、用于操作URL，并在做爬虫的时候经常要用到的库。在Python2.x中，分为Urllib库和Urllin2库，Python3.x之后都合并到Urllib库中，使用方法稍有不同。本次使用的是Python3中的urllib库。

pandas —— Python Data Analysis Library 或 pandas 是基于NumPy 的一种工具，该工具是为了解决数据分析任务而创建的。Pandas 纳入了大量库和一些标准的数据模型，提供了高效地操作大型数据集所需的工具。pandas提供了大量能使我们快速便捷地处理数据的函数和方法。你很快就会发现，它是使Python成为强大而高效的数据分析环境的重要因素之一。

缺点：不知道是不是time.sleep的时间太短了，爬到一定程度会被豆瓣认为是机器人，封ip,不过通常2-3个小时就会解封。尝试过用一个IP池，但网上免费IP通常都不能用。
