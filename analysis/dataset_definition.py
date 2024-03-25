from ehrql import (
    create_dataset,
    codelist_from_csv,
)
from ehrql.tables.tpp import (
    patients,
    clinical_events,
    emergency_care_attendances,
)
from datetime import date, timedelta

first_lockdown_date = date(2023, 3, 23)
year_before_lockdown = first_lockdown_date - timedelta(weeks=52)

pre_covid_dataset = create_dataset()

#this isn't working but not needed for now
#emergency_admission_codelist = codelist_from_csv('codelists/emergency_admission_codelist.csv',
#                                                 column = 'code')



#variables
pre_covid_dataset.sex = patients.sex
pre_covid_dataset.age = patients.age_on(year_before_lockdown)

#this line should look at discharge destination
pre_covid_dataset.discharged_home = (emergency_care_attendances
.sort_by(emergency_care_attendances.arrival_date)
.last_for_patient()
.discharge_destination == 19 
    #19 is discharge to usual home or no abode
)


#with regards to last condition, 
#not sure if this is how I specify that the patient had an admission
pre_covid_dataset.define_population((patients.age_on(year_before_lockdown)>18)
                                    & (patients.exists_for_patient())
                                    & emergency_care_attendances.
                                    arrival_date.exists_for_patient())