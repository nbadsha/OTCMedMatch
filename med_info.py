class Medicine(object):

    def __init__(self, med_name, med_des, med_use, med_sideeffect):
        self.med_name = med_name
        self.med_des = med_des
        self.med_use = med_use
        self.med_sideffet = med_sideeffect

    def insert(self):
        return """
        INSERT INTO med_info 
        VALUES(
            NULL,
            '{}',
            '{}',
            '{}',
            '{}'
        )
        """.format(self.med_name, self.med_des, self.med_use, self.med_sideffet)