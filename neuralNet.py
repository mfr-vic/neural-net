import random
from defs import *
import numpy as np
from neuralNetBase import NeuralNetwork


class NeuralNet():

	def __init__(self):
		self.model = self.create_neural_model()


	def create_neural_model(self):
		model = NeuralNetwork()
		model.add_dense(4, input = 2)
		model.add_dense(2,  activation="softmax")
		model.compile()

		return model

	def predict(self, input):
		input = np.expand_dims(input, axis = 0)
		return self.model.predict(input)[0]

	def mutate(self):
		weights = self.model.get_weights()

		mutated_weights = []

		for weight in weights:
			mutated_weights.append(self._mutate_weight(weight))

		self.model.set_weights(mutated_weights)

	def get_weights(self):
		return self.model.get_weights()

	def _mutate_weight(self, weight):
		if(random.randrange(0, 1) > MUTATION_CHANCE):
			return weight + random.rand(-weight / 4, weight / 4)
		return weight


	def breed(parents):
		father = parents[random.randint(0, len(parents) - 1)]
		mother = parents[random.randint(0, len(parents) - 1)]

		child_weights = []

		father_weights = father.brain.get_weights()
		mother_weights = mother.brain.get_weights()
		for i in range(len(father_weights)):
			if(random.randrange(0,1) > 0.5):
				child_weights.append(father_weights[i])
			else:
				child_weights.append(mother_weights[i])

		child_brain = NeuralNet()
		child_brain.model.set_weights(child_weights)
		child_brain._mutate_child()

		return child_brain


	def _mutate_child(self):
		weights = self.model.get_weights()

		mutated_weights = []

		for weight in weights:
			mutated_weights.append(self._mutate_weight(weight))

		self.model.set_weights(mutated_weights)

	def _mutate_weight(self, weight):
		if(random.randrange(0, 1) > CHILD_MUTATION_CHANCE):
			return weight + random.rand(-weight / 4, weight / 4)
		return weight