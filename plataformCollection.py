from plataformPopEvolver import Evolver


from defs import *
from plataform import Plataform
from neuralNet import NeuralNet


class PlataformCollection():
	def __init__(self, gameDisplay, ballGenerator):
		self.gameDisplay = gameDisplay
		self.plataforms = []
		self.create_generation()
		self.ballGenerator = ballGenerator
		self.active_plataforms = []
		self.generation = 1

	def create_generation(self):
		self.plataforms = []

		for i in range(GENERATION_SIZE):
			self.plataforms.append(Plataform(self.gameDisplay, NeuralNet()))

		self.active_plataforms = self.plataforms


	def update(self, dt):
		self.ballGenerator.update(dt)
		self.active_plataforms = self._get_active_plataforms()

		self._predict_movements()
		self._kill_losers()
		self._update_plataforms()


		if(self._all_died()):
			# self.create_generation()
			self._evolve()
			self.generation += 1
			self.ballGenerator.reset()

	def get_alive(self):
		return len(self.active_plataforms)

	def get_generation(self):
		return self.generation

	def gex_max_points(self):
		if(self._all_died()):
			return 0
		return self.active_plataforms[0].points

	def _get_active_plataforms(self):
		plat = []
		for plataform in self.active_plataforms:
			if (plataform.lost_game() == False):
				plat.append(plataform)

		return plat

	def _predict_movements(self):
		for plataform in self.active_plataforms:
			plataform.predict(self.ballGenerator)

	def _kill_losers(self):
		ball_is_in_catch_area = self._ball_is_in_catch_area()
		if(ball_is_in_catch_area):
			self._kill_all_that_didnt_catch()

	def _all_died(self):
		return len(self.active_plataforms) == 0

	def _ball_is_in_catch_area(self):
		ball = self.ballGenerator.ball
		return ball.is_inside(PLATAFORM_POSITION[1], PLATAFORM_POSITION[1] + PLATAFORM[1])

	def _kill_all_that_didnt_catch(self):
		ball = self.ballGenerator.ball

		for plataform in self.active_plataforms:
			plataform.try_to_catch(ball)					

	def _update_plataforms(self):
		for plataform in self.active_plataforms:
			plataform.update()


	def _evolve(self):
		evolver = Evolver(self.plataforms, self.gameDisplay)

		self.plataforms = evolver.evolve_population()
		self._reset_all()
		self.active_plataforms = self.plataforms

	
	def _reset_all(self):
		for plataform in self.plataforms:
			plataform.reset()