# from datetime import date, datetime
# from src.database import schemas

# def test_create_supply(create_supply_item):

#     new_supply = create_supply_item

#     assert new_supply.item_name == "starfruit"
#     assert new_supply.quantity == 80
#     assert new_supply.id == 1
#     assert new_supply.temp_sensitive == "no"
#     assert new_supply.users_id == 1
#     assert type(new_supply.created_at) == datetime
#     assert type(new_supply.date_ordered) == date


# def test_no_supplies_in_db(authorized_client):

#     res = authorized_client.get("/api/supplies/")

#     assert res.json().get('detail') == "There are no supplies in the database."

# def test_get_supply_by_id(authorized_client, create_supply_item):

#     res = authorized_client.get("/api/supplies/1")

#     supply = schemas.Supply(**res.json())

#     assert res.status_code == 200
#     assert supply.item_name == "starfruit"
#     assert supply.quantity == 80
#     assert supply.id == 1
#     assert supply.temp_sensitive == "no"
#     assert supply.users_id == 1
#     assert type(supply.created_at) == datetime
#     assert type(supply.date_ordered) == date


# def test_get_supply_by_id_failure(authorized_client,):

#     res = authorized_client.get("/api/supplies/2")

#     assert res.json().get('detail') == "Supply Item with the id:2 was not found."

# def test_get_all_supplies(authorized_client, create_multiple_supplies):


#     res = authorized_client.get("/api/supplies/")

#     list = res.json()

#     assert res.status_code == 200
#     assert len(list) == 3
#     assert list[0]['item_name'] == "starfruit"
#     assert list[1]['item_name'] == "toilet paper"
#     assert list[2]['item_name'] == "chips"


# def test_delete_supply(authorized_client, create_supply_item):

#     res = authorized_client.delete("/api/supplies/1")

#     res1= authorized_client.get("/api/supplies/")

#     assert res.status_code == 200
#     assert res1.json().get('detail') == "There are no supplies in the database."


