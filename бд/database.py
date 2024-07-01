import mysql.connector as connector
from datetime import date

db = connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="apteka"
)

def get_orders(str = ""):
    statement = "select idOrder, orderDate, patientName, medication.name, status.name, receiveDate from `order`  \
                    inner join medication on `order`.idMedication = medication.idMedication \
                    inner join prescription on `order`.idPrescription = prescription.idPrescription \
                    inner join costumer on prescription.idCostumer = costumer.idCostumer \
                    inner join status on status.idStatus = `order`.idStatus "
    if str != "":
        statement += " where patientName like '" + str + "%'"
    statement += " order by orderDate desc"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def insert_order(idPrescription, idMedication, orderDate, idStatus, componentsAvailable, receiveDate):
    cursor = db.cursor()
    if receiveDate is None:
        statement = "insert into `order` (idPrescription, idMedication, orderDate, idStatus, componentsAvailable) values (%s, %s, %s, %s, %s)"
        cursor.execute(statement, (idPrescription, idMedication, orderDate, idStatus, componentsAvailable))
    else:
        statement = "insert into `order` (idPrescription, idMedication, orderDate, idStatus, componentsAvailable, receiveDate) values (%s, %s, %s, %s, %s, %s)"
        cursor.execute(statement, (idPrescription, idMedication, orderDate, idStatus, componentsAvailable, receiveDate))
    db.commit()
    
def insert_costumer(name, phone, address):
    cursor = db.cursor()
    cursor.execute("insert into costumer (`fullName`, `phoneNumber`, `Address`) values (%s, %s, %s)", (name, phone, address))
    db.commit()
    
def get_costumers(str = ""):
    statement = "select * from costumer"
    if str != "":
        statement += " where fullName like '" + str + "%'"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def get_medications(str = ""):
    statement = "SELECT medication.idMedication, medication.name, `type`.name, method.name, manufactured, technology, prepareTime, price, criticalLevel FROM apteka.medication \
            inner join method on medication.idMethod = method.idMethod \
            left join technology on medication.idTechnology = technology.idTechnology \
            inner join `type` on `type`.idType = medication.idType"
    if str != "":
        statement += " where medication.name like '" + str + "%'"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def get_medication_by_name(name):
    statement = "select * from medication where name = %s"
    cursor = db.cursor()
    cursor.execute(statement, (name,))
    return cursor.fetchall()

def insert_medication(name, type, method, manufactured, technology, prepareTime, price, criticalLevel):
    cursor = db.cursor()
    cursor.execute("insert into medication (name, idType, idMethod, manufactured, idTechnology, prepareTime, price, criticalLevel) \
                    values (%s, %s, %s, %s, %s, %s, %s, %s)", (name, type, method, manufactured, technology, prepareTime, price, criticalLevel))
    db.commit()
    
def insert_ingredient(medication_id, ingridient_id, value):
    cursor = db.cursor()
    cursor.execute("insert into `apteka`.`ingridients` (`idMedication`, `idIngridient`, `voluem`) values (%s, %s, %s)", (medication_id, ingridient_id, value))
    db.commit()
    
def get_ingridients(medication_id):
    statement = "select idIngridient, voluem from `apteka`.`ingridients` where idMedication = %s"
    cursor = db.cursor()
    cursor.execute(statement, (medication_id,))
    return cursor.fetchall()

def get_types():
    statement = "select * from `type`"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def get_instructions():
    statement = "select * from instruction"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def get_technologies(str = ""):
    if str == "":
        statement = "select * from technology"
    else:
        statement = f"select * from technology where technology like '%{str}%'"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def get_technology_id(name):
    cursor = db.cursor()
    cursor.execute("select idTechnology from technology where technology = %s", (name,))
    return cursor.fetchone()

def insert_technology(name, description):
    cursor = db.cursor()
    cursor.execute("insert into technology (technology, description) values (%s, %s)", (name, description))
    db.commit()

def get_methods():
    statement = "select * from method"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def get_medication_quantity(medication_id):
    statement = "select quantity FROM apteka.inventory where idMedication = %s"
    cursor = db.cursor()
    cursor.execute(statement, (medication_id,))
    return cursor.fetchone()

def insert_prescription(idCostumer, docName, patientName, age, diagnosis, idMedication, quantity, idInstruction):
    statement = "insert into prescription (idCostumer, docName, patientName, age, diagnosis, idMedication, quantity, idInstruction) values (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db.cursor()
    cursor.execute(statement, (idCostumer, docName, patientName, age, diagnosis, idMedication, quantity, idInstruction))
    db.commit()
    return cursor.lastrowid

