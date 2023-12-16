#!/usr/bin/env python3

# Script goes here!
from models import Dev, Company, Freebie

# Companies
company1 = Company(name="AwesomeTech", founding_year=2010)
company2 = Company(name="SuperSoft", founding_year=2015)

# Developers
dev1 = Dev(name="Alice")
dev2 = Dev(name="Bob")

# Freebies
freebie1 = Freebie(item_name="T-shirt", value=10, dev=dev1, company=company1)
freebie2 = Freebie(item_name="Sticker", value=5, dev=dev2, company=company2)

# Adding data to session and commiting
session.add_all([company1, company2, dev1, dev2, freebie1, freebie2])
session.commit()

# Testing out
print(dev1.companies)  
print(company1.freebies)  
print(company2.give_freebie(dev1, "Mug", 20))  
print(dev1.received_one("Sticker"))  
