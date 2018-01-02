import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine

machine = TocMachine(
					 states=[
							 'modeSelection',
							 'stock',
							 'currency'
							 'makeOrder'
							 ],
					 transitions=[
								  {
								  'trigger': 'stockTermsTriggered',
								  'source': 'modeSelection',
								  'dest': 'stock',
								  
								  },
								  {
								  'trigger': 'currencyTermsTriggered',
								  'source': 'modeSelection',
								  'dest': 'currency',
								  },
								  {
								  'trigger': 'currencyTermsTriggered',
								  'source': 'stock',
								  'dest': 'currency'
								  },
								  {
								  'trigger': 'stockTermsTriggered',
								  'source': 'currency',
								  'dest': 'stock'
								  },
								  {
								  'trigger': 'buy',
								  'source': 'stock',
								  'dest': 'order'
								  },
								  {
								  'trigger': 'cancel',
								  'source': 'order',
								  'dest': 'stock'
								  },
								  {
								  'trigger': 'orderConfirmed',
								  'source': 'order',
								  'dest': 'modeSelection'
								  }
								  ],
					 initial='modeSelection',
					 auto_transitions=False,
					 show_conditions=True,
					 )


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
	byte_io = BytesIO()
	machine.graph.draw(byte_io, prog='dot', format='png')
	byte_io.seek(0)
	return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')