def get_status():
    statement = "select * from status"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def get_statistics(str = ""):
    statement = "select name, voluem, date from statistics \
        inner join medication on statistics.idMedication = medication.idMedication "
    if str != "":
        statement += " where medication.name like '" + str + "%'"
    statement += " order by date desc"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def write_statistic(idMedication, voluem, data=date.today()):
    statement = "select * from statistics where idMedication = %s and date = %s"
    cursor = db.cursor()
    cursor.execute(statement, (idMedication, data))
    search = cursor.fetchone()
    if search:
        statement = "update statistics set voluem = voluem + %s where idMedication = %s and date = %s"
    else:
        statement = "insert into statistics (voluem, idMedication, date) values (%s, %s, %s)"
    cursor.execute(statement, (voluem, idMedication, data))
    db.commit()
    
def get_medications_in_inventory(str = ""):
    statement = "select medication.idMedication, medication.name, quantity, expireDate from inventory	\
	    inner join medication on medication.idMedication = inventory.idMedication"
    if str != "":
        statement += " where medication.name like '" + str + "%'"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def get_medication_inventory(idMedication):
    statement = "select quantity, expireDate from inventory where idMedication = %s"
    cursor = db.cursor()
    cursor.execute(statement, (idMedication,))
    return cursor.fetchone()

def insert_inventory(idMedication, quantity, expire_date):
    cursor = db.cursor()
    if expire_date:
        statement = "insert into inventory (idMedication, quantity, expireDate) values (%s, %s, %s)"
        cursor.execute(statement, (idMedication, quantity, expire_date))
    else:
        statement = "insert into inventory (idMedication, quantity) values (%s, %s)"
        cursor.execute(statement, (idMedication, quantity))
    db.commit()
    
def update_inventory(idMedication, quantity, expire_date = None):
    cursor = db.cursor()
    if quantity == 0:
        expire_date = None
    if expire_date:
        statement = "update inventory set quantity = %s, expireDate = %s where idMedication = %s"
        cursor.execute(statement, (quantity, expire_date, idMedication))
    else:
        statement = "update inventory set quantity = %s, expireDate = NULL where idMedication = %s"
        cursor.execute(statement, (quantity, idMedication))
    db.commit()

def decrease_inventory(idMedication, quantity):
    cur_quantity = get_medication_inventory(idMedication)[0]
    statement = "update inventory set quantity = quantity - %s where idMedication = %s"
    cursor = db.cursor()
    cursor.execute(statement, (quantity, idMedication))
    if cur_quantity - quantity == 0:
        update_inventory(idMedication, 0)
    db.commit()
    
def find_costumers_not_take_order():
    statement = "select distinct costumer.fullName, costumer.phoneNumber, costumer.Address  \
                from `order` \
                inner join prescription on `order`.idPrescription = prescription.idPrescription \
                inner join costumer on prescription.idCostumer = costumer.idCostumer \
                where `order`.idStatus = 3 and `order`.receiveDate < curdate()"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def find_costumers_wait_order(type = None):
    cursor = db.cursor()
    if type:
        statement = "select distinct costumer.fullName, costumer.phoneNumber, costumer.Address \
                    from `order` \
                    inner join prescription on `order`.idPrescription = prescription.idPrescription \
                    inner join costumer on prescription.idCostumer = costumer.idCostumer \
                    inner join medication on `order`.idMedication = medication.idMedication \
                    inner join `type` on medication.idType = `type`.idType\
                    where `order`.idStatus = 2 and `type`.name = %s"
        cursor.execute(statement, (type,))
    else:
        statement = "select distinct costumer.fullName, costumer.phoneNumber, costumer.Address \
                    from `order` \
                    inner join prescription on `order`.idPrescription = prescription.idPrescription \
                    inner join costumer on prescription.idCostumer = costumer.idCostumer \
                    where `order`.idStatus = 2"
        cursor.execute(statement)
    return cursor.fetchall()

