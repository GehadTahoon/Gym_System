import sqlite3


# CRUD
def addTrainer(
    Trainer_Name,
    Trainer_Phone,
    Trainer_Age,
    Trainer_Coach,
    Trainer_StartDate,
    Trainer_EndDate,
    Trainer_Subscription,
):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()
    cursor.execute(
        "insert into trainer (`Trainer_Name`,`Trainer_Phone`,`Trainer_Age`,`Trainer_Coach`,`Trainer_StartDate`,`Trainer_EndDate`,`Trainer_Subscription`) values (?,?,?,?,?,?,?)",
        (
            Trainer_Name,
            Trainer_Phone,
            Trainer_Age,
            Trainer_Coach,
            Trainer_StartDate,
            Trainer_EndDate,
            Trainer_Subscription,
        ),
    )
    con.commit()
    con.close()


def updateTrainer(
    Trainer_Name,
    Trainer_Phone,
    Trainer_Age,
    Trainer_Coach,
    Trainer_StartDate,
    Trainer_EndDate,
    Trainer_Subscription,
    Trainer_Id,
):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()
    # Update the database with the new data
    cursor.execute(
        "UPDATE trainer SET Trainer_Name = ?, Trainer_Phone = ?, Trainer_Age = ?, Trainer_Coach = ?, Trainer_StartDate = ?, Trainer_EndDate = ?, Trainer_subscription = ? WHERE Trainer_Id = ?",
        (
            Trainer_Name,
            Trainer_Phone,
            Trainer_Age,
            Trainer_Coach,
            Trainer_StartDate,
            Trainer_EndDate,
            Trainer_Subscription,
            Trainer_Id,
        ),
    )
    con.commit()
    con.close()


def deleteTrainer(selectedID):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()
    cursor.execute(f"delete from trainer where Trainer_Id={selectedID}")

    con.commit()
    con.close()


def update_sup(
    new_name,
    new_company,
    new_quantity,
    new_price,
    selected_item_id,
):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    cursor.execute(
        "UPDATE Supplement SET Sup_Name=?, Sup_Company=?, Sup_Quantity=?, Sup_Price=? WHERE Sup_Id=?",
        (
            new_name,
            new_company,
            new_quantity,
            new_price,
            selected_item_id,
        ),
    )
    con.commit()


def search_Trainer(phoneNum):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()
    cursor.execute("SELECT * from trainer WHERE Trainer_phone like ?", [int(phoneNum)])
    con.commit()


