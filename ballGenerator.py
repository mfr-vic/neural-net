from defs import *
from ball import Ball

class BallGenerator():
	def __init__(self, gameDisplay):
		self.gameDisplay = gameDisplay
		self.ball = Ball(self.gameDisplay);
		self.next_ball_in = BALL_GENERATOR_TIME_SPAN
		# self.create_ball()

	def get_balls(self):
		return self.balls

	def create_ball(self):
		ball = Ball(self.gameDisplay)
		self.ball = ball;

	def update(self, dt):
		self.update_ball(dt)

	def update_ball(self, dt):
		self.ball.update(dt);
		if(self.ball.is_active() == False):
			self.create_ball();
			
	def should_generate_ball(self):
		return self.next_ball_in == 0

	def reset(self):
		self.next_ball_in = BALL_GENERATOR_TIME_SPAN
		self.create_ball()