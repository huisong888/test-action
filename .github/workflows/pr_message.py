import os
import json
import fsbot

pr_title = os.environ.get("pr_title", "")
pr_url = os.environ.get("pr_url", "")
pr_user = os.environ.get("pr_user", "")
pr_type = os.environ.get("pr_type", "")
reviewers = os.environ.get("reviewers", [])
review_user = os.environ.get("review_user", "")
merge_user = os.environ.get("merge_user", "")

ios_id_dic = {
    "yyc324": "ou_6dc12399b2c4ee4c10b9f77072455f42",
    "pointone-tww": "ou_6d0f27e25853db4bebabd4e87b3c0555",
    "zhangyuncheng-bud": "ou_bb20873f7eaedaea6fe1ce0c592525c6",
    "DarrenWang628": "ou_d2034ed0489dd507014b41b256f12785",
    "sawamula": "ou_6417f5d0435ad3ecb0e562783ebdf9f5",
    "liuhaojian-pointone": "ou_cd3018f0daa614a0ca02e1b6b8ee3854",
    "wangfangping-pointone": "ou_23a6e3e9d258303297ea109fd7f6af8f",
    "lihuikang": "ou_6d59bc1598881e0e42a26434c7f0cb01",
    "shawnlinnn": "ou_e0f13ed8f46ff6054ce64a08ee8886b9",
    "risaFeng": "ou_eeef9f3c054c57d6bdb43fb99b363ca2",
    "Steve-Zou": "ou_e21da98fe103d524c14c93405731988c",
    "huisong888": "ou_3eb6a3cdad8730f62980f7bb2d126c55",
    "leoyox": "ou_49c887448e89de44144b9c0ea609c170",
    "bud-chenming": "ou_1b3237d5556b3ee08e7e709e3559a393",
    "budxuchunfa": "ou_d96ed2e7749b7809d7e08d33db946103",
    "xuhaozhi2": "ou_b32e0208a38ba8c1de3a7ba002e12365",
    
}

class PrNotification():
    def __init__(self):
        '''
        机器人初始化
        :param webhook: 飞书群自定义机器人webhook地址
        :param secret: 机器人安全设置页面勾选“加签”时需要传入的密钥
        :param content: 富文本初始化内容
        '''

        self.webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/4c6c0f43-9b64-4411-8692-0e6cde615c59'
        self.secret = ''
        if pr_type == 'reviewed':
            self.event_name = 'BUD-Backend (global) Request Approved ✅ '
            self.content = self.pr_reviewed_content(
                pr_title, pr_user, pr_url)
        elif pr_type == 'created':
            self.event_name = 'BUD-Backend (global) Pull Request 🚀 '
            self.content = self.pr_create_content(
                pr_title, pr_user, pr_url)
        elif pr_type == 'merged':
            self.event_name = 'BUD-Backend (global) Pull Request Merged 👏 '
            self.content = self.pr_merged_content(
                pr_title, pr_user, pr_url)

    def send_message(self):
        '''
        发送消息
        '''
        if pr_type == 'created':
            self.content.append(self.get_at_list(reviewers))
        feishu = fsbot.FeiShuMessageBot(self.webhook, secret=self.secret)
        rich_text = self.create_rich_text(self.event_name, self.content)
        feishu.post(rich_text)

    def get_at_list(self, reviewers):
        '''
        生成@用户富文本
        :param reviewers: pull request中要求reivew的人
        '''
        at_lsit = [{
            "tag": "text",
            "text": '代码审查：'
        }, ]
        reviewers_list = json.loads(reviewers)
        print(reviewers_list)
        for reviewer in reviewers_list:
            username = reviewer["login"]
            at_tag = {"tag": "at", "user_id": ios_id_dic.get(username, "")}
            at_lsit.append(at_tag)
        return at_lsit

    def pr_create_content(self, desc, user, url):
        '''
        初始化PR创建富文本内容
        :param desc: PR描述
        :param user: 发起user的人
        '''
        content = [
            [
                {
                    "tag": "text",
                    "text": '描述：' + desc
                },
            ],
            [],
            [
                {
                    "tag": "text",
                    "text": '发起人：'
                },
                {
                    "tag": "at",
                    "user_id": ios_id_dic.get(user, "")
                }
            ],
            [],
            [
                {
                    "tag": "text",
                    "text": 'PR链接：'
                },
                {
                    "tag": "a",
                    "text": "点击查看",
                    "href": url
                }
            ],
            [],
        ]
        return content

    def pr_reviewed_content(self, desc, user, url):
        '''
        初始化PR完成代码审查富文本内容
        :param desc: PR描述
        :param user: 发起user的人
        '''
        content = [
            [
                {
                    "tag": "text",
                    "text": '描述：' + desc
                },
            ],
            [],
            [
                {
                    "tag": "text",
                    "text": '发起人：'
                },
                {
                    "tag": "at",
                    "user_id": ios_id_dic.get(user, "")
                }
            ],
            [],
            [
                {
                    "tag": "text",
                    "text": 'PR链接：'
                },
                {
                    "tag": "a",
                    "text": "",
                    "href": url
                }
            ],
            [],
            [
                {
                    "tag": "text",
                    "text": '审查人：'
                },
                {
                    "tag": "at",
                    "user_id": ios_id_dic.get(review_user, "")
                }
            ],
        ]
        return content

        def pr_merged_content(self, desc, user, url):
                '''
                初始化PR完成代码审查富文本内容
                :param desc: PR描述
                :param user: 发起user的人
                '''
                content = [
                    [
                        {
                            "tag": "text",
                            "text": '描述：' + desc
                        },
                    ],
                    [],
                    [
                        {
                            "tag": "text",
                            "text": '发起人：'
                        },
                        {
                            "tag": "at",
                            "user_id": ios_id_dic.get(user, "")
                        }
                    ],
                    [],
                    [
                        {
                            "tag": "text",
                            "text": 'PR链接：'
                        },
                        {
                            "tag": "a",
                            "text": "",
                            "href": url
                        }
                    ],
                    [],
                    [
                        {
                            "tag": "text",
                            "text": '合并人：'
                        },
                        {
                            "tag": "at",
                            "user_id": ios_id_dic.get(merge_user, "")
                        }
                    ],
                ]
                return content

    def create_rich_text(self, title, content):
        '''
        创建富文本
        :param title: 标题
        :param content: 富文本内容
        '''
        rich_text = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }
                }
            }
        }
        return rich_text

if __name__ == '__main__':
    noti = PrNotification()
    noti.send_message()
