# doubanmeizi
#### 抓取豆瓣妹子网站的图片

**PS**：  
1. 项目使用scrapy框架集成。  
2. 项目集成了Pipeline，下载的图片，会自动保存。  
3. 保存的目录，可以在项目中的setting.py中设置，必须设置一个可访问的文件夹路径，否则，文件不会被保存。  

```python

# Images store path
IMAGES_STORE = 'path/to/same/images'

```   

**使用如下命令，运行spider**  
`scrapy crawl douban`
