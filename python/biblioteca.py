from faker import Faker

fake = Faker(locale='pt-BR')

print(fake.email())

print(fake.name())

print(fake.date_of_birth())
