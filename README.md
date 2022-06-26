
<img src="/TPMWeb/public/image/banner.jpeg" width="601" height="256" alt="微信小程序"/><br/>

<p align="center">
  <a href="https://github.com/vuejs/vue">
    <img src="https://img.shields.io/badge/vue-2.6.10-brightgreen.svg" alt="vue">
  </a>
  <a href="https://github.com/ElemeFE/element">
    <img src="https://img.shields.io/badge/element--ui-2.15.6-brightgreen.svg" alt="element-ui">
  </a>
  <a href="https://github.com/PanJiaChen/vue-element-admin/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="license">
  </a>
</p>

# 测试需求管理平台
背景源于多年前的团队的一个需求，这里重新利用最新开箱即用的前后端框架重新实现出来，并配有系列开发分享文章，宗旨是为做想测试开发和或自己想实现个小工具平台，而没有练手实战项目的同学提供一份的学习参考资料，希望对需要的人有些许帮助。

[在线体验](http://tpm.mrzcode.com/)

# 前后端服务
代码全部放在一个Git项目上了，但服务分为独立的前端和后端服务，同时也给出了对应SQL数据库创表语句。

## SQL
数据使用的Mysql，版本建议5.7+，本项目中使用的是8.0版本，SQL文件夹中分别提供的提测平台用到的几张表
- products.sql  产品/项目表
- apps.sql      应用表
- request.sql   提测需求和报告信息表

## TPMService
后端服务，使用的是 Python Flask框架，Pyton版本是3.x，同样本项目讲解的是需求应用的部分，至于更多内容建议学习官网 [英文](https://flask.palletsprojects.com/en/2.0.x/) [中文](https://dormousehole.readthedocs.io/en/latest/)，英文好的强力推荐阅读英文官方版本，中文的翻译可能是老版本，相关内容有些滞后。

### 如何运行

```bash
# 克隆项目
git clone https://github.com/mrzcode/TestProjectManagement.git

# 进入项目目录 或 用WebStorm等IDE工具导入前端项目
cd TPMService

# 安装依赖
pip3 install -r requirements.txt

# 启动服务 或者 PyCharm等IDE配置运行
python3 app.py

```

## TPMWeb
前端服务，使用的是开箱即用的 [Vue-element-admin](https://github.com/PanJiaChen/vue-admin-template)基础template版本，它还有个amdin版本有很多综合页面可以进行参考，基础组件应用上使用的 [Element ui](https://element.eleme.io/#/zh-CN)，这里需要注意的是你代码中使用的是Vue2.x版本，如果你是刚刚开始跟学这个项目，可以尝试将这些都升级到3.x进行练习开发。

关于前端的Vue开发，本项目只是讲了如何快速的应用，而不是深入的讲解vue前端开发的技能，在分享文章里也讲过，我们并不是要做前端开发，所以对于全栈的测试开发只要掌握如何应用到实际需求中就行，如果想进一步深入学习，可以参考Vue-element-admin、Vue等技术官网或者相关专业课程。

### 如何运行

```bash
# 克隆项目
git clone https://github.com/mrzcode/TestProjectManagement.git

# 进入项目目录 或 用WebStorm等IDE工具导入前端项目
cd TPMWeb

# 安装依赖
npm install

# 启动服务
npm run dev

# 如果npm install安装较慢可切换依赖源
npm install --registry=https://registry.npm.taobao.org

```
浏览器访问 [http://localhost:9528](http://localhost:9528)

### 感谢
这里鸣谢 Vue-element-admin个人 和 element ui团队的无私奉献，才让前端的开发更简单。


# 系列教程文章
## 公众号发布
### 汇总帖
[【提测平台】测试开发练手项目源代码和教程汇总](https://mp.weixin.qq.com/s/5Bn3SiO43L3wRZiuieiz5w)

### 顺序帖 
**基础内容篇**
- [提测平台1-基础-前端Vue&后端Flask框架介绍](https://mp.weixin.qq.com/s/rLX5WxwCc-g2LNwy3IT1SA)
- [提测平台2-基础-前后端分离服务打通联调](https://mp.weixin.qq.com/s/KaL3sw5vv9XbDQjlBphKvA)
- [提测平台3-基础-项目初始化与项目托管](https://mp.weixin.qq.com/s/rjLfwlLhef_H2MlYPmbPEw)

**原型和需求** 
- [提测平台-TPM产品原型和需求说明](https://mp.weixin.qq.com/s/AS5nTaQfJQutASfRd15PBw)

**需求实现篇**
- [提测平台4-开发-数据库绑定&实现产品线展示功能](https://mp.weixin.qq.com/s/qZtVa0ajiLiY9np2ySYPKA)
- [提测平台5-开发-实现产品线的添加需求功能](https://mp.weixin.qq.com/s/BNhcm06tuukIFQmzTPNIaQ)
- [提测平台6-开发-实现产品线修改功能](https://mp.weixin.qq.com/s/PSGooQRf2Vd2RumzhSAX-g)
- [提测平台7-开发-完成产品线删除功能](https://mp.weixin.qq.com/s/xhgTRv3zAUqER7TgqyJSRg)
- [提测平台8-开发-实现产品搜索&时间优化显示](https://mp.weixin.qq.com/s/oh4gsqX9k3Sxq3xZ_4EYXQ)

   --- 阶段小结一&阶段结二 ---

- [提测平台9-开发-DBUntils优化数据连接&实现应用搜索和分页功能](https://mp.weixin.qq.com/s/sfOA6BoVqsNcGczK7bGjPQ)
- [提测平台10-开发-Element UI抽屉和表单校验&增改接口合并实现应用管理](https://mp.weixin.qq.com/s/G00qvXA4eGMTrb-u9cO-uA)
- [提测平台11-开发-Python邮件发送方法&落地有邮件工具类](https://mp.weixin.qq.com/s/IKjnEEgVodwuhZ4amsqPmA)
- [提测平台12-开发-时间控件使用&Python联合表查询&实现提测搜索展示](https://mp.weixin.qq.com/s/N7-J3pWEfvkp0XfCrASSwQ)
- [提测平台13-开发-远程搜索和路由$route使用实现新建提测需求](https://mp.weixin.qq.com/s/9CLeKXPSGo2iHNS_UmDqrA)
- [提测平台14-开发-图标Icon几种用法并利用其一优化菜单](https://mp.weixin.qq.com/s/HzeRSzm8WSKTKw9d9-AkIw)
- [提测平台15-开发-实现提测单修改和邮件标记](https://mp.weixin.qq.com/s/gXLiJBHc7qdcyug8xw6CLQ)
- [提测平台16-开发-状态流转和提测详情展示](https://mp.weixin.qq.com/s/DKZvBRBr4B_EODuN4lP3jQ)
- [提测平台17-开发-Flask&Vue文件上传实现实践](https://mp.weixin.qq.com/s/GJiD-79hJsC_z64PwrC9RA)
- [提测平台18-开发-测试报告管理功能实现](https://mp.weixin.qq.com/s/Uvt7UxBiVpzG7lRukyY44A)

   --- 阶段小结三 ---

**拓展需求篇**
- [提测平台19-拓展-Echarts图表在项目的应用](https://mp.weixin.qq.com/s/vXZOs6LCn-vUwpBP6XslXA)
- [提测平台20-拓展-G2Plot如何使用简化报表开发](https://mp.weixin.qq.com/s/QS29iN0JQtrIVWJ_NZ91Ig)


**阶段总结篇**
- [阶段小结一：Python Flask API实现方法](https://mp.weixin.qq.com/s/CKIxTBbDRcjVAqlXzOVcHw)
- [阶段小结二：Element Vue开箱即用框架使用](https://mp.weixin.qq.com/s/c1GXsFP2D_ji3dvBZ_PAlA)
- [阶段小结三：开发回顾和内容梳理](https://mp.weixin.qq.com/s/iT7440izmXH3bypz5Omm-g)

**补充篇**
- [补充一：前后端服务部署正式环境的方案实践](https://mp.weixin.qq.com/s/RpHtav-hV4ra8_mck1WYIA)


## 纯享版
计划中重新排版存粹的教程版本，todo 敬请期待！

# 公众号
欢迎关注《大奇测试开发》，长期关注可以收获更多系列干货文章
<img src="/TPMWeb/public/image/wechat.png" width="548" height="200" alt="微信小程序"/><br/>


