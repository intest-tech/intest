import attr
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


@attr.s
class Mail(object):
    subject = attr.ib()
    sender = attr.ib()
    sender_nickname = attr.ib()
    reciever = attr.ib()
    copy_reciever = attr.ib()

    def __attrs_post_init__(self):
        self.set_server()

    def get_mimetext(self, content):
        """
        设置邮件内容/发送者/接受者等信息
        :param content: 
        :return: 
        """
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = self.subject
        msg['From'] = formataddr([self.sender_nickname, self.sender])
        msg['to'] = ','.join(self.reciever)
        msg['cc'] = ','.join(self.copy_reciever)
        return msg.as_string()

    def set_server(self, server="smtp.exmail.qq.com", port=465):
        """
        设置邮件服务器
        :param server: 邮件服务器, 默认QQ企业邮箱
        :param port: 邮件服务器端口, 默认QQ企业邮箱
        :return: 
        """
        self.server = smtplib.SMTP_SSL(server, port)

    def login(self, password):
        """
        登录邮件服务器
        :param password: 
        :return: 
        """
        self.server.login(self.sender, password)

    def send(self, content="", autoclose=True):
        """
        发送邮件
        :param content: 发送的内容
        :param autoclose: 默认发送完成后关闭
        :return: 
        """
        self.server.sendmail(self.sender,
                             self.reciever + self.copy_reciever,
                             self.get_mimetext(content))
        if autoclose is True:
            self.server.quit()


def add_domain(name_list: list, domain: str) -> list:
    """
    为用户名添加邮箱后缀
    :param name_list: 不带邮箱后缀的用户名列表
    :param domain: 域名, 无需@符号
    :return: 添加了邮箱后缀的用户名列表
    """
    return [name + '@' + domain for name in name_list]


if __name__ == '__main__':
    # 示例
    my_sender = 'xxxxxxxxxxxxx'  # 发件人邮箱账号
    my_pass = 'xxxxxxxxxxxxx'  # 发件人邮箱密码
    dev_group = [
        'xxxxxxxxxxxxx',
    ]
    pm_group = [
        'xxxxxxxxxxxxx',
    ]

    recv_users = add_domain(dev_group, 'qq.com')
    cc_users = add_domain(pm_group, 'qq.com')

    mail = Mail(
        subject="default subject",
        sender=my_sender,
        sender_nickname="nickname",
        reciever=recv_users,
        copy_reciever=cc_users,
    )
    content = '这是邮件内容'
    mail.login(my_pass)
    mail.send(content=content)
