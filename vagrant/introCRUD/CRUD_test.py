from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlit:///restaurantmenu.db')
# bind the engine with Base class
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

# create restaurant
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
print session.query(Restaurant).all()

# create menu
cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella",
        course = "Entree", price = "$8.99", restaurant= myFirstRestaurant)
session.add(cheesepizza)
session.commit()
print session.query(MenuItem).all()


meatpizza = MenuItem(name = "Meat Pizza", description = "Made with all natural ingredients and fresh beef",
        course = "Entree", price = "$9.99", restaurant= myFirstRestaurant)
session.add(meatpizza)
session.commit()


fartpizza = MenuItem(name = "Fart Pizza", description = "Made with all natural ingredients and fresh fart",
        course = "Entree", price = "$20.99", restaurant= myFirstRestaurant)
session.add(fartpizza)
session.commit()

# read
firstResult = session.query(Restaurant).first()
print firstResult.name

# updatea (price of menuitem)
chees = session.query(MenuItem).filter_by(name = "Cheese Pizza")
for c in chees:
    if c.price != "$4.99":
    c.price = "$4.99"
    session.add(c)
    session.commit()

# delete (delete fart)
fart = session.query(MenuItem).filter_by(name = "Fart Pizza").one()
session.delete(fart)
session.commit()


