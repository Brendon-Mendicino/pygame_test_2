import entities as ent

class Screen:

    def __init__(self):
        self.entities = {}


    def add_entity(self, entity):
        self.entities[entity.get_ent_id()] = entity

    def get_entities(self):
        return self.entities
