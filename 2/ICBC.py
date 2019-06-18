import socket
import ssl
import pprint

from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi

import OpenSSL
import base64
import traceback

def verify_certificate(certificate):
	try:
		store = OpenSSL.crypto.X509Store()
		ca = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open('ca.crt').read())
		store.add_cert(ca)

		store_ctx = OpenSSL.crypto.X509StoreContext(store, certificate)

		store_ctx.verify_certificate()
		return True
	except:
		traceback.print_exc()
		return False

class PostHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		form = cgi.FieldStorage(fp=self.rfile,
								headers=self.headers,
								environ={
									'REQUEST_METHOD': 'POST',
									'CONTENT_TYPE':
									self.headers['Content-Type'],
								})

		self.send_response(200)
		self.end_headers()
		for field in form.keys():
			field_item = form[field]
			print(field,field_item.value)
		try:
			certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, form['cert'].value)
		except:
			traceback.print_exc()
			certificate = None
		if not verify_certificate(certificate):
			self.wfile.write(b'Certification in your form is invalid.')
			return
		try:
			signature = base64.b64decode(form['signMsg'].value)
			OpenSSL.crypto.verify(certificate, signature, 'true data\n', 'sha1')
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				ip = form['merURL'].value.split(':')[0]
				port = int(form['merURL'].value.split(':')[1].replace('/','')) if ':' in form['merURL'].value else 8080
				ssl_s = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs="ca.crt")
				ssl_s.connect((ip, port))
				print("Merchant Certificate Info")
				pprint.pprint(ssl_s.getpeercert())
				ssl_s.send(b'ICBC Transaction Acquired')
				self.wfile.write(b'ICBC has acquired your transaction, please check whether our server received response from ICBC in terminal.')
				data = ssl_s.recv(1024)
				print("Merchant Reply:", data.decode("utf-8") )
				ssl_s.close()
			except:
				traceback.print_exc()
				self.wfile.write(b'Connection Error.')
		except:
			traceback.print_exc()
			self.wfile.write(b'ICBC did not accept your transaction due to wrong signature or certification.')

		return
	def do_GET(self):
		return

sever = HTTPServer(("", 18888), PostHandler)
sever.serve_forever()
