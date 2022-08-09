from sys import argv

from module.controller import Controller

controller: Controller = Controller()
controller.run(argv)
