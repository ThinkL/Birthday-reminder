# coding:utf-8

from email.mime.text import MIMEText
import smtplib
from email import encoders
from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.multipart import MIMEMultipart,MIMEBase


#默认为QQ邮箱服务器，可以自行修改；
def mail_send_service(from_addr,password,to_addr,content=None,smtp_sever = 'smtp.qq.com',content_type ='plain',filepath = []):

    #用于构造邮件的from、to以及subject
    def _format_addr(s):
        name,addr = parseaddr(s)
        return formataddr((Header(name,'utf-8').encode(),addr))

    #发送方账号、密码
    from_add = from_addr
    password = password
    #接收方账号密码
    to_addr = to_addr
    #smtp服务器地址
    smtp_sever = smtp_sever


    #构造邮件正文及发送人、接收人、主题格式
    msg =MIMEMultipart()

    msg.attach(MIMEText(content, content_type, 'utf-8'))

    # 为邮件添加附件
    if filepath:
        for path,num in zip(filepath,range(len(filepath))):
            filetype = path.split('.')[-1]
            filename = path.split('\\')[-1]
            with open(path,'rb') as f:
                mime = MIMEBase(None,filetype,filename = filename)
                #加上必要的头信息
                mime.add_header('Content-Disposition', 'attachment', filename=filename)
                mime.add_header('Content-ID','<%s>' % num)
                mime.add_header('X-Attachment-Id','<%s>' % num)
                #把附件内容读进来
                mime.set_payload(f.read())
                #使用base_64进行编码
                encoders.encode_base64(mime)
                #添加到MIMEMultipart
                msg.attach(mime)

	
	#邮件from、to、object显示内容，可以自行修改
    msg['From'] = _format_addr('Think<%s>' % from_add)
    msg['To'] = _format_addr('You<%s>' % to_addr)
    msg['Subject'] = Header('Thinking...','utf-8').encode()



    #执行操作，QQ服务器是通过SSL进行信息传输的
    sever = smtplib.SMTP_SSL('smtp.qq.com',465)
    # sever.set_debuglevel(1)
    sever.login(from_add,password)
    sever.sendmail(from_add,[to_addr],msg.as_string())
    sever.quit()



if __name__ == '__main__':
    from_addr = to_addr = 'your email address'
    password = 'your password'
    content = 'your email content'
	#附件路径
    filepath = []
    mail_send_service(from_addr=from_addr,password=password,to_addr=to_addr,content=content,filepath=filepath)

