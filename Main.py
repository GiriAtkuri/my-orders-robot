from robocorp.tasks import task
from robocorp import browser
import time
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
from RPA.FileSystem import FileSystem


tables = Tables()
page = browser.page()
http = HTTP()
pdf = PDF()
archive = Archive()
lib = FileSystem()

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    message = "Hello"
    message = message + " World!"

    browser.configure(
    browser_engine = "chrome",
    slowmo = 100,
    )
    clear_filder_data()
    open_the_robotssparebin_website()
    log_in()
    navigates_order_your_robot()
    close_the_annoying_modal()
    download_the_orders_file()
    orders = get_orders_from_csv()
    print(orders)
    order_robots_with_orders_data(orders)
    zip_the_recipts_folder()
    log_out()

def clear_filder_data():
    """Clear all the data from folders"""
    dir_recipts = "output/recipts/"
    dir_robots = "output/robots/"
    if lib.does_directory_exist(dir_recipts):
        lib.empty_directory(dir_recipts)

    if lib.does_directory_exist(dir_robots):
        lib.empty_directory(dir_robots)        


def open_the_robotssparebin_website():
    """Open Robot Sparebin Industries website"""
    browser.goto("https://robotsparebinindustries.com/")

def log_in():
    """Fills in the login form and clicks the 'Log in' button"""
    username_selector = "//input[@id='username']"
    passwor_selector = "//input[@id='password']"
    login_selector = "//button[@type='submit'][text()='Log in']"
    page.bring_to_front()
    page.fill(selector=username_selector, value="maria")
    page.fill(selector=passwor_selector, value="thoushallnotpass")    
    page.click(selector=login_selector)

def navigates_order_your_robot():
    """Navigates to the Order Your Robot"""
    order_your_robot_selector = "//a[contains(@href,'robot-order')][text()='Order your robot!']"
    page.click(selector=order_your_robot_selector)

def close_the_annoying_modal():    
    time.sleep(1)
    popup_ok_button_selector = "//div[@class='alert-buttons']/button[text()='OK']"
    page.click(selector=popup_ok_button_selector)

def download_the_orders_file():
    """Download the orders file from given URL"""
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
    time.sleep(1)

def get_orders_from_csv():
    """Read data from Orders CSV file as a table"""
    orders = tables.read_table_from_csv(path="orders.csv", header=True)
    return orders

def log_out():
    """Presses the 'Log out' button"""
    logout_selectors = "//button[@id='logout'][text()='Log out']"  
    page.click(selector=logout_selectors)
    time.sleep(2)
    page.close()

def order_robots_with_orders_data(orders):
    """Order Robots using orders data"""

    for order in orders:
        process_each_order(order)
        take_robot_screenshot(order)
        export_as_pdf(order)
        close_the_annoying_modal()

def process_each_order(order):    
        head_selector = "//select[@id='head']"
        legs_selector = "//input[@placeholder='Enter the part number for the legs']"
        address_selector = "//input[@id='address']"
        submit_selector = "//button[@id='order'][@type='submit']"
        preview_button = "//button[@id='preview'][@type='submit']" 
        head = order["Head"]
        body = order["Body"]
        legs = order["Legs"]
        address = order["Address"]
        body_selector = f"//input[@value={str(body)}][@type='radio']"

        page.select_option(selector=head_selector, value=head)
        page.click(selector=body_selector)
        page.fill(selector=legs_selector, value=legs)
        page.fill(selector=address_selector, value=address)
        page.click(selector=preview_button)
        time.sleep(2)
        page.click(selector=submit_selector)
        time.sleep(2)

def take_robot_screenshot(order):
    """Take the screenshot for each robot image"""
    order_number = order["Order number"]   
    page.screenshot(path=f"output/robots/{order_number}.png")
    time.sleep(2)

def export_as_pdf(order):
    """Export the recipt data to a pdf file"""
    robot_result_selector = "//div[@id='receipt']"
    another_order_selector = "//button[@id='order-another']"
    order_number = order["Order number"] 
    pdf_path = f"output/recipts/{order_number}.pdf"
    order_results_html = page.locator(selector=robot_result_selector).inner_html()
    pdf.html_to_pdf(order_results_html, pdf_path)
    page.click(selector=another_order_selector)
    time.sleep(2)

def zip_the_recipts_folder():
    """Archive/zip all the order recipts"""
    archive.archive_folder_with_zip("output/recipts/", "output/recipts/reciepts.zip")
    time.sleep(2)




    
    