def find_most_popular_medications(type = None):
    cursor = db.cursor()
    if type:
        statement = "select medication.name, sum(statistics.voluem) as 'total voluem' \
                    from statistics \
                    inner join medication on statistics.idMedication = medication.idMedication \
                    inner join `type` on medication.idType = `type`.idType \
                    where `type`.name = %s \
                    group by statistics.idMedication \
                    order by sum(statistics.voluem) desc limit 10" 
        cursor.execute(statement, (type,))
    else:
        statement = "select medication.name, sum(statistics.voluem) as 'total voluem' \
                    from statistics \
                    inner join medication on statistics.idMedication = medication.idMedication \
                    group by statistics.idMedication \
                    order by sum(statistics.voluem) desc limit 10"
        cursor.execute(statement)
    return cursor.fetchall()
                    
def find_values_in_period(medications_list, start_date, end_date):
    statement = f"select medication.name, sum(statistics.voluem) as 'total voluem' \
                from statistics \
                inner join medication on statistics.idMedication = medication.idMedication \
                where medication.name IN (" +'\'' + '\', \''.join(medications_list)+ '\'' +") and (statistics.date between %s and %s) \
                group by statistics.idMedication \
                order by sum(statistics.voluem) desc" 
    cursor = db.cursor()
    cursor.execute(statement, (start_date, end_date))
    return cursor.fetchall()

def find_for_med_in_period(medication, start, end):
    statement ="select costumer.fullName, costumer.phoneNumber, costumer.Address \
                from `order` \
                inner join prescription on `order`.idPrescription = prescription.idPrescription \
                inner join medication on `order`.idMedication = medication.idMedication \
                inner join costumer on prescription.idCostumer = costumer.idCostumer \
                where (`order`.orderDate between %s and %s) and medication.name = %s \
                group by costumer.idCostumer"
    cursor = db.cursor()
    cursor.execute(statement, (start, end, medication))
    return cursor.fetchall()

def find_critical_level():
    statement = "select medication.idMedication, medication.name, `type`.name, method.name, manufactured, technology, prepareTime, price, criticalLevel \
                from medication \
                inner join method on medication.idMethod = method.idMethod \
                left join technology on medication.idTechnology = technology.idTechnology \
                left join inventory on medication.idMedication = inventory.idMedication \
                inner join `type` on `type`.idType = medication.idType \
                where medication.criticalLevel > COALESCE(inventory.quantity, 0)"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def find_med_least_quantity(type = None):
    cursor = db.cursor()
    if type:
        statement = "select medication.name, inventory.quantity as quantity, inventory.expireDate \
                    from medication \
                    inner join inventory on medication.idMedication = inventory.idMedication \
                    inner join `type` on `type`.idType = medication.idType \
                    where `type`.name = %s and inventory.quantity = \
                    (select min(quantity) from inventory \
                    inner join medication on medication.idMedication = inventory.idMedication \
                    inner join `type` on `type`.idType = medication.idType \
                    where `type`.name = %s)"
        cursor.execute(statement, (type, type))
    else:
        statement = "select medication.name, inventory.quantity as quantity, inventory.expireDate \
                    from medication \
                    inner join inventory on medication.idMedication = inventory.idMedication \
                    where inventory.quantity = (select min(quantity) from inventory)"
        cursor.execute(statement)
    return cursor.fetchall()

def find_orders_in_production():
    statement = "select idOrder, orderDate, patientName, medication.name, status.name, receiveDate from `order`  \
                inner join prescription on `order`.idPrescription = prescription.idPrescription \
                inner join medication on medication.idMedication =`order`.idMedication \
                inner join status on status.idStatus = `order`.idStatus \
                where `order`.idStatus = 1\
                order by orderDate desc"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def find_med_needed_for_orders():
    statement = "select ingrMed.idMedication, ingrMed.name, `type`.name, method.name, ingrMed.manufactured, technology, ingrMed.prepareTime, ingrMed.price, ingrMed.criticalLevel from `order` \
                inner join medication on medication.idMedication =`order`.idMedication \
                inner join ingridients on ingridients.idMedication = medication.idMedication \
                inner join (medication as ingrMed) on ingrMed.idMedication = ingridients.idIngridient \
                inner join method on method.idMethod = ingrMed.idMethod \
                left join technology on technology.idTechnology = ingrMed.idTechnology \
                inner join `type` on `type`.idType = ingrMed.idType \
                where `order`.idStatus = 1 \
                group by ingrMed.name"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def find_technologies_by_type(type):
    statement = "select distinct technology.technology, technology.description from technology \
                inner join medication on medication.idTechnology = technology.idTechnology \
                inner join `type` on `type`.idType = medication.idType \
                where `type`.name = %s"
    cursor = db.cursor()
    cursor.execute(statement, (type, ))
    return cursor.fetchall()

