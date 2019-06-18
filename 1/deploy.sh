gcc -w server.c -o server -g -lssl -lcrypto
gcc -w client.c -o client -g -lssl -lcrypto
rm -r *.dSYM