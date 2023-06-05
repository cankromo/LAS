from visitor import Visitor
from emailsender import send_email
from qrcode import constants
import qrcode, db

scanning_in_progress = False  # the variable needed for the scanning process

def create_qr(data: str, name: str) -> None:
    """
    Creates a qr code of data named {name} with syntax {id;name;surname;age;email} and saves it in qrcodes folder.
    """

    # Create qr code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f'qrcodes/{name}')


def get_vis(data: str) -> Visitor:
    """
    Returns a visitor object according to the data written in qr code.
    """

    # Split the line into fields
    fields = data.split(';')
    # Create a new instance of Visitor using the fields
    visitor = Visitor(id=fields[0], name=fields[1], surname=fields[2], age=fields[3], email=fields[4])

    return visitor


def add_new_user(data: str):
    """
    adds a new user to database and sends an email to the user containing the qr code.
    """

    # the user input part !!! some conditions has to be set !!!
    id = db.get_number_of_user() + 1

    data = str(id) + ";" + data
    vis: Visitor = get_vis(data)
    qrcode_name = str(id) + "_qrcode.png"
    
    create_qr(data, qrcode_name)

    send_email(
        receiver = data.split(';')[-1],
        attachment_path = "qrcodes/" + qrcode_name
        )

    db.insert_visitor(vis)


def resend_qr_code(id: str, name: str, surname: str, age: str, email: str):
    """
    Resends the email to the user with the id of {id}
    """

    data = id + ";" + name + ";" + surname + ";" + age + ";" + email
    qrcode_name = str(id) + "_qrcode.png"

    create_qr(data, qrcode_name)

    send_email(
        receiver = email,
        attachment_path = "qrcodes/" + qrcode_name
        )