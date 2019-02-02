from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Chocolate, Base, ChocoTypes, User

engine = create_engine('sqlite:///chocolatemenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(name='Vidya Guruju', email='vijju12344@gmail.com')
session.add(user1)
session.commit()

user2 = User(name='Vidya Satya', email='vidya.guruju@gmail.com')
session.add(user2)
session.commit()

# Menu for Cadbury
chocolate1 = Chocolate(name="Cadbury", user_id=1,
                       picture="/static/pics/Cadbury.jpg")

session.add(chocolate1)
session.commit()

chocoType1 = ChocoTypes(name="Choclairs Gold ",
                        description="""The luscious candy with an indulgent
                        brownie flavour in its caramel and pure dairy milk
                        in its centre""", price="Rs.200/-",
                        picture="/static/pics/c1(1).jpg",
                        chocolate=chocolate1, user_id=1)

session.add(chocoType1)
session.commit()


chocoType2 = ChocoTypes(name="Rich Dry Fruit Gift Box",
                        description="""Each box contains almonds,
                        cashews and raisins enrobed in rich chocolate""",
                        price="Rs.450/-", picture="/static/pics/c1(2).jpg",
                        chocolate=chocolate1, user_id=1)

session.add(chocoType2)
session.commit()

chocoType3 = ChocoTypes(name="DairyMilk Silk Miniatures",
                        description="""Contains 24 premium miniatures -
                        Classic Chocolate, Sea Salt, Butterscotch, Almond""",
                        price="Rs.530/-", picture="/static/pics/c1(3).jpg",
                        chocolate=chocolate1, user_id=1)

session.add(chocoType3)
session.commit()

chocoType4 = ChocoTypes(name="Dairy Milk Lickables",
                        description="""Lick and enjoy this liquid chocolaty
                        treat with a twist of Oreo bits and wheat crispies""",
                        price="Rs.35/-", picture="/static/pics/c1(4).jpg",
                        chocolate=chocolate1, user_id=1)

session.add(chocoType4)
session.commit()


chocoType5 = ChocoTypes(name="Monster Gems",
                        description="""Cadbury gems is colourful and fun
                        outside, delicious and chocolaty inside""",
                        price="Rs.80/-", picture="/static/pics/c1(6).jpg",
                        chocolate=chocolate1, user_id=1)

session.add(chocoType5)
session.commit()

chocoType6 = ChocoTypes(name="Bournville Bar, Cranberry",
                        description="""A dark chocolate that allows
                        you to end your day on a perfect note""",
                        price="Rs.90/-", picture="/static/pics/c1(7).jpg",
                        chocolate=chocolate1, user_id=1)

session.add(chocoType6)
session.commit()

chocoType7 = ChocoTypes(name="5 Star Chocolate",
                        description="""A delicious indulgent combination
                        of chocolate, caramel and nougat""",
                        price="Rs.135/-", picture="/static/pics/c1(8).jpg",
                        chocolate=chocolate1, user_id=1)

session.add(chocoType7)
session.commit()

chocoType8 = ChocoTypes(name="Fuse Chocolate Bar",
                        description="""A delicious indulgent combination
                        of chocolate, caramel and nougat""",
                        price="Rs.450/-", picture="/static/pics/c1(9).jpg",
                        chocolate=chocolate1, user_id=1)

session.add(chocoType8)
session.commit()


# Menu for Ferrero
chocolate2 = Chocolate(name="Ferrero", user_id=1,
                       picture="/static/pics/Ferrero.jpg")

session.add(chocolate2)
session.commit()


chocoType1 = ChocoTypes(name="Ferrero Rocher",
                        description="""A delicious creamy hazelnut filling,
                        a crisp wafer shell covered with chocolate and gently
                        roasted pieces""",
                        price="Rs.500/-", picture="/static/pics/c2(1).jpg",
                        chocolate=chocolate2, user_id=1)

session.add(chocoType1)
session.commit()

chocoType2 = ChocoTypes(name="Hanuta Hazelnut",
                        description="""Hanuta hazelnut chocolate,
                        Easy to eat, Quantity is 220g""",
                        price="Rs.1000/-", picture="/static/pics/c2(2).jpg",
                        chocolate=chocolate2, user_id=1)

session.add(chocoType2)
session.commit()

chocoType3 = ChocoTypes(name="Nutella B-Ready",
                        description="""Flavored with hazelnut and cocoa solids,
                        generically called chocolate spread.""",
                        price="Rs.900/-", picture="/static/pics/c2(3).jpg",
                        chocolate=chocolate2, user_id=1)

session.add(chocoType3)
session.commit()

chocoType4 = ChocoTypes(name="Kinder Country Milk",
                        description="""Multi-layered Milk Chocolate with
                        Cereal Bar individually wrapped """,
                        price="Rs.825/-", picture="/static/pics/c2(4).jpg",
                        chocolate=chocolate2, user_id=1)

session.add(chocoType4)
session.commit()

chocoType5 = ChocoTypes(name="Confetteria Raffaello",
                        description="""Confetteria raffaello with
                        Chocolate in white""",
                        price="Rs.151/-", picture="/static/pics/c2(5).jpg",
                        chocolate=chocolate2, user_id=1)

session.add(chocoType5)
session.commit()

chocoType6 = ChocoTypes(name="Ferrero Rocher(Golden)",
                        description="""Ferrero rocher the golden experience
                        chocolates, Luscious & creamy with Smooth chocolate""",
                        price="Rs.250/-", picture="/static/pics/c2(6).jpg",
                        chocolate=chocolate2, user_id=1)

session.add(chocoType6)
session.commit()


# Menu for Nestle
chocolate3 = Chocolate(name="Nestle", user_id=1,
                       picture="/static/pics/Nestle.png")

session.add(chocolate3)
session.commit()


chocoType1 = ChocoTypes(name="Kit Kat Chunky",
                        description="""Bars of crispy wafer fingers
                        covered with milk chocolate""",
                        price="Rs.300/-", picture="/static/pics/c3(1).jpg",
                        chocolate=chocolate3, user_id=1)

session.add(chocoType1)
session.commit()

chocoType2 = ChocoTypes(name="Dark Sences",
                        description="Nestle Kitkat Dark Special of 170 grams",
                        price="Rs.1000/-",  picture="/static/pics/c3(2).jpg",
                        chocolate=chocolate3, user_id=1)

session.add(chocoType2)
session.commit()

chocoType3 = ChocoTypes(name="BARONE",
                        description=" center filled with caramel and nougat",
                        price="Rs.150/-",  picture="/static/pics/c3(3).jpg",
                        chocolate=chocolate3, user_id=1)

session.add(chocoType3)
session.commit()

chocoType4 = ChocoTypes(name=" Munch Crunchy",
                        description="""Nestle Munch Crunchilicious
                        Chocolate coated wafer.""",
                        price="Rs.240/-",  picture="/static/pics/c3(4).jpg",
                        chocolate=chocolate3, user_id=1)

session.add(chocoType4)
session.commit()

chocoType5 = ChocoTypes(name="Kitkat ",
                        description="""Crunchilicious Chocolate coated
                        wafer with Tasty chocolate""",
                        price="Rs.200/-",  picture="/static/pics/c3(5).jpg",
                        chocolate=chocolate3, user_id=1)

session.add(chocoType5)
session.commit()

chocoType6 = ChocoTypes(name="ALPINO",
                        description="Cocoa and Intensely Dark chocolate",
                        price="Rs.450/-",  picture="/static/pics/c3(6).jpg",
                        chocolate=chocolate3, user_id=1)

session.add(chocoType6)
session.commit()


# Menu for Amul Chocolate
chocolate4 = Chocolate(name="Amul Chocolate ", user_id=2,
                       picture="/static/pics/Amul.jpg")

session.add(chocolate4)
session.commit()


chocoType1 = ChocoTypes(name="Fruit N Nut",
                        description="""Amul chocolates are made with goodness
                        of rich creamy milk and delicious cocoa""",
                        price="Rs.100/-",  picture="/static/pics/c4(1).jpg",
                        chocolate=chocolate4, user_id=2)

session.add(chocoType1)
session.commit()

chocoType2 = ChocoTypes(name="Dark-Chocolate",
                        description="""Made with cocoa from tanzania
                        yield a chocolate that has a nutty, sweet
                        taste with hints of bitter notes""",
                        price="Rs.540/-",  picture="/static/pics/c4(2).jpg",
                        chocolate=chocolate4, user_id=2)

session.add(chocoType2)
session.commit()

chocoType3 = ChocoTypes(name="Smooth & Creamy Chocolate",
                        description="""Amul Chocolates Are Made With Rich
                        Creamy Milk And Delicious Cocoa Indulge In The
                        Exquisite Taste Of Milk Chocolate.""",
                        price="Rs.200/-", picture="/static/pics/c4(3).jpg",
                        chocolate=chocolate4, user_id=2)

session.add(chocoType3)
session.commit()

chocoType4 = ChocoTypes(name="Tropical Orange Bar",
                        description="""Combo Of Amul
                        Chocolate and Silver Plated Coin""",
                        price="Rs.215/-",  picture="/static/pics/c4(4).jpg",
                        chocolate=chocolate4, user_id=2)

session.add(chocoType4)
session.commit()

chocoType5 = ChocoTypes(name="Chocominis",
                        description="""Amul Chocominis Chocolate 250 Grams
                        Perfect Git For Loved Ones""",
                        price="Rs.120/-", picture="/static/pics/c4(5).jpg",
                        chocolate=chocolate4, user_id=2)

session.add(chocoType5)
session.commit()


# Menu for Hershey's Kisses
chocolate5 = Chocolate(name="Hershey's Kisses ", user_id=2,
                       picture="/static/pics/hershey.jpg")

session.add(chocolate5)
session.commit()


chocoType1 = ChocoTypes(name=" Kisses",
                        description="""Individually wrapped in silver foils
                        A kosher and gluten-free candy""",
                        price="RS.1000/-", picture="/static/pics/c5(1).jpg",
                        chocolate=chocolate5, user_id=2)

session.add(chocoType1)
session.commit()

chocoType2 = ChocoTypes(name=" Miniatures",
                        description="""Each piece are foil wrapped
                        Assorted chocolate pack""",
                        price="Rs.800/-", picture="/static/pics/c5(2).jpg",
                        chocolate=chocolate5, user_id=2)

session.add(chocoType2)
session.commit()

chocoType3 = ChocoTypes(name=" Classic with Almond",
                        description="""Classic milk chocolate
                        Combined with almond""",
                        price="Rs.790/-", picture="/static/pics/c5(3).jpg",
                        chocolate=chocolate5, user_id=2)

session.add(chocoType3)
session.commit()

chocoType4 = ChocoTypes(name=" Nuggets Milk Chocolate",
                        description="""Classic milk chocolate
                        Combined with Nuggets""",
                        price="Rs.725/-", picture="/static/pics/c5(4).jpg",
                        chocolate=chocolate5, user_id=2)

session.add(chocoType4)
session.commit()

chocoType5 = ChocoTypes(name="Cookies N Cream",
                        description="""White creame candies with chocolate cookie
                        bits Individually wrapped in bright blue foils""",
                        price="Rs.508/-", picture="/static/pics/c5(5).jpg",
                        chocolate=chocolate5, user_id=2)

session.add(chocoType5)
session.commit()


# Menu for Galaxy Jewels
chocolate6 = Chocolate(name="Galaxy Jewels", user_id=2,
                       picture="/static/pics/galaxy.jpg")

session.add(chocolate6)
session.commit()


chocoType1 = ChocoTypes(name="Assorted Chocolates",
                        description="""A delicious assortment of individually
                        wrapped bitesize chocolates Made with Galaxy's silky
                        smooth chocolate blends of milk and dark chocolate""",
                        price="Rs.700/-", picture="/static/pics/c6(1).jpg",
                        chocolate=chocolate6, user_id=2)

session.add(chocoType1)
session.commit()

chocoType2 = ChocoTypes(name="Minis Milk Bars",
                        description="""These are Minis Smooth Milk
                        Chocolate 20 bars It is brown in colour.""",
                        price="Rs.950", picture="/static/pics/c6(2).jpg",
                        chocolate=chocolate6, user_id=2)

session.add(chocoType2)
session.commit()

chocoType3 = ChocoTypes(name="Milk Chocolate",
                        description="""Smooth milk chocolate Weight: 458.4g""",
                        price="Rs.480/-", picture="/static/pics/c6(3).jpg",
                        chocolate=chocolate6, user_id=2)

session.add(chocoType3)
session.commit()

chocoType4 = ChocoTypes(name="Fruit & Nut",
                        description="""Fruit and Nut Chocolate Pouch""",
                        price="Rs.400/-", picture="/static/pics/c6(4).jpg",
                        chocolate=chocolate6, user_id=2)

session.add(chocoType4)
session.commit()

print("chocolates are added to database!")