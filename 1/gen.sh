rm *.key *.crt *.csr *.srl
openssl req -newkey rsa:2048 -nodes -keyout ca.key -x509 -days 365 -out ca.crt -subj "/C=CN/ST=Jilin/L=Changchun/O=CUST/OU=1605112/CN=w630.ca/emailAddress=ca@w630.cc"
openssl genrsa -aes256 -passout pass:1111 -out server.key 2048
openssl rsa -in server.key -out server.key
openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=Jilin/L=Changchun/O=CUST/OU=1605112/CN=w630.cc/emailAddress=me@w630.cc"
openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt