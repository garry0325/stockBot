from transitions.extensions import GraphMachine

class stockMachine(GraphMachine):
	def __init__(self, **machine_configs):
		self.machine=GraphMachine(
			model=self,
			**machine_configs
		)


