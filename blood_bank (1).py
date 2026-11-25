blood_bank={"O+":5,"O-":3,"A+":4,"A-":2,"B+":3,"B-":2,"AB+":2,"AB-":1}
blood_groups=["O+","O-","A+","A-","B+","B-","AB+","AB-"]
component_stock={"Whole Blood":{group:0 for group in blood_groups},"Plasma":{group:0 for group in blood_groups}}
compatibility={"O+": ["O+","O-"],"O-":["O-"],"A+": ["A+","A-","O+","O-"],"A-":["A-","O-"],"B+": ["B+","B-","O+","O-"],"B-":["B-","O-"],"AB+": ["AB+","AB-","A+","A-","B+","B-","O+","O-"],"AB-":["AB-","A-","B-","O-"]}
donors=[]
patients=[]
donations=[]
donor_id=1
patient_id=1
donation_id=1
def get_integer(message):
    while True:
        try:
            value=int(input(message))
            if value>=0:
                return value
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input! Enter a number.")
def get_units(message):
    while True:
        try:
            value=float(input(message))
            if value>0:
                return value
            print("Units must be greater than zero.")
        except ValueError:
            print("Please enter a valid number.")
def get_blood_group():
    while True:
        group=input("Enter blood group: ").upper().strip()
        if group in blood_groups:
            return group
        print("Invalid blood group!")
def register_donor():
    global donor_id
    print("\n--- DONOR REGISTRATION ---")
    name=input("Donor name: ").strip()
    age=get_integer("Age: ")
    group=get_blood_group()
    phone=input("Contact number: ").strip()
    height=get_units("Height (cm): ")
    weight=get_units("Weight (kg): ")
    donor={"id":donor_id,"name":name,"age":age,"group":group,"phone":phone,"height":height,"weight":weight,"screening":"Not Screened"}
    donors.append(donor)
    print("\nDonor registered successfully!")
    print("Donor ID:",donor_id)
    donor_id+=1
def donor_screening():
    print("\n--- DONOR HEALTH SCREENING ---")
    if len(donors)==0:
        print("No donors registered.")
        return
    show_donors()
    selected_id=get_integer("Enter donor ID: ")
    for donor in donors:
        if donor["id"]==selected_id:
            print("\nDonor:",donor["name"])
            if donor["age"]<18:
                print("Donor must be at least 18.")
                donor["screening"]="Rejected"
                return
            haemoglobin=input("Haemoglobin checked? (Yes/No): ").lower()
            bp=input("Blood pressure checked? (Yes/No): ").lower()
            illness=input("Recent illness reported? (Yes/No): ").lower()
            history=input("Medical history recorded? (Yes/No): ").lower()
            print("\nMedical staff decision:")
            print("1. Approved")
            print("2. Deferred")
            print("3. Rejected")
            choice=input("Enter choice: ")
            if choice=="1":
                if haemoglobin=="yes" and bp=="yes" and illness=="no" and history=="yes":
                    donor["screening"]="Approved"
                else:
                    donor["screening"]="Pending Review"
                    print("Screening details need further review.")
            elif choice=="2":
                donor["screening"]="Deferred"
            elif choice=="3":
                donor["screening"]="Rejected"
            else:
                print("Invalid choice.")
                return
            print("Screening status:",donor["screening"])
            return
    print("Donor ID not found.")
def show_donors():
    print("\n--- DONOR LIST ---")
    if len(donors)==0:
        print("No donors available.")
        return
    for donor in donors:
        print("--------------------------------")
        print("ID:",donor["id"])
        print("Name:",donor["name"])
        print("Age:",donor["age"])
        print("Blood Group:",donor["group"])
        print("Contact:",donor["phone"])
        print("Screening:",donor["screening"])
def register_donation():
    global donation_id
    print("\n--- REGISTER BLOOD DONATION ---")
    if len(donors)==0:
        print("Register a donor first.")
        return
    show_donors()
    selected_id=get_integer("Enter donor ID: ")
    for donor in donors:
        if donor["id"]==selected_id:
            if donor["screening"]!="Approved":
                print("Donor is not approved for donation.")
                return
            print("\nSelect blood component:")
            print("1. RBC")
            print("2. Whole Blood")
            print("3. Plasma")
            choice=input("Enter choice: ")
            components={"1":"RBC","2":"Whole Blood","3":"Plasma"}
            if choice not in components:
                print("Invalid component.")
                return
            component=components[choice]
            units=get_units("Enter donated units: ")
            donation={"id":donation_id,"donor_id":selected_id,"name":donor["name"],"group":donor["group"],"component":component,"units":units,"test_status":"Pending"}
            donations.append(donation)
            print("Donation registered successfully!")
            print("Donation ID:",donation_id)
            print("Testing status: Pending")
            donation_id+=1
            return
    print("Donor ID not found.")
