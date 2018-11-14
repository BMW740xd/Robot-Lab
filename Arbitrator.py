class Arbitrator:

    def __init__(self, controller_object):
        # en liste med alle active_behaviors fra bbcon
        self.controller = controller_object
        self.active_behaviors = self.controller.active_behavior_list

    def choose_action(self):
        # velger den oppførselen med størst vekt
        winner = 0
        winning_action = None
        action = ()  # lager en tuppel
        for i in range(len(self.active_behaviors)):  # går gjennom alle elementene i listen med active_behaviors
            print(self.active_behaviors[i].behavior, " = ", self.active_behaviors[i].weight)
            if self.active_behaviors[i].weight > winner:  # sjekker om neste behavior er større en winner
                winner = self.active_behaviors[i].weight  # setter winner til den nye behavior med større vekt
                winning_action = self.active_behaviors[i]  # setter winning_action til den nye behavior
            action = (winning_action.motor_recommendations,
                      winning_action.halt_request)  # legger til behavior og en boolean om behavior skal bli stoppet
        print(action)
        return action  # returnerer tuppelen
