from simulation import *

class Experiment:
    def __init__(self):
        self.simulation = None
        self.agentPos = [ -140.0, 20]
    
    def start(self, xmin, xmax, maxT ):
        self.simulation = Simulation( xmin, xmax, maxT )
        #a = AgentBuilder.buildSimpleTemperatureAgent( self.simulation.model.environment, 20.0, 20.0 )
        a1 = AgentBuilder.buildBraitenbergAgent2b( self.simulation.model.environment, self.agentPos[0], self.agentPos[1] )		
        a2 = AgentBuilder.buildBraitenbergAgent3a( self.simulation.model.environment, 140.0, 20.0 )		

        self.simulation.model.addAgent( a1 )
        self.simulation.model.addAgent( a2 )
        self.simulation.model.addFoodSource( -200, 100 )
        self.simulation.model.addFoodSource( 200, -50 )

        # self.simulation.model.addFoodSource( 100, 100 )
