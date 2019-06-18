# Getting Started with OpenSSL

Developed as a curriculum design of computer network, under MacOS Mojave.

## 1.OpenSSL C/S Demo

### Dependency

```sh
brew install openssl
# REMEMBER CHANGE PATH TO OPENSSL
export CPATH="/usr/local/Cellar/openssl/1.0.2r/include:$CPATH"
export LIBRARY_PATH="/usr/local/Cellar/openssl/1.0.2r/lib:$LIBRARY_PATH"
```

### Installation

```sh
cd 1
./gen.sh    # Generate CA & Server Certification
./deploy.sh # Compile Server & Client
```

Note: The pass phrase for `server.key` is `1111`

### Usage

* Firstly, start the server.

```sh
./server
```

* Open a new terminal window, and start the client.

```sh
./client
```


## 2.Safe Online Paying Demo

### Background

Here's an old(before 2010?) ICBC pay API.
```html
<form name=" sendOrder " method="post" action="http://某网上银行支付服务器IP地址 / servlet/com.MerPayReqServlet ">  
<input type="text" name="merchantid" value="020000010001" >    --商城代码  
<input type="text" name="interfaceType" value="HS" >  --接口类型 
<input type="text" name="merURL" value="http://www.icbc_mert.com/toIcbcPay.asp" >  --接收支付结果信息的程序名称和地址  
<input type="text" name="orderid" values="12345678912345" >  --订单号 
<input type="text" name="amount" value="10056" >   --订单总金额（以分为单位） 
<input type="text" name="curType" value="001" >   --币种  
<input type="text" name="hsmsgType" value="0" >   --信息发送类型  
<input type="text" name="signMsg" value="LKJDFKF#$LKJFDA090980LKJAFK…">   --BASE64编码后的交易数据签名信息  
<input type="text" name="cert" value="%$#%#KLLK4LKJLJ67LJ8L54LH67L…">     --BASE64编码后的商户CA证书  
<input type="text" name="comment1" value=" " >   --备注字段 
<input type="submit" value="网银支付">  
</form>
```
This project implemented a simple ICBC CGI and a simple server. After posting a static form in HTML, ICBC CGI will receive it and check the certification and signature in it,then establish an SSL connection with server(URL set in *merURL* form item).

### Dependency

```sh
pip3 install pyopenssl
```

### Installation

```sh
cd 2
./gen.sh    # Generate CA & Server Certification
./sign.sh   # Generate data and signature with certification
```

### Usage

* Firstly, start server.
```sh
python3 server.py
```

* Open a new terminal window, and start the ICBC CGI.
```sh
python3 ICBC.py
```

* Then, open `form.html`, check the server URL, and fill in the two textarea. 

* Copy the content of `signature` into the **right** textarea.

```sh
pbcopy < signature
```

* Copy the content of `server.crt` into the **right** textarea.

```sh
pbcopy < server.crt
```

* Submit the form.