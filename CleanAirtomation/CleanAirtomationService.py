class CleanAirtomationService:

    def __init__(self, caqi_treshold, airly_dao, air_purifier):
        self.airly_dao = airly_dao
        self.air_purifier = air_purifier
        self.caqi_treshold = caqi_treshold

    def clean_polluted_air(self):
        current_caqi = self.airly_dao.caqi()
        print("current caqi value " + str(current_caqi))
        if current_caqi is not None:
            if current_caqi > self.caqi_treshold:
                print('CAQI above treshold, state of purifier = ' + str(self.air_purifier.get_state()))
                if self.air_purifier.get_state() == 0:
                    print('bad air - purifier needs to be switched on')
                    on_status = self.air_purifier.turn_on()
                    print('air purifier turn on with status ' + str(on_status))

            else:
                print('CAQI below treshold, state of purifier = ' + str(self.air_purifier.get_state()))
                if self.air_purifier.get_state() == 1:
                    print('good air - purifier needs to be switched off')
                    off_status = self.air_purifier.turn_off()
                    print('air purifier turn off with status ' + str(off_status))
        else:
            print('Unable to get CAQI from Airly')
