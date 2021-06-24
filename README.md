# Braitenberg
A simulator of vehicles with different kind of brains

## Requeriments
- python2.7
- Qt5

## General usage
1. Instantiate the class experiments adding agents with the different brains available (or personalized)

```python
class MyExperiment(Experiment):
    """ 
    Example experiment with basic braitenberg vehicles
    """
    def __init__(self):
        super(MyExperiment, self).__init__()
    
    def start(self, xmin, xmax, maxT ):
        self.simulation = Simulation( xmin, xmax, maxT )
        a1 = AgentBuilder.buildBraitenbergAgent2a( self.simulation.model.environment, -180.0, 20.0 )		
        a2 = AgentBuilder.buildBraitenbergAgent3a( self.simulation.model.environment, 100.0, 20.0 )		

        self.simulation.model.addAgent( a1 )
        self.simulation.model.addAgent( a2 )
        self.simulation.model.addFoodSource( -200, 100 )
        self.simulation.model.addFoodSource( 200, -50 )
```

2. Create a Window object sending as a parameter your experiment

```python
if __name__ == '__main__':

	app = QApplication( sys.argv )
	e = MyExperiment()
	window = MainWindow( e )
	window.show()

	app.exec_()
```
 
 To execute the example, type:
 `python braitenberg.py`
 
