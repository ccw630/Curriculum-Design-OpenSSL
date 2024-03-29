#include <stdio.h>
#include <openssl/evp.h>
#include <openssl/x509.h>
#include <openssl/ssl.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <sys/socket.h>
#include <netinet/in.h>  
#include "dlfcn.h"

#define CACERT "ca.crt"

#define CHK_ERR(err, s) if((err) == -1) { perror(s); return -1; }
#define CHK_RV(rv, s) if((rv) != 1) { printf("%s error\n", s); return -1; }
#define CHK_NULL(x, s) if((x) == NULL) { printf("%s error\n", s); return -1; }
#define CHK_SSL(err, s) if((err) == -1) { ERR_print_errors_fp(stderr);  return -1;}

int main()
{
	int rv;
	int err;
	int listen_sd;
	struct sockaddr_in socketAddrClient;
	SSL_METHOD *meth = NULL;
	SSL_CTX *ctx = NULL;
	SSL *ssl = NULL;
	char buf[4096];
	char* str;

	rv = SSL_library_init();
	CHK_RV(rv, "SSL_library_init");

	meth = SSLv23_client_method();
	ctx = SSL_CTX_new(meth);
	CHK_NULL(ctx, "SSL_CTX_new");

	SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL);
	SSL_CTX_load_verify_locations(ctx, CACERT, NULL);
	
	listen_sd = socket(AF_INET, SOCK_STREAM, 0);
	CHK_ERR(listen_sd, "socket");
	memset(&socketAddrClient, 0, sizeof(socketAddrClient));
	socketAddrClient.sin_family = AF_INET;
	socketAddrClient.sin_port = htons(8443);
	socketAddrClient.sin_addr.s_addr = inet_addr("127.0.0.1");

	err = connect(listen_sd, (struct sockaddr *)&socketAddrClient, sizeof(socketAddrClient));
	CHK_ERR(err, "connect");
	ssl = SSL_new(ctx);
	CHK_NULL(ssl, "SSL_new");
	rv = SSL_set_fd(ssl, listen_sd);
	CHK_RV(rv, "SSL_set_fd");
	rv = SSL_connect(ssl);
	CHK_RV(rv, "SSL_connect");

	X509* server_cert = SSL_get_peer_certificate(ssl);
    CHK_NULL(server_cert, "SSL_get_peer_certificate");
    printf ("Server certificate:\n");

    str = X509_NAME_oneline(X509_get_subject_name(server_cert),0,0);
    CHK_NULL(str, "X509_get_subject_name");
    printf ("\t subject: %s\n", str);
    free(str);

    str = X509_NAME_oneline (X509_get_issuer_name(server_cert),0,0);
    CHK_NULL(str, "X509_get_issuer_name");
    printf ("\t issuer : %s\n", str);
    free(str);

	rv = SSL_write(ssl, "Hello, I am the client", strlen("Hello, I am the client"));
	CHK_SSL(rv, "SSL_write");
	rv = SSL_read(ssl, buf, sizeof(buf) - 1);
	CHK_SSL(rv, "SSL_read");
	buf[rv] = '\0';
	printf("Got %d chars :%s\n", rv, buf);

	SSL_shutdown(ssl);
	close(listen_sd);
	SSL_free(ssl);
	SSL_CTX_free(ctx);

	return 0;
}
