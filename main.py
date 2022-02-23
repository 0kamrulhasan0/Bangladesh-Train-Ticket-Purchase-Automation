from selenium import webdriver
from selenium.webdriver.common.by import By


def list_to_dict(list_of_info):
    """
    From a list of information it parses out the important ones
    (the name of the train and seat availibility) and returns it
    """
    train_name = list_of_info.pop(0)
    start_journey_time = list_of_info.pop(0)
    start_journey_place = list_of_info.pop(0)
    start_journey_date = list_of_info.pop(0)
    end_journey_time = list_of_info.pop(0)
    end_journey_place = list_of_info.pop(0)
    end_journey_date = list_of_info.pop(0)
    journey_duration = list_of_info.pop(0)
    ticket_price = list_of_info.pop(0)

    list_of_info.pop(0)  # Included all
    list_of_info.pop(0)  # Route
    list_of_info.pop(0)  # Availability
    list_of_info.pop(0)  # Class
    list_of_info.pop(0)  # Seats
    list_of_info.pop(0)  # Fair (A)
    list_of_info.pop(0)  # Fair (C)

    list_of_info.pop(-1)  # Note

    seats = []
    while len(list_of_info) != 0:
        seats.append(
            {
                "train_class": list_of_info.pop(0),
                "online_ticket": list_of_info.pop(0),
                "counter_ticket": list_of_info.pop(0),
                "adult_ticket_price": list_of_info.pop(0),
                "child_ticket_price": list_of_info.pop(0),
            }
        )
        list_of_info.pop(0)  # Purchase

    return train_name, seats


def url_generation(from_st, to_st, date, cls):
    """Generates url based on where you want to go from where and on which date"""
    return f"https://www.esheba.cnsbd.com/#/search-result?stationFrom={from_st}&stationTo={to_st}&journeyDate={date}&cls={cls}&adult=1&child=0"


def get_ticket_information(url):
    """
    creates the webdriver, parses it, goes through the buttons and returns the important info as a dictonary
    like train name, seat, purchase button as object (which only need to be .click())
    """
    driver = webdriver.Firefox()
    driver.get(url)

    driver.implicitly_wait(5)
    detail_button = driver.find_elements(
        by=By.XPATH, value="//button[contains(text(), 'Details')]"
    )
    for i in range(len(detail_button)):
        detail_button[i].click()

    avil_button = driver.find_elements(
        by=By.XPATH, value="//a[contains(text(),'Availability')]"
    )
    for j in range(len(avil_button)):
        avil_button[j].click()

    train_row = driver.find_elements(
        by=By.XPATH,
        value="/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div/div[*]",
    )
    purchase_buttons = driver.find_elements(
        by=By.XPATH,
        value="/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div/div[*]",
    )
    checked_tickets = 0
    ticket_list = []

    for row in train_row:
        train_info_list = row.text.split("\n")
        train_name, seats = list_to_dict(train_info_list)

        for seat in seats:
            online_ticket = int(seat["online_ticket"].split()[-1])
            if online_ticket > 0:
                print(
                    f"{train_name}\t{seat['train_class']}\tOnline Ticket:{online_ticket}"
                )
                ticket_list.append(
                    {
                        "name": train_name,
                        "cls": seat["train_class"],
                        "ticket": online_ticket,
                        "purchase_link": purchase_buttons[i],
                    }
                )
                checked_tickets += 1

    return ticket_list


if __name__ == "__main__":
    """
    TODO:
    * Login
    * esheba url generate with all dates and stations and chairs
    * Print Seats assoiated with train
    * Purshase Button Click
    """
    FROM_ST = "DA"  # Dhaka
    TO_ST = "PLB"  # Fulbari
    DATE = "2022-02-26"
    CLS_PREF = "S_CHAIR"  # Shovon Chair

    url = url_generation(FROM_ST, TO_ST, DATE, CLS_PREF)
    ticket_list = get_ticket_information(url)

    cls_preference = ["S_CHAIR", "SNIGDHA"]
    ticket_list.sort(key=lambda x: cls_preference.index(x["cls"]))

    print(ticket_list)
