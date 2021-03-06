# --------------------------------------------------------------------
# Agent: Represents the physical body of the 
# --------------------------------------------------------------------
import numpy as np
from sensors import *
from brainsv2 import *
from body import *
import matplotlib.pyplot as plt

class AgentBuilder:
	@staticmethod
	def buildSimpleTemperatureAgent( environment, x, y ):
		# Sensors
		tempSensorL = TemperatureSensor( ego_angle = -np.pi/2.0, environment = environment )
		tempSensorR = TemperatureSensor( ego_angle = np.pi/2.0, environment = environment )
		# Brain
		brain = SimpleBrain()
		brain.registerSensor( 'Tl', tempSensorL )
		brain.registerSensor( 'Tr', tempSensorR )		

		# Agent
		a = Agent( environment, brain, x = x, y = y, theta = np.pi/2.0 )
		a.addSensor( tempSensorR )
		a.addSensor( tempSensorL )

		return a

	@staticmethod
	def buildBraitenbergAgent2a( environment, x, y ):
		# Sensors
		chemSensorL = ChemicalSensor( ego_angle = -np.pi/2.0, environment = environment )
		chemSensorR = ChemicalSensor( ego_angle = np.pi/2.0, environment = environment )
		# Brain
		brain = Braitenberg2a()
		brain.registerSensor( 'Fl', chemSensorL )
		brain.registerSensor( 'Fr', chemSensorR )		

		# Agent
		a = Agent( environment, brain, x = x, y = y, theta = np.pi/2.0 )
		a.addSensor( chemSensorL )
		a.addSensor( chemSensorR )

		return a

	@staticmethod
	def buildBraitenbergAgent2b( environment, x, y ):
		# Sensors
		chemSensorL = ChemicalSensor( ego_angle = -np.pi/2.0, environment = environment )
		chemSensorR = ChemicalSensor( ego_angle = np.pi/2.0, environment = environment )
		# Brain
		brain = Braitenberg2b()
		brain.registerSensor( 'Fl', chemSensorL )
		brain.registerSensor( 'Fr', chemSensorR )		

		# Agent
		a = Agent( environment, brain, x = x, y = y, theta = np.pi/2.0 )
		a.addSensor( chemSensorL )
		a.addSensor( chemSensorR )

		return a

	@staticmethod
	def buildBraitenbergAgent3a( environment, x, y ):
		# Sensors
		chemSensorL = ChemicalSensor( ego_angle = -np.pi/2.0, environment = environment )
		chemSensorR = ChemicalSensor( ego_angle = np.pi/2.0, environment = environment )
		# Brain
		brain = Braitenberg3a()
		brain.registerSensor( 'Fl', chemSensorL )
		brain.registerSensor( 'Fr', chemSensorR )		

		# Agent
		a = Agent( environment, brain, x = x, y = y, theta = np.pi/2.0 )
		a.addSensor( chemSensorL )
		a.addSensor( chemSensorR )

		return a

	@staticmethod
	def buildBraitenbergAgent3b( environment, x, y ):
		# Sensors
		chemSensorL = ChemicalSensor( ego_angle = -np.pi/2.0, environment = environment )
		chemSensorR = ChemicalSensor( ego_angle = np.pi/2.0, environment = environment )
		# Brain
		brain = Braitenberg3b()
		brain.registerSensor( 'Fl', chemSensorL )
		brain.registerSensor( 'Fr', chemSensorR )		

		# Agent
		a = Agent( environment, brain, x = x, y = y, theta = np.pi/2.0 )
		a.addSensor( chemSensorL )
		a.addSensor( chemSensorR )

		return a

	@staticmethod
	def buildMotivationalAgent( environment, x, y ):
		# Sensors
		tempSensorL = TemperatureSensor( ego_angle = -np.pi/2.0, environment = environment )
		tempSensorR = TemperatureSensor( ego_angle = np.pi/2.0, environment = environment )
		chemSensorL = ChemicalSensor( ego_angle = -np.pi/2.0, environment = environment )
		chemSensorR = ChemicalSensor( ego_angle = np.pi/2.0, environment = environment )

		# Brain
		brain = MotivationalBrain( Tb = 37.0, E = 1.0 )
		brain.registerSensor( 'Tl', tempSensorL )
		brain.registerSensor( 'Tr', tempSensorR )	
		brain.registerSensor( 'Fl', chemSensorL )
		brain.registerSensor( 'Fr', chemSensorR )

		# Agent
		a = Agent( environment, brain, x = x, y = y, theta = np.pi/2.0 )
		a.addSensor( tempSensorR )
		a.addSensor( tempSensorL )
		a.addSensor( chemSensorR )
		a.addSensor( chemSensorL )

		return a	

class Agent:

	def __init__(self, environment, brain, x, y, theta, radius = 2.0 ):
		
		self.body = Body(x, y, theta0 = theta)
		# Setting up brain and recorder
		if brain is not None:
			self.recorder = Recorder( brain )
			brain.setBody( self.body )

		self.brain = brain
		self.environment = environment
		self.sensors = []

		self.updateSensorPositions( x, y, theta )

	def getTransformation( self, x, y, theta ):
		return np.array([[np.cos(theta), -np.sin(theta), x], 
						 [np.sin(theta), np.cos(theta), y], 
						 [0, 0, 1]])

	def updateSensorPositions( self, x, y, theta ):
		p = np.array([self.body.radius, 0, 1])
		M = self.getTransformation( x, y, theta )

		for s in self.sensors:
			R = self.getTransformation( 0, 0, s.ego_angle )
			new_pos = np.dot(M, np.dot(R, p))
			s.setPosition( new_pos[0].item(), new_pos[1].item() )

	def addSensor( self, sensor ):
		self.sensors.append( sensor )

	def reset( self, tf, h ):
		m = int(tf/h)
		self.recorder.reset( m + 1 )
		self.brain.reset()
		self.body.reset()

	def step( self, h, t ):
		x,y = self.body.getPosition()

		self.recorder.recordSnapshot( t, x, y, self.brain )

		F = self.environment.getFood( x, y )
		self.brain.step( h, t, F )

		x,y = self.body.getPosition()
		theta = self.body.getOrientation()
		
		self.updateSensorPositions( x, y, theta )

	def clone( self ):
		a = Agent( self.environment, None, self.body.x[0], self.body.x[1], self.body.theta )
		
		a.recorder = self.recorder.clone()
		a.sensors = [s.clone() for s in self.sensors]

		return a


