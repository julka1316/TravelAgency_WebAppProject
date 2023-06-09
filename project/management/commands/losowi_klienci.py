
import random

from django.core.management.base import BaseCommand

from project.models import Customer

imiona_damskie = ['Anna', 'Maria', 'Katarzyna', 'Małgorzata', 'Agnieszka', 'Krystyna', 'Barbara', 'Ewa', 'Elżbieta',
                  'Zofia', 'Janina', 'Teresa', 'Joanna', 'Magdalena', 'Monika', 'Jadwiga', 'Danuta', 'Irena', 'Halina',
                  'Helena', 'Beata', 'Aleksandra', 'Marta', 'Dorota', 'Marianna', 'Grażyna', 'Jolanta', 'Stanisława',
                  'Iwona', 'Karolina', 'Bożena', 'Urszula', 'Justyna', 'Renata', 'Alicja', 'Paulina', 'Sylwia',
                  'Natalia', 'Wanda', 'Agata', 'Aneta', 'Izabela', 'Ewelina', 'Marzena', 'Wiesława', 'Genowefa',
                  'Patrycja', 'Kazimiera', 'Edyta', 'Stefania']
imiona_meskie = ['Jan', 'Andrzej', 'Piotr', 'Krzysztof', 'Stanisław', 'Tomasz', 'Paweł', 'Józef', 'Marcin', 'Marek',
                 'Michał', 'Grzegorz', 'Jerzy', 'Tadeusz', 'Adam', 'Łukasz', 'Zbigniew', 'Ryszard', 'Dariusz', 'Henryk',
                 'Mariusz', 'Kazimierz', 'Wojciech', 'Robert', 'Mateusz', 'Marian', 'Rafał', 'Jacek', 'Janusz',
                 'Mirosław', 'Maciej', 'Sławomir', 'Jarosław', 'Kamil', 'Wiesław', 'Roman', 'Władysław', 'Jakub',
                 'Artur', 'Zdzisław', 'Edward', 'Mieczysław', 'Damian', 'Dawid', 'Przemysław', 'Sebastian', 'Czesław',
                 'Leszek', 'Daniel', 'Waldemar']
nazwiska = ['Nowak', 'Kowalski', 'Wiśniewski', 'Dąbrowski', 'Lewandowski', 'Wójcik', 'Kamiński', 'Kowalczyk',
            'Zieliński', 'Szymański', 'Woźniak', 'Kozłowski', 'Jankowski', 'Wojciechowski', 'Kwiatkowski', 'Kaczmarek',
            'Mazur', 'Krawczyk', 'Piotrowski', 'Grabowski', 'Nowakowski', 'Pawłowski', 'Michalski', 'Nowicki',
            'Adamczyk', 'Dudek', 'Zając', 'Wieczorek', 'Jabłoński', 'Król', 'Majewski', 'Olszewski', 'Jaworski',
            'Wróbel', 'Malinowski', 'Pawlak', 'Witkowski', 'Walczak', 'Stępień', 'Górski', 'Rutkowski', 'Michalak',
            'Sikora', 'Ostrowski', 'Baran', 'Duda', 'Szewczyk', 'Tomaszewski', 'Pietrzak', 'Marciniak', 'Wróblewski',
            'Zalewski', 'Jakubowski', 'Jasiński', 'Zawadzki', 'Sadowski', 'Bąk', 'Chmielewski', 'Włodarczyk',
            'Borkowski', 'Czarnecki', 'Sawicki', 'Sokołowski', 'Urbański', 'Kubiak', 'Maciejewski', 'Szczepański',
            'Kucharski', 'Wilk', 'Kalinowski', 'Lis', 'Mazurek', 'Wysocki', 'Adamski', 'Kaźmierczak', 'Wasilewski',
            'Sobczak', 'Czerwiński', 'Andrzejewski', 'Cieślak', 'Głowacki', 'Zakrzewski', 'Kołodziej', 'Sikorski',
            'Krajewski', 'Gajewski', 'Szymczak', 'Szulc', 'Baranowski', 'Laskowski', 'Brzeziński', 'Makowski',
            'Ziółkowski', 'Przybylski']



class Command(BaseCommand):
    help = "Dodaje losowo wygenerowanych N studentów"

    def add_arguments(self, parser):
        parser.add_argument("N", type=int)

    def handle(self, *args, **options):
        for i in range(options['N']):
            surname = random.choice(nazwiska)
            if random.random() < 0.5:
                customername = random.choice(imiona_meskie)
            else:
                customername = random.choice(imiona_damskie)
                if surname.endswith('ski') or surname.endswith('cki') or surname.endswith('dzki'):
                    surname = surname.replace('ski', 'ska').replace('cki', 'cka').replace('dzki', 'dzka')

            age = str(random.randint(1, 120))

            customer = Customer(customername=customername, surname=surname,
                              age=age,
                              email=f'{customername.lower()}.{surname.lower()}@gmail.com',
                             )
            customer.save()
            print(customer)

