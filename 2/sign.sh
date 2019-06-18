echo "true data" > data
openssl dgst -sha1 -sign server.key -out tmp.sha1 data
openssl base64 -in tmp.sha1 -out signature
rm data tmp.sha1
