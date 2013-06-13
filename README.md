# Topo Builder

Topo Builder是一个持续集成（Continuous Integration）工具，帮助研发团队更好的展开持续集成。

![](https://github.com/cloudtopo/topo-builder/raw/master/builder/static/images/builder_home.png)

* Topo Builder可以创建多个自动调度的构建任务。
* 构建任务可以设置类似Unix cron格式的调度器，非常灵活的来定时调度。还可以手动指定Job运行，甚至可以强制指定构建任意历史版本。
* 构建和版本管理系统（Subversion）关联。
* 每个构建的完整log记录以及构建生成的目标文件都会被保存，log记录和构建目标文件可以方便的浏览和下载。
* 构建成功与否可以非常灵活的定义，可以根据构建记录，构建命令返回值，或是构建花费时间，或任何Python表达式来灵活定义。
* 构建结束后可以发送邮件，收件人可以在Job定义中预定义，可以根据构建成功或是失败定义不同的收件人。
* 易用的Web界面，项目成员可以通过Web浏览任务及构建的结果，管理员可以通过Web界面配置构建任务。

## 环境

Topo Builder需要在Windows下运行，下载后即可使用，无需安装，因为构建和SVN关联，因此需要在运行Topo Builder的机器上安装好SVN，否则Builder启动时会报错。

## 下载

直接下载zip包，或者运行下面的git命令：

	$ git clone git://github.com/cloudtopo/topo-builder.git builder

## 使用

双击 builder.bat 就可以启动 Topo Builder，启动成功后，在浏览器打开 http://localhost:8000 就可以了。

