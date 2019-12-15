from flask import Flask, render_template, send_from_directory
import serial
import serial.tools.list_ports
import threading

app = Flask(__name__)

def run_server():
	app.run(host=bind_ip, debug=True, port=bind_port)

@app.route('/')
def index():
	return render_template('_basic.html', ports=serialhandler.get_port_list())

@app.route('/get/temp')
def get_angle():
	return str(serialhandler.temp_now)

@app.route('/open/<path:port>')
def open_serial(port):
	serialhandler.connect(port[1:])
	return '1'

@app.route('/static/<path:path>')
def send_static(path):
	return send_from_directory('static', path, as_attachment=False)



class SerialHandler(object):
	def __init__(self):
		self.Serial = serial.Serial()
		self.Serial.baudrate = 9600
		self.Serial.timeout = 0.5
		self.temp_now = 25.0
		self.q = ''

	def get_port_list(self):
		result = serial.tools.list_ports.comports()
		return result

	def connect(self, port):
		self.Serial.port = port
		self.Serial.open()
		threading.Timer(0.2, self.read_serial).start()

	def read_serial(self):
		threading.Timer(0.2, self.read_serial).start()
		try:
			while self.Serial.in_wating > 0:
				self.q += self.Serial.read().decode('utf-8')
		except:
			while self.Serial.inWaiting() > 0:
				self.q += self.Serial.read(1).decode('utf-8')
		splitted = self.q.split('\n\n')
		last = splitted[len(splitted)-1]
		if 'T_' in last:
			self.q = ''
			self.temp_now = (float) (last.split('_')[1].split('\n')[0])

if __name__ == '__main__':
	bind_ip = '127.0.0.1'
	bind_port = 8000
	serialhandler = SerialHandler()
	run_server()