def find_technologies_by_medication(medication):
    statement = "select technology.technology, technology.description from technology \
                inner join medication on medication.idTechnology = technology.idTechnology \
                where medication.name = %s"
    cursor = db.cursor()
    cursor.execute(statement, (medication, ))
    return cursor.fetchall()

def find_technologies_in_production():
    statement = "select distinct technology.technology, technology.description from technology \
                inner join medication on medication.idTechnology = technology.idTechnology \
                inner join `order` on `order`.idMedication = medication.idMedication \
                where `order`.idStatus = 1"
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor.fetchall()

def find_ingridients_by_medication(medication_id):
    statement = "select idIngridient, medication.name, voluem from `apteka`.`ingridients` \
        inner join medication on medication.idMedication = ingridients.idIngridient \
        where ingridients.idMedication = %s"
    cursor = db.cursor()
    cursor.execute(statement, (medication_id,))
    return cursor.fetchall()

def get_most_buying_freaquency_by_medication(medication):
    statement = "select count(costumer.idCostumer) \
                from `order`  \
                inner join  medication on  `order`.idMedication = medication.idMedication \
                inner join prescription on  `order`.idPrescription = prescription.idPrescription \
                inner join costumer  on  prescription.idCostumer = costumer.idCostumer \
                where medication.name = %s \
                group by costumer.idCostumer \
                order by count(costumer.idCostumer) desc limit 1"
    cursor = db.cursor()
    cursor.execute(statement, (medication, ))
    freaquancy = cursor.fetchall()
    return freaquancy[0][0] if freaquancy else 0

def find_most_freaquent_costumers_by_medication(medication):
    freaquancy = get_most_buying_freaquency_by_medication(medication)
    cursor = db.cursor()
    statement = "select costumer.fullName, costumer.phoneNumber, costumer.Address \
                from `order`  \
                inner join  medication on  `order`.idMedication = medication.idMedication \
                inner join prescription on  `order`.idPrescription = prescription.idPrescription \
                inner join costumer  on  prescription.idCostumer = costumer.idCostumer \
                where medication.name = %s \
                group by costumer.idCostumer \
                having count(costumer.idCostumer) = %s"
    cursor.execute(statement, (medication, freaquancy))
    return cursor.fetchall()

def get_most_buying_freaquency_by_type(type):
    statement = "select count(costumer.idCostumer) \
                from `order`  \
                inner join  medication on  `order`.idMedication = medication.idMedication \
                inner join prescription on  `order`.idPrescription = prescription.idPrescription \
                inner join costumer  on  prescription.idCostumer = costumer.idCostumer \
                inner join `type` on medication.idType = `type`.idType \
                where `type`.name = %s \
                group by costumer.idCostumer \
                order by count(costumer.idCostumer) desc limit 1"
    cursor = db.cursor()
    cursor.execute(statement, (type, ))
    freaquancy = cursor.fetchall()
    return freaquancy[0][0] if freaquancy else 0

def find_most_freaquent_costumers_by_type(type):
    freaquancy = get_most_buying_freaquency_by_type(type)
    cursor = db.cursor()
    statement = "select costumer.fullName, costumer.phoneNumber, costumer.Address \
                from `order`  \
                inner join  medication on  `order`.idMedication = medication.idMedication \
                inner join prescription on  `order`.idPrescription = prescription.idPrescription \
                inner join costumer  on  prescription.idCostumer = costumer.idCostumer \
                inner join `type` on medication.idType = `type`.idType \
                where `type`.name = %s \
                group by costumer.idCostumer \
                having count(costumer.idCostumer) = %s"
    cursor.execute(statement, (type, freaquancy))
    return cursor.fetchall()

def find_order_info(id_order):
    statement = "select idOrder, costumer.fullName, receiveDate, medication.name, quantity, medication.idMedication, idStatus, componentsAvailable \
                from `order` \
                inner join prescription on `order`.idPrescription = prescription.idPrescription \
                inner join costumer on prescription.idCostumer = costumer.idCostumer \
                inner join medication on `order`.idMedication = medication.idMedication \
                where idOrder = %s"
    cursor = db.cursor()
    cursor.execute(statement, (id_order, ))
    return cursor.fetchall()

