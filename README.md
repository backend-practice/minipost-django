## MiniPost后台Django实现

[https://minipost-django.herokuapp.com/](https://minipost-django.herokuapp.com/)

[![Build Status](https://travis-ci.org/backend-practice/minipost-django.svg?branch=master)](https://travis-ci.org/backend-practice/minipost-django)

### 环境配置

* 代码缩进风格：editorconfig，配置文件[.editorconfig](.editorconfig)
* 代码风格检查：flake8，配置文件[setup.cfg](setup.cfg)
* import顺序：isort，配置文件[setup.cfg](setup.cfg)

### 依赖关系

* Django 2.1

* Django-REST-Framework

* drf-yasg 用于文档生成

详细的依赖见[requirements.txt](requirements.txt)

### CI/CD

持续集成通过Travis实现，参加[.travis.yml](.travis.yml)配置文件，完成自动构建测试和部署。

#### 构建
Django项目不需要构建。
TODO: 构建Docker镜像

#### 测试
* 通过flake8和isort进行代码风格检查
* 运行``python manage.py test``运行单元测试

#### 部署
部署到heroku，参考[Heroku文档](https://devcenter.heroku.com/articles/getting-started-with-python)
和[Travis文档](https://docs.travis-ci.com/user/deployment/heroku/)。
