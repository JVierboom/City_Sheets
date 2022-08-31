from os import linesep
import random
import datetime

class City:

    # -------------------------------- constructor ------------------------------- #

    def __init__(self, city_type_code: int = 1, debug_enabled: bool = False):

        # variable declaration
        self.debug_enabled = debug_enabled

        self.population = 0
        self.min_stat = 0
        self.max_stat = 0
        self.first_speciality = ""
        self.second_speciality = ""

        self.specialities = dict()
        self.stats = dict()
        self.locations = dict()
        self.stat_names = {"crime", "culture", "health", "military", "order", "production", "recreation", "reputation", "tech", "trade", "wealth", "worship"}
        self.speciality_names = {"militaristic", "mercantile", "industrial", "education", "cultural", "agriculture"}

        # set city type and match type with type_code for calculations for population etc.
        city_types = dict({
            1: "Outpost",
            2: "Thorp",
            3: "Hamlet",
            4: "Village",
            5: "Small town",
            6: "Large town",
            7: "Small city",
            8: "Large city",
            9: "Metropolis",
            10: "Capital"
        })

        self.type = city_types[city_type_code]
        self.type_code = city_type_code

        # init dictionaries with stat names and speciality names to save heckloads of hard-coding.
        for name in self.stat_names:
            self.stats[name] = 0
            self.locations[name] = [" ", " ", " ", " ", " "]

        for speciality in self.speciality_names:
            self.specialities[speciality] = 0

    # ------------------------------- debug method ------------------------------- #

    def __log(self, debug_message: str):
        if self.debug_enabled:
            timestamp = datetime.datetime.now()
            file = open(f'./output/logs/city_sheet_{timestamp.strftime("%d-%m-%Y")}.log', 'a')
            file.write(f'[{timestamp.strftime("%H:%M:%S")}] - {debug_message}' + linesep)
            file.close()

    # ---------------------------------- methods --------------------------------- #

    def propogate_data(self):

        self.__log("# BEGIN DATA  PROPOGATION #")

        # generate population
        if self.type_code == 1:
            self.population = random.randint(10, 20)
        else:
            self.population = self.type_code ** 5
            self.population = int(random.uniform(self.population * 0.7, self.population * 1.3))

        self.__log(f"Population: {self.population}")

        # generate potential min/max for city stat RNG
        self.min_stat = int(self.type_code / 2 + 1)
        if self.type_code <= 7:
            self.max_stat = self.type_code + 1
        else:
            self.max_stat = self.type_code

        self.__log(f"Stat boundaries: {self.min_stat} - {self.max_stat}")

        # run RNG for stat numbers
        for stat in self.stats:
            self.stats[stat] = random.randint(self.min_stat, self.max_stat)
            self.__log(f"Stat generated for {stat}: {self.stats[stat]}")

        # set random location checkmarks per stat
        for stat, location_group in self.locations.items():
            # calculate how many locations need to be selected
            proficiency_weight = [0.6, 1.0, 1.4]
            proficiency = int((self.stats[stat] / 2) * proficiency_weight[random.randrange(len(proficiency_weight))])
            
            # toggle number of random locations based on proficiency
            locations_sample = random.sample(range(0, 5), proficiency)
            for index in locations_sample:
                self.locations[stat][index] = "x"

            self.__log(f"New locations for {stat}: {str(self.locations[stat])}")
            
        # calculate speciality sums. hard-coding to avoid recursion.
        self.specialities["militaristic"] = self.stats["military"] + self.stats["order"]
        self.specialities["mercantile"] = self.stats["trade"] + self.stats["wealth"]
        self.specialities["industrial"] = self.stats["production"] + self.stats["crime"]
        self.specialities["education"] = self.stats["tech"] + self.stats["worship"]
        self.specialities["cultural"] = self.stats["culture"] + self.stats["recreation"]
        self.specialities["agriculture"] = self.stats["health"] + self.stats["reputation"]

        self.__log(f"New specialities: {str(self.specialities)}")
        
        # assign highest 2 specialities to go on sheet

        for speciality, value in self.specialities.items():
            if self.first_speciality == "":
                self.first_speciality = speciality
            elif value >= self.specialities[self.first_speciality]:
                self.second_speciality = self.first_speciality
                self.first_speciality = speciality
            
        self.__log(f"New specialities: 1-{self.first_speciality} 2-{self.second_speciality}")

    # ---------------------------- getters and setters --------------------------- #

    def get_type(self):
        return self.type

    def get_population(self):
        return self.population

    def get_stat(self, stat_name: str):
        try:
            return self.stats[stat_name.lower()]
        except:
            return None

    def get_locations(self, stat_name: str):
        try:
            return self.locations[stat_name.lower()]
        except:
            return None

    def get_specialities(self):
        return [self.first_speciality, self.second_speciality]