def blood_testing():
    print("\n--- BLOOD TESTING ---")
    if len(donations)==0:
        print("No donations registered.")
        return
    for donation in donations:
        print("ID:",donation["id"],"| Donor:",donation["name"],"| Status:",donation["test_status"])
    selected_id=get_integer("Enter donation ID: ")
    for donation in donations:
        if donation["id"]==selected_id:
            if donation["test_status"]!="Pending":
                print("This donation has already been tested.")
                return
            print("\nEnter simulated lab test results.")
            tests=["HIV","Hepatitis B","Hepatitis C","Syphilis","Malaria"]
            all_negative=True
            for test in tests:
                result=input(test+" (Negative/Positive): ").strip().lower()
                if result!="negative":
                    all_negative=False
            if all_negative:
                approval=input("Has authorised staff approved this unit? (Yes/No): ").lower()
                if approval=="yes":
                    donation["test_status"]="Approved"
                    group=donation["group"]
                    component=donation["component"]
                    units=donation["units"]
                    if component=="RBC":
                        blood_bank[group]+=units
                    else:
                        component_stock[component][group]+=units
                    print("Donation approved and stock updated!")
                else:
                    donation["test_status"]="Pending Review"
                    print("Waiting for staff review.")
            else:
                donation["test_status"]="Rejected"
                print("Donation rejected in this simulation.")
            return
    print("Donation ID not found.")
def show_inventory():
    print("\n========== BLOOD INVENTORY ==========")
    print("\nRBC STOCK")
    for group,units in blood_bank.items():
        print(group,":",units,"units")
    for component,stock in component_stock.items():
        print("\n"+component.upper()+" STOCK")
        for group,units in stock.items():
            print(group,":",units,"units")
def register_patient():
    global patient_id
    print("\n--- PATIENT REGISTRATION ---")
    name=input("Patient name: ").strip()
    age=get_integer("Patient age: ")
    group=get_blood_group()
    print("\nSelect required component:")
    print("1. RBC")
    print("2. Whole Blood")
    print("3. Plasma")
    choice=input("Enter choice: ")
    components={"1":"RBC","2":"Whole Blood","3":"Plasma"}
    if choice not in components:
        print("Invalid component.")
        return
    units=get_units("Units required: ")
    patient={"id":patient_id,"name":name,"age":age,"group":group,"component":components[choice],"units":units,"status":"Registered"}
    patients.append(patient)
    print("Patient registered successfully!")
    print("Patient ID:",patient_id)
    patient_id+=1
def find_compatible_groups(group,component):
    if component=="RBC":
        return compatibility[group]
    return [group]
def issue_blood():
    print("\n--- ISSUE BLOOD ---")
    if len(patients)==0:
        print("Register a patient first.")
        return
    for patient in patients:
        print("ID:",patient["id"],"| Name:",patient["name"],"| Status:",patient["status"])
    selected_id=get_integer("Enter patient ID: ")
    for patient in patients:
        if patient["id"]==selected_id:
            if patient["status"]=="Issued":
                print("Blood has already been issued.")
                return
            group=patient["group"]
            component=patient["component"]
            required=patient["units"]
            if component=="RBC":
                stock=blood_bank
            else:
                stock=component_stock[component]
            compatible=find_compatible_groups(group,component)
            print("\nCompatible groups:",compatible)
            total_available=sum(stock[g] for g in compatible)
            print("Total available:",total_available)
            print("Required:",required)
            if total_available<required:
                print("Insufficient blood stock.")
                return
            crossmatch=input("Has authorised staff approved crossmatch? (Yes/No): ").lower()
            if crossmatch!="yes":
                print("Blood not issued.")
                return
            remaining=required
            ordered_groups=[group]+[g for g in compatible if g!=group]
            for blood_group in ordered_groups:
                if remaining<=0:
                    break
                available=stock[blood_group]
                used=min(available,remaining)
                stock[blood_group]-=used
                remaining-=used
            patient["status"]="Issued"
            print("\nBlood issued successfully!")
            print("Patient:",patient["name"])
            print("Component:",component)
            print("Units issued:",required)
            return
    print("Patient ID not found.")
def show_patients():
    print("\n--- PATIENT RECORDS ---")
    if len(patients)==0:
        print("No patient records.")
        return
    for patient in patients:
        print("--------------------------------")
        print("ID:",patient["id"])
        print("Name:",patient["name"])
        print("Age:",patient["age"])
        print("Blood Group:",patient["group"])
        print("Component:",patient["component"])
        print("Units:",patient["units"])
        print("Status:",patient["status"])
def show_donations():
    print("\n--- DONATION RECORDS ---")
    if len(donations)==0:
        print("No donation records.")
        return
    for donation in donations:
        print("--------------------------------")
        print("Donation ID:",donation["id"])
        print("Donor:",donation["name"])
        print("Blood Group:",donation["group"])
        print("Component:",donation["component"])
        print("Units:",donation["units"])
        print("Test Status:",donation["test_status"])
def main():
    while True:
        print("\n================================")
        print("     BLOOD BANK MANAGEMENT")
        print("================================")
        print("1. Register Donor")
        print("2. Donor Health Screening")
        print("3. Show Donors")
        print("4. Register Blood Donation")
        print("5. Blood Testing")
        print("6. Show Donation Records")
        print("7. Show Blood Inventory")
        print("8. Register Patient")
        print("9. Issue Blood")
        print("10. Show Patient Records")
        print("11. Exit")
        choice=input("\nEnter your choice: ")
        if choice=="1":
            register_donor()
        elif choice=="2":
            donor_screening()
        elif choice=="3":
            show_donors()
        elif choice=="4":
            register_donation()
        elif choice=="5":
            blood_testing()
        elif choice=="6":
            show_donations()
        elif choice=="7":
            show_inventory()
        elif choice=="8":
            register_patient()
        elif choice=="9":
            issue_blood()
        elif choice=="10":
            show_patients()
        elif choice=="11":
            print("Thank you for using Blood Bank Management System!")
            break
        else:
            print("Invalid choice! Please try again.")
main()