def find_medication_info(medication):
    cursor = db.cursor()
    statment = "select medication.idMedication, medication.name, `type`.name as 'type', inventory.quantity as 'quantity', medication.price, technology.technology \
                from medication \
                left join `type` on medication.idType = `type`.idType \
                left join inventory on inventory.idMedication = medication.idMedication \
                left join technology on technology.idTechnology = medication.idTechnology \
                where medication.name = %s"
    cursor.execute(statment, (medication, ))
    info = cursor.fetchall()
    statment = "select ingrMed.name, ingridients.voluem, ingrMed.price from medication \
                inner join ingridients on ingridients.idMedication = medication.idMedication \
                inner join (medication as ingrMed) on ingrMed.idMedication = ingridients.idIngridient \
                where medication.name = %s"
    cursor.execute(statment, (medication, ))
    ingrs = cursor.fetchall()
    info.append(ingrs)
    return info

def delete_inventory(medication):
    statement = "delete from inventory where idMedication = %s"
    cursor = db.cursor()
    cursor.execute(statement, (medication, ))
    db.commit()
    
def delete_technology(id):
    statement = "delete from technology where idTechnology = %s"
    cursor = db.cursor()
    cursor.execute(statement, (id, ))
    db.commit()
    
def delete_costumer(id):
    statement = "delete from costumer where idCostumer = %s"
    cursor = db.cursor()
    cursor.execute(statement, (id, ))
    db.commit()
    
def delete_order(id_order):
    statement = "delete from `order` where idOrder = %s"
    cursor = db.cursor()
    cursor.execute(statement, (id_order, ))
    db.commit()
    
def delete_medication(id_medication):
    statement = "delete from medication where idMedication = %s"
    cursor = db.cursor()
    cursor.execute(statement, (id_medication, ))
    db.commit()
    
def delete_ingridient(id_medication, id_ingredient):
    statement = "delete from ingridients where idMedication = %s and idIngridient = %s"
    cursor = db.cursor()
    cursor.execute(statement, (id_medication, id_ingredient))
    db.commit()
    
def update_technology(id, name, description):
    statement = "update technology set technology = %s, description = %s where idTechnology = %s"
    cursor = db.cursor()
    cursor.execute(statement, (name, description, id))
    db.commit()
    
def update_costumer(id, fullName, phoneNumber, address):
    statement = "update costumer set fullName = %s, phoneNumber = %s, address = %s where idCostumer = %s"
    cursor = db.cursor()
    cursor.execute(statement, (fullName, phoneNumber, address, id))
    db.commit()
    
def update_order(id_order, id_costumer = None, id_receive_date = None, id_status = None, components_available = None):
    print(id_costumer, id_receive_date, id_status, components_available)
    cursor = db.cursor()
    if id_costumer is not None:
        cursor.execute("select idPrescription from `order`\
                        where idOrder = %s", (id_order, ))
        prescription = cursor.fetchall()[0][0]
        statment = "update prescription set idCostumer = %s where idPrescription = %s"
        cursor.execute(statment, (id_costumer, prescription))
    statment = "update `order` set "
    params = []
    if id_receive_date is not None:
        statment += "receiveDate = %s, "
        params.append(id_receive_date)
    else:
        statment += "receiveDate = NULL, "
    if id_status is not None:
        statment += "idStatus = %s, "
        params.append(id_status)
    if components_available is not None:
        statment += "componentsAvailable = %s, "
        params.append(components_available)
    statment = statment[:-2]
    if len(params) == 0:
        return
    statment += " where idOrder = %s"
    params.append(id_order)
    cursor.execute(statment, (*params, ))
    db.commit()
    
def update_medication(id, name, type, method, manufactured, price, critical_level, technology=None, prepare_time=None):
    params = [name, type, method, manufactured, price, critical_level]
    statement = "update medication \
        set name = %s, idType = %s, idMethod = %s, manufactured = %s, price = %s, criticalLevel = %s"
    if technology is not None:
        statement += ", idTechnology = %s"
        params.append(technology)
    else:
        statement += ", idTechnology = NULL"
    if prepare_time is not None:
        statement += ", prepareTime = %s"
        params.append(prepare_time)
    else:
        statement += ", prepareTime = NULL"
    statement += " where idMedication = %s"
    params.append(id)
    cursor = db.cursor()
    cursor.execute(statement, params)
    db.commit()
    cursor = db.cursor()
    
def update_ingridients(id_medication, ingr_ids, voluems):
    old = get_ingridients(id_medication)
    for ingr in old:
        delete_ingridient(id_medication, ingr[0])
    for id, voluem in zip(ingr_ids, voluems):
        insert_ingredient(id_medication, id, voluem)